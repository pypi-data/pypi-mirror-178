#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/23 15:54
# @Author  : lj
# @File    : __init__.py.py
from sword_mound.set_sword_mound_config import use_config_form_sword_mound_config_module
from sword_mound import sword_mound_config_default
from sword_mound.patch.print_patch import patch_print_stop as sm_patch_print_stop
from sword_mound.patch.print_patch import patch_print_run as sm_patch_print_run
from sword_mound.tool.times import now_timestamp as sm_now_timestamp
from sword_mound.tool.times import timestamp_to_time as sm_timestamp_to_time
from sword_mound.tool.parse import urlparse as sm_urlparse
from sword_mound.tool import decorators as sm_decorators
name = "sword_mound"
__all__ = [
    'sm_patch_print_stop',
    'sm_now_timestamp',
    'sm_timestamp_to_time',
    'sm_urlparse',
    'sm_decorators'
]
if sword_mound_config_default.DEFAULUT_USE_PRINT_PATCH:
    sm_patch_print_run()