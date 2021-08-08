import logging
import multiprocessing
import time
import uuid

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)5d] - %(levelname)s: %(message)s')
log = logging.getLogger('chaos')


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
            raise ValueError("process pool has started")

        self.pool = multiprocessing.Pool(processes=max_workers)
        log.debug("start process pool successful")
        return True

    def stop(self, force=False):
        if not self.pool:
            log.debug("stop process pool successful")
            return

        self.pool.close()
        self.task_result.clear()
        if force:
            log.warning("force terminal process pool, it is not security")
            self.pool.terminate()
        self.pool = None
        log.debug("stop process pool successful")

    def exec_task(self, func, *args, **kwargs):
        if not self.pool:
            log.warning("process pool has not started")
            raise ValueError("process pool has not started")

        result = self.pool.apply_async(func, args, kwargs)
        task_id = str(uuid.uuid1())
        self.task_result.append(dict(id=task_id, result=result))
        log.debug("add a task to process pool successful")
        return str(task_id)

    def _get_task_result(self, task_id, timeout):
        for item in self.task_result:
            if item['id'] != task_id:
                continue

            while timeout > 0:
                if item['result'].ready():
                    return item['result'].get()

                time.sleep(0.2)
                timeout = timeout - 0.2
        return ValueError(f'get result by task id: {task_id} timeout')

    def _get_all_task_result(self, timeout):
        task_result_ready = dict()
        while timeout > 0:
            try:
                for item in self.task_result:
                    if item['id'] in task_result_ready.keys():
                        continue

                    if item['result'].ready():
                        task_result_ready[item['id']] = True
                        continue

                    time.sleep(0.2)
                    timeout = timeout - 0.2

                if len(task_result_ready) == len(self.task_result):
                    break
            except Exception as e:
                self.stop(True)
                raise e
            finally:
                pass
        if len(task_result_ready) != len(self.task_result):
            raise ValueError("get all task result timeout")

        ret = list()
        for item in self.task_result:
            ret.append(item['result'].get())
        return ret

    def get_task_result(self, task_id: str = None, timeout=120):
        if not self.pool:
            log.warning("process pool has not started")
            raise ValueError("process pool has not started")

        if task_id:
            return self._get_task_result(task_id, timeout)
        return self._get_all_task_result(timeout=timeout)

    def clear_task_result(self, task_id: str = None):
        if not task_id:
            self.task_result.clear()
            return

        for item in self.task_result:
            if item['id'] != task_id:
                continue
            self.task_result.remove(item)
            break


def task(task_id):
    print('task beign')
    time.sleep(3)
    return task_id


if __name__ == '__main__':
    pool = ProcessPool()
    pool.start(3)
    id = pool.exec_task(task, 10)
    print(pool.get_task_result(id, timeout=10))
    pool.stop()
    # pool.clear_task_result()
    # pool.exec_task(task, 11)
    # print(pool.get_task_result())
    # pool.stop()
