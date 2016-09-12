#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/31
"""

from datetime import datetime, timedelta
from sqlalchemy import and_
from ..models.model import *
from ..common.dateutils import date_now, get_next_date
from ..service.booking_service import add_booking, update_booking
from ..service.meeting_service import delete_meeting, add_meeting_bdr
from ..service.org_service import find_org_by_user
import logging
import transaction

logger = logging.getLogger('operator')


def find_org_rooms(dbs, user_id, meeting_date):
    """
    获取可分配的机构
    :param dbs:
    :param user_id:
    :param meeting_date:
    :return:
    """
    orgs = dbs.query(SysOrg.id, SysOrg.org_name, SysOrg.parent_id)\
        .outerjoin(SysUserOrg, (SysUserOrg.org_id == SysOrg.id))\
        .filter(SysUserOrg.user_id == user_id).all()
    rooms = dbs.query(HasBoardroom.id, HasBoardroom.name, HasBoardroom.org_id) \
        .outerjoin(SysOrg, SysOrg.id == HasBoardroom.org_id)\
        .outerjoin(SysUserOrg, (SysUserOrg.org_id == SysOrg.id)) \
        .filter(SysUserOrg.user_id == user_id).all()
    meetings = dbs.query(HasMeeting.id, HasMeeting.name, HasMeeting.description, HasMeetBdr.boardroom_id,
                         HasMeetBdr.meeting_date, HasMeeting.start_time,
                         HasMeeting.end_time, HasMeeting.repeat, HasMeeting.create_user, HasMeeting.create_time,
                         SysUser.user_name, SysUser.phone, SysOrg.org_name)\
        .outerjoin(SysUser, HasMeeting.create_user == SysUser.id)\
        .outerjoin(SysOrg, SysUser.org_id == SysOrg.id)\
        .outerjoin(HasMeetBdr, HasMeetBdr.meeting_id == HasMeeting.id)\
        .outerjoin(HasBoardroom, HasBoardroom.id == HasMeetBdr.boardroom_id)\
        .filter(HasMeetBdr.meeting_date == meeting_date).all()
    lists = []
    for org in orgs:
        org_id = org.id
        org_name = org.org_name
        parent_id = org.parent_id
        # room_list = []
        # for room in rooms:
        #     # 将会议室拼入公司机构list
        #     if org_id == room.org_id:
        #         room_dict = {
        #             'id': room.id,
        #             'name': room.name,
        #             'org_id': org_id
        #         }
        #         room_list.append(room_dict)
        temp_dict = {
            'org_id': org_id,
            'org_name': org_name,
            'parent_id': parent_id
            # 'rooms': room_list
        }
        lists.append(temp_dict)
    return lists


def mob_find_meetings(dbs, user_id=None, room_id=None, meeting_id=None):
    """
    获取会议列表
    :param dbs:
    :param user_id:
    :param room_id:
    :param meeting_id:
    :return:
    """
    meetings = dbs.query(HasMeeting.id, HasMeeting.name, HasMeeting.description,
                         HasMeeting.start_date, HasMeeting.end_date, HasMeeting.start_time,
                         HasMeeting.end_time, HasMeeting.create_user, HasMeeting.create_time,
                         SysUser.user_name, SysUser.phone, SysOrg.org_name) \
        .outerjoin(SysUser, HasMeeting.create_user == SysUser.id) \
        .outerjoin(SysOrg, SysUser.org_id == SysOrg.id) \
        .outerjoin(HasMeetBdr, HasMeetBdr.meeting_id == HasMeeting.id)\
        .outerjoin(HasBoardroom, HasMeetBdr.boardroom_id == HasBoardroom.id)

    if user_id:
        # 取此用户3天内的会议
        today = date_now()[0:10]
        day_after_tomorrow = get_next_date(get_next_date(today))
        meetings = meetings.filter(and_(HasMeeting.create_user == user_id, HasMeeting.start_date >= today,
                                        HasMeeting.start_date <= day_after_tomorrow))
    if meeting_id:
        meetings = meetings.filter(HasMeeting.id == meeting_id)
    if room_id:
        meetings = meetings.filter(HasBoardroom.id == room_id)
    meetings = meetings.all()
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


def mob_find_meeting(dbs, meeting_id):
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
            'org_name': org_name
        }
    return meeting_dict


def mob_find_boardrooms(dbs, user_id):
    """
    查询符合条件的办公室，返回列表和分页对象
    :param dbs:
    :param user_id:
    :return:
    """
    branches = find_org_by_user(dbs, user_id)  # 获取当前用户所分配机构id
    # 当前用户可分配会议室
    boardrooms = dbs.query(HasBoardroom.id,
                           HasBoardroom.name,
                           HasBoardroom.picture,
                           HasBoardroom.config,
                           HasBoardroom.description,
                           HasBoardroom.org_id,
                           SysOrg.org_name,
                           HasBoardroom.pad_id,
                           HasBoardroom.state)\
        .outerjoin(SysOrg, SysOrg.id == HasBoardroom.org_id)
    if branches:
        boardrooms = boardrooms.filter(HasBoardroom.org_id.in_(branches))
    else:
        boardrooms = boardrooms.outerjoin(SysUser, SysUser.org_id == SysOrg.id)
    boardrooms = boardrooms.filter(SysUser.id == user_id).order_by(HasBoardroom.create_time.desc())
    lists = []
    for obj in boardrooms:
        br_id = obj[0] if obj[0] else ''
        br_name = obj[1] if obj[1] else ''
        picture = obj[2] if obj[2] else ''
        config = obj[3] if obj[3] else ''
        description = obj[4] if obj[4] else ''
        org_id = obj[5] if obj[5] else ''
        org_name = obj[6] if obj[6] else ''
        pad_code = obj[7] if obj[7] else ''
        state = obj[8] if obj[8] else ''

        temp_dict = {
            'br_id': br_id,
            'br_name': br_name,
            'picture': (str(org_id) + '/' + picture) if picture else '',
            'config': config,
            'description': description,
            'org_id': org_id,
            'org_name': org_name,
            'pad_code': pad_code,
            'state': state
        }
        lists.append(temp_dict)
    return lists


def mob_find_user_meetings(dbs, user_id=None, start_date=None, end_date=None):
    """
    获取用户预定会议
    :param dbs:
    :param user_id:
    :param start_date:
    :param end_date:
    :return:
    """
    meetings = dbs.query(HasMeeting.id, HasMeeting.name, HasMeeting.description,
                         HasMeeting.start_date, HasMeeting.end_date, HasMeeting.start_time,
                         HasMeeting.end_time, HasMeeting.create_user, HasMeeting.create_time,
                         SysUser.user_name, SysUser.phone, SysOrg.org_name, SysOrg.id,
                         HasMeetBdr.boardroom_id, HasBoardroom.name, HasMeetBdr.meeting_date, HasMeeting.repeat_date) \
        .outerjoin(SysUser, HasMeeting.create_user == SysUser.id) \
        .outerjoin(SysOrg, SysUser.org_id == SysOrg.id) \
        .outerjoin(HasMeetBdr, HasMeetBdr.meeting_id == HasMeeting.id)\
        .outerjoin(HasBoardroom, HasMeetBdr.boardroom_id == HasBoardroom.id)

    if user_id:
        # 取此用户3天内的会议
        # today = date_now()[0:10]
        # day_after_tomorrow = get_next_date(get_next_date(today))
        meetings = meetings.filter(and_(HasMeeting.create_user == user_id, HasMeetBdr.meeting_date >= start_date,
                                        HasMeetBdr.meeting_date <= end_date))
    meetings = meetings.all()
    lists = []
    for meeting in meetings:
        id = meeting[0]
        name = meeting[1]
        description = meeting[2]
        start_date = meeting[3]
        end_date = meeting[15]
        start_time = meeting[15]
        end_time = meeting[6]
        create_user = meeting[7]
        create_time = meeting[8]
        user_name = meeting[9]
        phone = meeting[10]
        org_name = meeting[11]
        org_id = meeting[12]
        room_id = meeting[13]
        room_name = meeting[14]
        repeat = meeting[16]
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
            'org_id': org_id,
            'room_id': room_id,
            'room_name': room_name,
            'repeat': repeat if repeat else ''
        }
        lists.append(temp_dict)
    return lists


def mob_find_org_meetings(dbs, org_id=None, meeting_date=None):
    """
    获取机构会议信息
    :param dbs:
    :param org_id:
    :param meeting_date:
    :return:
    """
    meetings = dbs.query(HasMeeting.id, HasMeeting.name, HasMeeting.description,
                         HasMeeting.start_date, HasMeeting.end_date, HasMeeting.start_time,
                         HasMeeting.end_time, HasMeeting.create_user, HasMeeting.create_time,
                         SysUser.user_name, SysUser.phone, SysOrg.org_name, SysOrg.id,
                         HasMeetBdr.boardroom_id, HasBoardroom.name, HasMeetBdr.meeting_date, HasMeeting.repeat) \
        .outerjoin(SysUser, HasMeeting.create_user == SysUser.id) \
        .outerjoin(SysOrg, SysUser.org_id == SysOrg.id) \
        .outerjoin(HasMeetBdr, HasMeetBdr.meeting_id == HasMeeting.id)\
        .outerjoin(HasBoardroom, HasMeetBdr.boardroom_id == HasBoardroom.id)

    if user_id:
        # 取此用户3天内的会议
        # today = date_now()[0:10]
        # day_after_tomorrow = get_next_date(get_next_date(today))
        meetings = meetings.filter(and_(HasMeeting.create_user == user_id, HasMeetBdr.meeting_date >= start_date,
                                        HasMeetBdr.meeting_date <= end_date))
    meetings = meetings.all()
    lists = []
    for meeting in meetings:
        id = meeting[0]
        name = meeting[1]
        description = meeting[2]
        start_date = meeting[3]
        end_date = meeting[15]
        start_time = meeting[15]
        end_time = meeting[6]
        create_user = meeting[7]
        create_time = meeting[8]
        user_name = meeting[9]
        phone = meeting[10]
        org_name = meeting[11]
        org_id = meeting[12]
        room_id = meeting[13]
        room_name = meeting[14]
        repeat = meeting[16]
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
            'org_id': org_id,
            'room_id': room_id,
            'room_name': room_name,
            'repeat': repeat if repeat else ''
        }
        lists.append(temp_dict)
    return lists
