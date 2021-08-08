import logging
from concurrent.futures._base import as_completed
from concurrent.futures.thread import ThreadPoolExecutor

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)5d] - %(levelname)s: %(message)s')
log = logging.getLogger('choas')


class ThreadPool:
    def __init__(self):
        self.pool = None
        self.task_result = list()
        pass

    def __del__(self):
        self.stop(True)
        pass

    def start(self, max_workers):
        if self.pool:
            log.error("thread pool has started")
            return False
        self.pool = ThreadPoolExecutor(max_workers=max_workers)
        log.debug("start thread pool successful")
        return True

    def stop(self, force=False):
        if not self.pool:
            log.warning("thread pool has stopped or not started")
            return

        if not force:
            self.pool.shutdown()
            self.clear_result()
            self.pool = None
            return
        try:
            self.pool.shutdownNow()
            self.clear_result()
            self.pool = None
        except Exception as e:
            self.pool.shutdown()
            self.pool = None
            return

    def exec_task(self, func, *args, **kwargs):
        if not self.pool:
            log.warning("thread pool has not started")
            return False

        result = self.pool.submit(func, *args, **kwargs)
        self.task_result.append(result)
        log.debug("add a task to thread pool successful")
        return result

    def get_task_result(self, timeout=120):
        all_result = list()
        for future in as_completed(self.task_result, timeout=timeout):
            all_result.append(future.result())

        if len(all_result) != len(self.task_result):
            log.error("get all task result timeout")
            return list()
        else:
            return all_result

    def clear_result(self):
        self.task_result = list()
