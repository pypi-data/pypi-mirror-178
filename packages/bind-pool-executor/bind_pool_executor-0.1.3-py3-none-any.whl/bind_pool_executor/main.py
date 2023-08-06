"""
    @description: 主模块
    @author: llango
    @github: github.com/llango
    @time: 2022.11.26
"""

import multiprocessing
import threading
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


class BindPoolExecutor:
    """
        @description:
        @args: None
        @return: None
    """
    def acquire(self):
        self.semaphore.acquire()
    
    def release(self, fn):
        self.semaphore.release()
    
    def submit(self, fn, *args, **kwargs):
        self.acquire()
        future = super().submit(fn, *args, **kwargs)
        future.add_done_callback(self.release)
        return future 


class BindProcessPoolExecutor(BindPoolExecutor, ProcessPoolExecutor):
    """
        @description:
        @args:
        @return:
    """
    def __init__(self, max_workers=None):
        super().__init__(max_workers)
        self.semaphore = multiprocessing.BoundedSemaphore(self._max_workers)


class BindThreadPoolExecutor(BindPoolExecutor, ThreadPoolExecutor):
    """
        @description:
        @args:
        @return:
    """

    def __init__(self, max_workers=None):
        super().__init__(max_workers)
        self.semaphore = threading.BoundedSemaphore(self._max_workers)
