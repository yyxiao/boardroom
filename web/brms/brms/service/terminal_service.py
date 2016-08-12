#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/12
"""

from ..models.model import *
from ..common.paginator import Paginator
import transaction


def find_terminals(dbs, pad_code, page_no):
    """
    终端列表
    :param dbs:
    :param pad_code:
    :param page_no:
    :return:
    """
    terminals = dbs.query(HasPad.id, HasPad.pad_code, HasPad.last_time, SysUser.user_name, HasPad.create_time)\
        .outerjoin(SysUser, SysUser.id == HasPad.create_user)
    if pad_code:
        terminals = terminals.filter(HasPad.pad_code.like('%'+pad_code+'%'))
    pad_list = terminals.order_by(HasPad.create_time)
    results, paginator = Paginator(pad_list, page_no).to_dict()
    lists = []
    for obj in results:
        id = obj[0] if obj[0] else ''
        pad_code = obj[1] if obj[1] else ''
        last_time = obj[2] if obj[2] else ''
        user_name = obj[3] if obj[3] else ''
        create_time = obj[4] if obj[4] else ''
        temp_dict = {
            'id': id,
            'pad_code': pad_code,
            'last_time': last_time,
            'user_name': user_name,
            'create_time': create_time,
        }
        lists.append(temp_dict)
    return lists, paginator


def add(dbs, terminal):
    error_msg = ''
    try :
        with transaction.manager:
            dbs.add(terminal)
    except Exception:
        error_msg = '新增终端失败，请核对后重试'
    return error_msg


def delete_terminal(dbs, terminal_id):
    error_msg = ''
    try:
        with transaction.manager:
            dbs.query(HasPad).filter(HasPad.terminal_id == terminal_id).delete()
    except Exception:
        error_msg = '删除终端失败，请核对后重试'
    return error_msg


def find_terminal(dbs, terminal_id):
    terminal = dbs.query(HasPad).filter(HasPad.terminal_id == terminal_id).first()
    return terminal
