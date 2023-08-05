#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/23 15:54
# @Author  : lj
# @File    : __init__.py.py
name = "swork_mound"
from swork_mound.patch.print_patch import patch_print_run,patch_print_stop
__all__ = [
    'patch_print_run',
    'patch_print_stop'
]