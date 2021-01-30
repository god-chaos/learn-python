import threading
import time

from common.ThreadPool import ThreadPool, log


def print_message(msg):
    log.info(
        "print message: {}, thread id: {}".format(msg, threading.current_thread().ident))
    time.sleep(2)
    log.info("print message end, thread id is :{}".format(threading.current_thread().ident))
    return True


def test_tasks():
    pool = ThreadPool()
    pool.start(10)
    for i in range(100):
        msg = 'this is id'.format(i)
        pool.exec_task(print_message, msg)

    ret = pool.get_task_result(120)
    if not ret:
        pool.stop(True)
    else:
        log.info(ret)
        pool.stop()
    pass


if __name__ == '__main__':
    test_tasks()
