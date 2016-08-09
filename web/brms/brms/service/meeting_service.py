#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/8
"""

from datetime import datetime
from ..models.model import *
from ..common.paginator import Paginator
import transaction


def find_meetings(dbs, meeting_name, create_user, page_no):
    """
    会议列表
    :param dbs:
    :param meeting_name:
    :param page_no:
    :return:
    """
    meetings = dbs.query(HasMeeting.id,
                         HasMeeting.name,
                         HasMeeting.description,
                         HasMeeting.start_date,
                         HasMeeting.end_date,
                         HasMeeting.start_time,
                         HasMeeting.end_time,
                         SysUser.user_name,
                         HasMeeting.create_time)\
        .outerjoin(SysUser, SysUser.id == HasMeeting.create_user)
    if meeting_name:
        meetings = meetings.filter(HasMeeting.name.like('%'+meeting_name+'%'))
    if create_user:
        meetings = meetings.filter(HasMeeting.create_user.like('%' + create_user + '%'))
    user_list = meetings.order_by(HasMeeting.create_time)
    results, paginator = Paginator(user_list, page_no).to_dict()
    lists = []
    for obj in results:
        id = obj[0] if obj[0] else ''
        name = obj[1] if obj[1] else ''
        description = obj[2] if obj[2] else ''
        start_date = obj[3] if obj[3] else ''
        end_date = obj[4] if obj[4] else ''
        start_time = obj[5] if obj[5] else ''
        end_time = obj[6] if obj[6] else ''
        create_user = obj[7] if obj[7] else ''
        create_time = obj[8] if obj[8] else ''
        temp_dict = {
            'id': id,
            'name': name,
            'description': description,
            'start_date': start_date,
            'end_date': end_date,
            'start_time': start_time,
            'end_time': end_time,
            'create_user': create_user,
            'create_time': create_time,
        }
        lists.append(temp_dict)
    return lists, paginator


def add(dbs, meeting):
    error_msg = ''
    try :
        with transaction.manager:
            dbs.add(meeting)
    except Exception:
        error_msg = '新增会议失败，请核对后重试'
    return error_msg


def delete_meeting(dbs, meeting_id):
    error_msg = ''
    try:
        with transaction.manager:
            dbs.query(HasMeeting).filter(HasMeeting.id == meeting_id).delete()
    except Exception:
        error_msg = '删除会议失败，请核对后重试'
    return error_msg


def find_meeting(dbs, meeting_id):
    meeting = dbs.query(HasMeeting).filter(HasMeeting.id == meeting_id).first()
    return meeting
