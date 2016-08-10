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
import logging

logger = logging.getLogger('operator')


def find_pad_by_id(dbs, pad_code, create_user):
    """
    查找pad_code,存在则获取第一个，不存在则添加一个设备
    :param dbs:
    :param pad_code:
    :param create_user:
    :return:
    """
    error_msg = ''
    pad = dbs.query(HasPad).filter(HasPad.pad_code == pad_code).first()
    if not pad:
        pad = HasPad()
        pad.pad_code = pad_code
        pad.create_user = create_user
        pad.create_time = date_now()
        pad.last_time = date_now()
        pad.org_id = create_user
        try:
            dbs.add(pad)
            dbs.flush()
        except Exception as e:
            logger.error(e)
            error_msg = '新增设备失败，请稍后后重试'
    return pad, error_msg
