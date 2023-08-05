#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/24 14:48
# @Author  : lj
# @File    : decorators.py
import sys
import threading
import time
import unittest
from functools import wraps


def singleton(cls):
    """
    单例模式装饰器,新加入线程锁，更牢固的单例模式，主要解决多线程如100线程同时实例化情况下可能会出现三例四例的情况,实测。
    """
    _instance = {}
    singleton.__lock = threading.Lock()

    @wraps(cls)
    def _singleton(*args, **kwargs):
        with singleton.__lock:
            if cls not in _instance:
                _instance[cls] = cls(*args, **kwargs)
            return _instance[cls]

    return _singleton


def timer(func):
    """计时器装饰器，只能用来计算函数运行时间"""

    @wraps(func)
    def _timer(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        t_spend = round(t2 - t1, 2)
        print('执行[ {} ]方法用时 {} 秒'.format(func.__name__, t_spend))
        return result

    return _timer

class TimerContextManager():
    """
    用上下文管理器计时，可对代码片段计时
    """

    def __init__(self, is_print_log=True):
        self._is_print_log = is_print_log
        self.t_spend = None
        self._line = None
        self._file_name = None
        self.time_start = None

    def __enter__(self):
        self._line = sys._getframe().f_back.f_lineno  # 调用此方法的代码的函数
        self._file_name = sys._getframe(1).f_code.co_filename  # 哪个文件调了用此方法
        self.time_start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.t_spend = time.time() - self.time_start
        print(f'对下面代码片段进行计时:  \n执行"{self._file_name}:{self._line}" 用时 {round(self.t_spend, 2)} 秒')


class __KThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False
        self.__run_backup = None

    # noinspection PyAttributeOutsideInit
    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run  # Force the Thread to install our trace.
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


class TIMEOUT_EXCEPTION(Exception):
    """function run timeout"""
    pass


def timeout(seconds):
    """超时装饰器，指定超时时间

    若被装饰的方法在指定的时间内未返回，则抛出Timeout异常"""

    def timeout_decorator(func):

        def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

        def _(*args, **kwargs):
            result = []
            new_kwargs = {
                'oldfunc': func,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }

            thd = __KThread(target=_new_func, args=(), kwargs=new_kwargs)
            thd.start()
            thd.join(seconds)
            alive = thd.is_alive()
            thd.kill()  # kill the child thread

            if alive:
                # raise TIMEOUT_EXCEPTION('function run too long, timeout %d seconds.' % seconds)
                raise TIMEOUT_EXCEPTION(f'{func.__name__}运行时间超过{seconds}秒')
            else:
                if result:
                    return result[0]
                return result

        _.__name__ = func.__name__
        _.__doc__ = func.__doc__
        return _

    return timeout_decorator


class _Test(unittest.TestCase):
    @unittest.skip
    def test_timer(self):
        """测试计时器装饰器"""

        @timer
        def f7():
            time.sleep(2)

        f7()

    @unittest.skip
    def test_timeout(self):
        """
        测试超时装饰器
        :return:
        """

        @timeout(3)
        def f(time_to_be_sleep):
            time.sleep(time_to_be_sleep)
            print('hello wprld')

        f(5)

if __name__ == '__main__':

    unittest.main()

    # @timeout(3)
    # def f(time_to_be_sleep):
    #     time.sleep(time_to_be_sleep)
    #     print('hello wprld')
    #
    # f(5)