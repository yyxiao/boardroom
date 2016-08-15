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
    pad = dbs.query(HasPad).filter(HasPad.pad_code == pad_code).first()
    try:
        pad.last_time = date_now()
        pad.last_funct = last_funct
        dbs.add(pad)
        dbs.flush()
    except Exception as e:
        logger.error(e)
        error_msg = '新增设备失败，请稍后后重试!'
    return pad, error_msg


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
