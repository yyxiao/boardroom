#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/12
"""

from ..models.model import *
from ..common.paginator import Paginator
import transaction
import logging

logger = logging.getLogger('operator')


def find_terminals(dbs, pad_code, meeting_name, page_no):
    """
    终端列表
    :param dbs:
    :param pad_code:
    :param meeting_name:
    :param page_no:
    :return:
    """
    terminals = dbs.query(HasPad.id, HasPad.pad_code, HasPad.last_time, SysUser.user_name,
                          HasPad.create_time, HasBoardroom.name)\
        .outerjoin(SysUser, SysUser.id == HasPad.create_user)\
        .outerjoin(HasBoardroom, HasBoardroom.pad_id == HasPad.id)
    if pad_code:
        terminals = terminals.filter(HasPad.pad_code.like('%'+pad_code+'%'))
    if meeting_name:
        terminals = terminals.filter(HasBoardroom.name.like('%' + meeting_name + '%'))
    pad_list = terminals.order_by(HasPad.create_time.desc())
    results, paginator = Paginator(pad_list, page_no).to_dict()
    lists = []
    for obj in results:
        id = obj[0] if obj[0] else ''
        pad_code = obj[1] if obj[1] else ''
        last_time = obj[2] if obj[2] else ''
        user_name = obj[3] if obj[3] else ''
        create_time = obj[4] if obj[4] else ''
        bdr_name = obj[5] if obj[5] else ''
        temp_dict = {
            'id': id,
            'pad_code': pad_code,
            'last_time': last_time,
            'create_user': user_name,
            'create_time': create_time,
            'bdr_name': bdr_name,
        }
        lists.append(temp_dict)
    return lists, paginator


def add(dbs, terminal, room_id):
    error_msg = ''
    try :
        dbs.add(terminal)
        dbs.flush()
        logger.debug("终端添加完毕，terminal_id:" + str(terminal.id))
        terminal_id = terminal.id  # 终端ID
        room1 = dbs.query(HasBoardroom).filter(HasBoardroom.pad_id == terminal_id).first()
        if room1:                   # 清除以前会议室pad_id数据
            room1.pad_id = 0
            dbs.add(room1)
        room = dbs.query(HasBoardroom).filter(HasBoardroom.id == room_id).first()
        room.pad_id = terminal_id
        dbs.add(room)
    except Exception as e:
        logger.error(e)
        error_msg = '新增终端失败，请核对后重试'
    return error_msg


def delete_terminal(dbs, terminal_id):
    error_msg = ''
    try:
        with transaction.manager:
            dbs.query(HasPad).filter(HasPad.id == terminal_id).delete()
    except Exception as e:
        logger.error(e)
        error_msg = '删除终端失败，请核对后重试'
    return error_msg


def find_terminal(dbs, terminal_id):
    terminal = dbs.query(HasPad.id, HasPad.pad_code, HasBoardroom.id.label("room_id"))\
        .outerjoin(HasBoardroom, HasBoardroom.pad_id == HasPad.id).filter(HasPad.id == terminal_id).first()
    return terminal


def find_rooms(dbs, user_id):
    """
    获取该用户可选择的会议室
    :param dbs:
    :param user_id:
    :return:
    """
    room_list = []
    rooms = dbs.query(HasBoardroom.id, HasBoardroom.name, HasBoardroom.org_id) \
        .outerjoin(SysOrg, SysOrg.id == HasBoardroom.org_id) \
        .outerjoin(SysUserOrg, SysUserOrg.org_id == SysOrg.id) \
        .filter(SysUserOrg.user_id == user_id).all()
    for room in rooms:
        # 将会议室拼入公司机构list
        room_dict = {
            'id': room.id,
            'name': room.name
        }
        room_list.append(room_dict)
    return room_list
