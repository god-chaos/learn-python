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
        self.stop()
        self.pool = multiprocessing.Pool(processes=max_workers)
        return True

    def stop(self, force=False):
        if not self.pool:
            return

        self.pool.close()
        self.task_result.clear()
        if force:
            self.pool.terminal()
        self.pool = None

    def exec_task(self, func, *args, **kwargs):
        if not self.pool:
            return False

        result = self.pool.apply_async(func, *args, **kwargs)
        self.task_result.append(result)
        return result

    def get_task_result(self, timeout=120):
        task_result_ready = dict()
        while timeout > 0:
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
        if len(task_result_ready) != len(self.task_result):
            return list()

        ret = list()
        for res in self.task_result:
            ret.append(res.get())
        return ret

    def clear_task_result(self):
        self.task_result.clear()
