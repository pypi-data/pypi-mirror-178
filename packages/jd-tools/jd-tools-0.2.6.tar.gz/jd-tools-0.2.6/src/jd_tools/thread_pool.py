# -*- coding:utf-8 -*-
# 文件:  thread_pool.py
# 日期:  2022/8/19 9:50
"""

"""
import threading
from concurrent import futures
from .logs import logger


__version__ = '1.1'
__all__ = ['JdThreadPool']


class JdThreadPool(object):
    """
    线程池
    """

    def __init__(self, max_workers=5):
        self.pool = futures.ThreadPoolExecutor(max_workers=max_workers)
        self._thread_lock = threading.Lock()
        self._future = set()

    def add_job(self, callback, para):
        thread_name = threading.current_thread().name
        logger.debug(f"[ {thread_name} ], {para}")
        future = self.pool.submit(callback, para)
        self._thread_lock.acquire()
        self._future.add(future)
        self._thread_lock.release()
        future.add_done_callback(self.done)

    def done(self, future: futures.Future):
        thread_name = threading.current_thread().name
        logger.debug(f"[ {thread_name} ]执行完成： {future.result()}")
        self._thread_lock.acquire()
        self._future.remove(future)
        self._thread_lock.release()
