import time
from functools import wraps


def exec_time(func):
    """
    功能描述：定义嵌套函数，用来打印出装饰的函数的执行时间
    :param func: func参数（自动）
    :return: 返回内部wrapper函数
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        功能描述：定义开始时间和结束时间，将func夹在中间执行，取得其返回值
        :param args:
        :param kwargs:
        :return: 被装饰函数的实际返回值
        """
        start = time.time() * 1000
        func_ret = func(*args, **kwargs)
        end = time.time() * 1000
        print('func:{%s} exec time is:{%.5f} ms' % (func.__name__, end - start))
        return func_ret

    # 返回嵌套的函数
    return wrapper
