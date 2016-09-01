#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/31
"""

from datetime import datetime, timedelta
from ..models.model import *
from ..common.dateutils import date_now, date_pattern1
from ..service.booking_service import add_booking, update_booking
from ..service.meeting_service import delete_meeting, add_meeting_bdr
import logging
import transaction

logger = logging.getLogger('operator')


def find_org_rooms(dbs, user_id):
    """
    获取可分配的机构
    :param dbs:
    :param user_id:
    :return:
    """
    orgs = dbs.query(SysOrg.id, SysOrg.org_name, SysOrg.parent_id)\
        .outerjoin(SysUserOrg, (SysUserOrg.org_id == SysOrg.id))\
        .filter(SysUserOrg.user_id == user_id).all()
    rooms = dbs.query(HasBoardroom.id, HasBoardroom.name, HasBoardroom.org_id) \
        .outerjoin(SysOrg, SysOrg.id == HasBoardroom.org_id)\
        .outerjoin(SysUserOrg, (SysUserOrg.org_id == SysOrg.id)) \
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
                    'id': room.id,
                    'name': room.name,
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


def find_meetings(dbs, user_id, room_id):
    meetings = dbs.query(HasMeeting.id, HasMeeting.name, HasMeeting.description,
                         HasMeeting.start_date, HasMeeting.end_date, HasMeeting.start_time,
                         HasMeeting.end_time, HasMeeting.create_user, HasMeeting.create_time,
                         SysUser.user_name, SysUser.phone, SysOrg.org_name) \
        .outerjoin(SysUser, HasMeeting.create_user == SysUser.id) \
        .outerjoin(SysOrg, SysUser.org_id == SysOrg.id) \
        .outerjoin(HasMeetBdr, HasMeetBdr.meeting_id == HasMeeting.id)\
        .outerjoin(HasBoardroom, HasMeetBdr.boardroom_id == HasBoardroom.id)\
        .filter(HasBoardroom.id == room_id).all()
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
    return lists
