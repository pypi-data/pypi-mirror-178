#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/23 16:12
# @Author  : lj
# @File    : print_patch.py
import multiprocessing
import sys
import time
import traceback
from platform import system

print_raw = print

WORD_COLOR = 37


def stdout_write(msg: str):
    sys.stdout.write(msg)
    sys.stdout.flush()


def stderr_write(msg: str):
    sys.stderr.write(msg)
    sys.stderr.flush()


def x_print(*args, sep=' ', end='\n', file=None, flush=True):
    """
    超流弊的print补丁
    :param x:
    :return:
    """
    args = (str(arg) for arg in args)  # REMIND 防止是数字不能被join
    if file == sys.stderr:
        stderr_write(sep.join(args))  # 如 threading 模块第926行，打印线程错误，希望保持原始的红色错误方式，不希望转成蓝色。
    elif file in [sys.stdout, None]:
        Location = traceback.extract_stack()
        # filename = Location[0].filename
        # lineno = Location[0].lineno

        line = sys._getframe().f_back.f_lineno
        # 获取被调用函数所在模块文件名

        file_name = sys._getframe(1).f_code.co_filename
        if system() == 'Windows':
            stdout_write(
            f'\033[0;{WORD_COLOR};34m{time.strftime("%H:%M:%S")}  "{file_name}:{line}" | {sep.join(args)} {end} \033[0m')  # 36  93 96 94
        else:
            stdout_write(f'{time.strftime("%H:%M:%S")}  "{file_name}:{line}" | {sep.join(args)} {end}')
    else:  # 例如traceback模块的print_exception函数 file的入参是   <_io.StringIO object at 0x00000264F2F065E8>，必须把内容重定向到这个对象里面，否则exception日志记录不了错误堆栈。
        print_raw(*args, sep=sep, end=end, file=file)


# print = nb_print

def is_main_process():
    return multiprocessing.process.current_process().name == 'MainProcess'

def patch_print_run():
    """
    Python有几个namespace，分别是

    locals

    globals

    builtin

    其中定义在函数内声明的变量属于locals，而模块内定义的函数属于globals。


    https://codeday.me/bug/20180929/266673.html   python – 为什么__builtins__既是模块又是dict

    :return:
    """
    try:
        __builtins__.print = x_print
    except AttributeError:
        """
        <class 'AttributeError'>
        'dict' object has no attribute 'print'
        """
        # noinspection PyUnresolvedReferences
        __builtins__['print'] = x_print
    # traceback.print_exception = print_exception  # file类型为 <_io.StringIO object at 0x00000264F2F065E8> 单独判断，解决了，不要加这个。

def patch_print_stop():
    """
    提供一个反猴子补丁，恢复print原状
    :return:
    """
    # try:
    #     __builtins__.print = common_print
    # except AttributeError:
    #     __builtins__['print'] = common_print

    try:
        __builtins__.print = print_raw
    except AttributeError:
        __builtins__['print'] = print_raw

if __name__ == '__main__':
    patch_print_run()
    print('aaa',789)