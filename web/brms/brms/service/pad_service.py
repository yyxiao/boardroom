#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/10
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import aliased
from ..models.model import *
from ..common.paginator import Paginator
from ..common.dateutils import date_now, date_pattern1
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
    json_dict = {}
    pad = dbs.query(HasPad.id, HasBoardroom.id, HasBoardroom.name)\
        .outerjoin(HasBoardroom,HasBoardroom.pad_id == HasPad.id)\
        .filter(HasPad.pad_code == pad_code).first()
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
            json_dict = {'pad_id': pad.id
                         }
        except Exception as e:
            logger.error(e)
            error_msg = '新增设备失败，请稍后后重试!'
    else:
        json_dict = {'pad_id': pad[0],
                     'room_id': pad[1],
                     'room_name': pad[2]
                     }
    return json_dict, error_msg


def update_last_time(dbs, pad_code, last_funct):
    """
    更新最后通信时间
    :param dbs:
    :param pad_code: 设备编码
    :param last_funct: 设备最后调用方法
    :return:
    """
    pad = dbs.query(HasPad).filter(HasPad.pad_code == pad_code).first()
    try:
        pad.last_time = date_now()
        pad.last_funct = last_funct
        dbs.add(pad)
        dbs.flush()
    except Exception as e:
        logger.error(e)


def find_meetings(dbs, pad_code):
    """
    pad获取会议列表，近三天
    :param dbs:
    :param pad_code:
    :return:
    """
    error_msg = ''
    now_day = datetime.now().strftime(date_pattern1)
    delta = timedelta(days=3)
    n_days = datetime.now() + delta
    n_days = n_days.strftime(date_pattern1)
    print("now_day"+now_day+"n_days"+n_days)
    meetings = dbs.query(HasMeeting.id, HasMeeting.name, HasMeeting.description,
                         HasMeeting.start_date, HasMeeting.end_date, HasMeeting.start_time,
                         HasMeeting.end_time, HasMeeting.create_user, HasMeeting.create_time,
                         SysUser.user_name, SysUser.phone, SysOrg.org_name)\
        .outerjoin(SysUser, HasMeeting.create_user == SysUser.id)\
        .outerjoin(SysOrg, SysUser.org_id == SysOrg.id)\
        .outerjoin(HasMeetBdr, HasMeetBdr.meeting_id == HasMeeting.id)\
        .outerjoin(HasBoardroom, HasBoardroom.id == HasMeetBdr.boardroom_id)\
        .outerjoin(HasPad, HasPad.id == HasBoardroom.pad_id)\
        .filter(HasPad.pad_code == pad_code)\
        .filter(HasMeeting.start_date < n_days).filter(HasMeeting.start_date >= now_day)
    lists = []
    for meeting in meetings:
        id = meeting.id
        name = meeting.name
        description = meeting.description
        start_date = meeting.start_date
        end_date = meeting.end_date
        start_time = meeting.start_time
        end_time = meeting.end_time
        create_user = meeting.create_user
        create_time = meeting.create_time
        user_name = meeting.user_name
        phone = meeting.phone
        org_name = meeting.org_name
        temp_dict = {
            'meeting_id': id,
            'meeting_name': name,
            'description': description,
            'start_date': start_date,
            'end_date': end_date,
            'start_time': start_time,
            'end_time': end_time,
            'create_user': create_user,
            'create_time': create_time,
            'user_name': user_name,
            'user_phone': phone,
            'org_name': org_name,
        }
        lists.append(temp_dict)
    return lists, error_msg


def add_by_pad(dbs, meeting, pad_code):
    """
    PAD添加会议
    :param dbs:
    :param meeting:
    :param pad_code
    :return:
    """
    error_msg = ''
    meeting_id = 0
    try:
        # 查询padcode对应的boardroom_id
        board = dbs.query(HasBoardroom.id)\
            .outerjoin(HasPad, HasBoardroom.pad_id == HasPad.id)\
            .filter(HasPad.pad_code == pad_code).first()
        if not board:                                       # 不存在
            error_msg = '该pad未分配会议室，请联系管理员！'
        else:
            # 添加会议
            dbs.add(meeting)
            dbs.flush()
            logger.debug("会议添加完毕，meeting_id:" + str(meeting.id))
            meeting_id = meeting.id                         # 会议ID
            meet_bdr = HasMeetBdr()                         # 会议室会议关联信息
            meet_bdr.meeting_id = meeting_id
            meet_bdr.boardroom_id = board.id
            meet_bdr.create_user = meeting.create_user
            meet_bdr.create_time = date_now()
            dbs.add(meet_bdr)
            logger.debug("会议会议室关联添加完毕")
    except Exception as e:
        logger.error(e)
        error_msg = '新增会议失败，请核对后重试'
    return error_msg, meeting_id


def update_by_pad(dbs, meeting, pad_code):
    """
    PAD更新会议
    :param dbs:
    :param meeting:
    :param pad_code
    :return:
    """
    error_msg = ''
    try:
        # 查询padcode对应的boardroom_id
        board = dbs.query(HasBoardroom.id)\
            .outerjoin(HasPad, HasBoardroom.pad_id == HasPad.id)\
            .filter(HasPad.pad_code == pad_code).first()
        if not board:                                       # 不存在
            error_msg = '该pad未分配会议室，请联系管理员！'
        else:
            # 更新会议
            dbs.add(meeting)
            dbs.flush()
            logger.debug("会议更新完毕，meeting_id:" + str(meeting.id))
    except Exception as e:
        logger.error(e)
        error_msg = '更新会议失败，请核对后重试'
    return error_msg, meeting.id


def pad_find_meeting(dbs, meeting_id):
    """
    获取会议以及会议室关联的名称
    :param dbs:
    :param meeting_id:
    :return:
    """
    meeting_dict = {}
    meeting = dbs.query(HasMeeting.id, HasMeeting.name, HasMeeting.description,
                         HasMeeting.start_date, HasMeeting.end_date, HasMeeting.start_time,
                         HasMeeting.end_time, HasMeeting.create_user, HasMeeting.create_time,
                         SysUser.user_name, SysUser.phone, SysOrg.org_name)\
        .outerjoin(SysUser, HasMeeting.create_user == SysUser.id)\
        .outerjoin(SysOrg, SysUser.org_id == SysOrg.id)\
        .filter(HasMeeting.id == meeting_id).first()
    if meeting:
        id = meeting.id
        name = meeting.name
        description = meeting.description
        start_date = meeting.start_date
        end_date = meeting.end_date
        start_time = meeting.start_time
        end_time = meeting.end_time
        create_user = meeting.create_user
        create_time = meeting.create_time
        user_name = meeting.user_name
        phone = meeting.phone
        org_name = meeting.org_name
        meeting_dict = {
            'meeting_id': id,
            'meeting_name': name,
            'description': description,
            'start_date': start_date,
            'end_date': end_date,
            'start_time': start_time,
            'end_time': end_time,
            'create_user': create_user,
            'create_time': create_time,
            'user_name': user_name,
            'user_phone': phone,
            'org_name': org_name,
        }
    return meeting_dict


def pad_find_orgs(dbs, user_id):
    """
    pad获取可分配的机构
    :param dbs:
    :param user_id:
    :return:
    """
    orgs = dbs.query(SysOrg.id, SysOrg.org_name, SysOrg.parent_id)\
        .outerjoin(SysUserOrg, (SysUserOrg.org_id == SysOrg.id) | (SysUserOrg.org_id == SysOrg.parent_id))\
        .filter(SysUserOrg.user_id == user_id).all()
    rooms = dbs.query(HasBoardroom.id, HasBoardroom.name, HasBoardroom.org_id) \
        .outerjoin(SysOrg, SysOrg.id == HasBoardroom.org_id)\
        .outerjoin(SysUserOrg, (SysUserOrg.org_id == SysOrg.id) | (SysUserOrg.org_id == SysOrg.parent_id)) \
        .filter(SysUserOrg.user_id == user_id).all()
    lists = []
    for org in orgs:
        org_id = org.id
        org_name = org.org_name
        parent_id = org.parent_id
        room_list = []
        for room in rooms:
            # 将会议室拼入公司机构list
            if org_id == room.org_id:
                room_dict = {
                    'room_id': room.id,
                    'room_name': room.name,
                    'org_id': org_id
                }
                room_list.append(room_dict)
        temp_dict = {
            'org_id': org_id,
            'org_name': org_name,
            'parent_id': parent_id,
            'rooms': room_list
        }
        lists.append(temp_dict)
    return lists