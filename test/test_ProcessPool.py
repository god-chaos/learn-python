import os
import time

from common.ProcessPool import ProcessPool, log


def print_message(msg):
    log.info("print message: {}, process id is :{}".format(msg, os.getpid()))
    time.sleep(2)
    log.info("print message end, process id is :{}".format(os.getpid()))


def test_process():
    pool = ProcessPool()
    pool.start(10)
    for i in range(100):
        msg = 'this is id'.format(i)
        pool.exec_task(print_message, msg)

    ret = pool.get_task_result(timeout=120)
    if not ret:
        pool.stop(True)
    else:
        log.info(ret)
        pool.stop()
    pass


if __name__ == '__main__':
    test_process()
