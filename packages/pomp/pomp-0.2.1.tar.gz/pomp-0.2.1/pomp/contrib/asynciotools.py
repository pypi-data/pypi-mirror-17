import sys
import logging
import asyncio
from functools import partial


try:
    from asyncio import ensure_future
except ImportError:  # pragma: no cover
    from asyncio import async as ensure_future


from pomp.core.base import BaseQueue, BaseCrawlException
from pomp.core.utils import iterator, Planned
from pomp.core.engine import StopCommand
from pomp.core.engine import Pomp as SyncPomp

from pomp.contrib.concurrenttools import (
    _run_crawler_worker, ConcurrentCrawler,
)


log = logging.getLogger(__name__)


class SimpleAsyncioQueue(BaseQueue):

    def __init__(self, use_lifo=False):
        self.q = asyncio.Queue() if use_lifo else asyncio.LifoQueue()

    @asyncio.coroutine
    def get_requests(self, count=None):
        return (yield from self.q.get())

    @asyncio.coroutine
    def put_requests(self, requests):
        yield from self.q.put(requests)


class AioPomp(SyncPomp):
    DEFAULT_QUEUE_CLASS = SimpleAsyncioQueue

    @asyncio.coroutine
    def pump(self, crawler):
        """Start crawling

        :param crawler: isntance of :class:`pomp.core.base.BaseCrawler`
        """
        self.prepare(crawler)

        # add ENTRY_REQUESTS to the queue
        next_requests = getattr(crawler, 'ENTRY_REQUESTS', None)
        if next_requests:
            yield from self._put_requests(
                iterator(next_requests), request_done=False,
            )

        _pending_iteration_tasks = []

        def _on_iterations_task_done(task, future):
            _pending_iteration_tasks.remove(task)

        while True:

            # pre-lock
            if self.queue_lock:
                yield from self.queue_lock.acquire()

            next_requests = yield from self.queue.get_requests(
                count=self.queue_semaphore_value
            )

            if isinstance(next_requests, StopCommand):
                break

            # process requests and do not block loop
            task = asyncio.ensure_future(
                self.process_requests(
                    iterator(next_requests), crawler,
                )
            )
            _pending_iteration_tasks.append(task)
            task.add_done_callback(
                partial(_on_iterations_task_done, task)
            )

            # block loop if requests in process more than downloader
            # can fetch
            if self.queue_lock:
                if self.queue_semaphore_value <= 0:
                    yield from self.queue_lock.acquire()
                elif self.queue_lock.locked():
                    self.queue_lock.release()

        # loop ended, but we have pending tasks - wait
        if _pending_iteration_tasks:
            log.debug(
                "Wait pending iteration tasks: %s",
                len(_pending_iteration_tasks),
            )
            yield from asyncio.wait(_pending_iteration_tasks)

        self.finish(crawler)

    @asyncio.coroutine
    def process_requests(self, requests, crawler):

        # execute requests by downloader
        for response in self.downloader.process(
                # process requests by middlewares
                self._req_middlewares(requests, crawler), crawler):

            if response is None:
                # response was rejected by middlewares
                pass

            elif isinstance(response, Planned):
                future = asyncio.Future()

                def _(r):
                    response = r.result()
                    ensure_future(
                        # put new requests to queue
                        self._put_requests(
                            # process response by crawler
                            self.response_callback(
                                crawler,
                                # pass response to middlewares
                                self._resp_middlewares(response, crawler),
                            ),
                            response,
                            crawler,
                        )
                    ).add_done_callback(
                        future.set_result
                    )

                response.add_done_callback(_)

                yield from future
            else:
                # put new requests to queue
                yield from self._put_requests(
                    # process response by crawler
                    self.response_callback(
                        crawler,
                        # pass response to middlewares
                        self._resp_middlewares(response, crawler),
                    ),
                    response,
                    crawler,
                )

    @asyncio.coroutine
    def _put_requests(
            self, requests, response=None, crawler=None, request_done=True):

        @asyncio.coroutine
        def _put(items):

            if items:
                for item in items:
                    self.in_progress += 1
                    yield from self.queue.put_requests(item)

            if request_done:
                yield from self._request_done(response, crawler)

        if isinstance(requests, Planned):
            future = asyncio.Future()

            def _(r):
                ensure_future(
                    _put(r.result())
                ).add_done_callback(
                    future.set_result
                )

            requests.add_done_callback(_)

            yield from future
        else:
            yield from _put(requests)

    @asyncio.coroutine
    def _request_done(self, response, crawler):
        if self.queue_lock:
            # increment counter, but not more then workers count
            self.queue_semaphore_value = min(
                self.workers_count,
                self.queue_semaphore_value + 1,
            )
            if self.queue_semaphore_value > 0 and self.queue_lock.locked():
                self.queue_lock.release()

        self.in_progress -= 1

        # send StopCommand if all jobs are done and running on internal queue
        if self._is_internal_queue and self.in_progress == 0:
            # work done
            yield from self.queue.put_requests(StopCommand())

        # response processing complete
        try:
            crawler.on_processing_done(response)
        except Exception as e:
            log.exception("On done processing exception")
            self._exception_middlewares(
                BaseCrawlException(
                    request=response.request,
                    response=response,
                    exception=e,
                    exc_info=sys.exc_info(),
                ),
                crawler,
            )

    def get_queue_lock(self):
        workers_count = self.downloader.get_workers_count()
        if workers_count >= 1:
            self.queue_semaphore_value = workers_count
            self.workers_count = workers_count
            return asyncio.Lock()


class AioConcurrentCrawler(ConcurrentCrawler):

    def process(self, response):

        # build Planned object
        done_future = Planned()

        # fire done_future when asyncio finish response processing by
        # crawler worker in executor
        asyncio.ensure_future(
            asyncio.get_event_loop().run_in_executor(
                self.executor,
                _run_crawler_worker,
                self.worker_params,
                response,
            )
        ).add_done_callback(
            partial(self._done, response, done_future)
        )

        return done_future
