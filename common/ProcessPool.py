import logging
import multiprocessing
import time

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)5d] - %(levelname)s: %(message)s')
log = logging.getLogger('choas')


class ProcessPool:
    def __init__(self):
        self.pool = None
        self.task_result = list()

    def __del__(self):
        self.stop(True)
        pass

    def start(self, max_workers: int):
        if self.pool:
            log.error("process pool has started")
            return False
        self.pool = multiprocessing.Pool(processes=max_workers)
        log.debug("start process pool successful")
        return True

    def stop(self, force=False):
        if not self.pool:
            log.warning("process pool has stopped")
            return

        self.pool.close()
        self.task_result.clear()
        if force:
            log.warning("force terminal process pool, it is not security")
            self.pool.terminal()
        self.pool = None
        log.debug("stop process pool successful")

    def exec_task(self, func, *args, **kwargs):
        if not self.pool:
            log.warning("process pool has not started")
            return False

        result = self.pool.apply_async(func, args, kwargs)
        self.task_result.append(result)
        log.debug("add a task to process pool successful")
        return result

    def get_task_result(self, timeout=120):
        task_result_ready = dict()
        while timeout > 0:
            try:
                for index, res in enumerate(self.task_result):
                    if str(index) in task_result_ready.keys():
                        continue

                    if res.ready():
                        task_result_ready[str(index)] = True
                        continue

                    time.sleep(0.2)
                    timeout = timeout - 0.2
                if len(task_result_ready) == len(self.task_result):
                    break
            except Exception as e:
                self.stop(True)
                raise e
        if len(task_result_ready) != len(self.task_result):
            log.error("get all task result timeout")
            return list()

        ret = list()
        for res in self.task_result:
            ret.append(res.get())
        return ret

    def clear_task_result(self):
        self.task_result.clear()
