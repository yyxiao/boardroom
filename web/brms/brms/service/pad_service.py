#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/10
"""

from datetime import datetime
from ..models.model import *
from ..common.paginator import Paginator
from ..common.dateutils import date_now
import transaction


def find_pad_by_id(dbs, pad_code, create_user):
    pad = HasPad()
    pad.pad_code = pad_code
    pad.create_user = create_user
    pad.create_time = date_now()
    pad.last_time = date_now()
    pad.org_id = create_user
    try:
        with transaction.manager:
            dbs.add(pad)
    except Exception:
        error_msg = '新增设备失败，请稍后后重试'
    return pad
