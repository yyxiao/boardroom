#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/8
"""

import json
import copy
import logging
import transaction
from sqlalchemy.sql import and_
from ..models.model import *
from ..common.paginator import Paginator
from ..common.dateutils import date_now, get_weekday, add_date
from ..service.booking_service import check_repeat_occupy, add_booking, delete_booking
from ..service.org_service import find_org_ids, find_parent_org

logger = logging.getLogger('operator')


def find_meetings(dbs, user_id=None, user_org_id=None, meeting_name=None, room_name=None, start_date=None,
                  end_date=None, org_id=None, page_no=1):
    """
    会议列表
    :param dbs:
    :param user_id:
    :param user_org_id:
    :param meeting_name:
    :param room_name:
    :param start_date:
    :param end_date:
    :param org_id:
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
                         HasMeeting.create_time,
                         HasBoardroom.name)\
        .outerjoin(SysUser, SysUser.id == HasMeeting.create_user)\
        .outerjoin(SysUserOrg, and_(SysUserOrg.user_id == SysUser.id, HasMeeting.org_id == SysUserOrg.org_id))\
        .outerjoin(SysOrg, SysUserOrg.org_id == SysOrg.id) \
        .outerjoin(HasMeetBdr,
                   and_(HasMeetBdr.meeting_id == HasMeeting.id, HasMeetBdr.meeting_date == HasMeeting.end_date)) \
        .outerjoin(HasBoardroom, HasBoardroom.id == HasMeetBdr.boardroom_id)\
        .outerjoin(HasPad, HasPad.id == HasBoardroom.pad_id)
    branches = find_org_ids(dbs, user_org_id)               # 获取当前用户所属机构及下属机构id
    if meeting_name:
        meetings = meetings.filter(HasMeeting.name.like('%'+meeting_name+'%'))
    if user_id:
        meetings = meetings.filter(HasMeeting.create_user == user_id)
    if user_org_id and branches:
        meetings = meetings.filter(SysOrg.id.in_(branches))
    if start_date:
        meetings = meetings.filter(HasMeeting.start_date >= start_date)
    if end_date:
        meetings = meetings.filter(HasMeeting.end_date <= end_date)
    if room_name:
        meetings = meetings.filter(HasBoardroom.name.like('%' + room_name + '%'))
    if org_id:
        meetings = meetings.filter(HasMeeting.org_id == org_id)

    meeting_list = meetings.order_by(HasMeeting.create_time.desc())
    if page_no == 0:
        results = meeting_list.all()
        paginator = None
    else:
        results, paginator = Paginator(meeting_list, page_no).to_dict()
    lists = []
    for obj in results:
        meeting_id = obj[0] if obj[0] else ''
        name = obj[1] if obj[1] else ''
        description = obj[2] if obj[2] else ''
        start_date = obj[3] if obj[3] else ''
        end_date = obj[4] if obj[4] else ''
        start_time = obj[5] if obj[5] else ''
        end_time = obj[6] if obj[6] else ''
        create_user = obj[7] if obj[7] else ''
        create_time = obj[8] if obj[8] else ''
        room_name = obj[9] if obj[9] else ''
        temp_dict = {
            'id': meeting_id,
            'name': name,
            'description': description,
            'start_date': start_date,
            'end_date': end_date,
            'start_time': start_time,
            'end_time': end_time,
            'create_user': create_user,
            'create_time': create_time,
            'room_name': room_name
        }
        lists.append(temp_dict)
    return lists, paginator


def find_meeting_calendar(dbs, user_id, org_ids, room_id, user_org_id):
    """

    :param dbs:
    :param user_id:
    :param org_ids:
    :param room_id:
    :param user_org_id:
    :return:
    """

    user_parent_org_id = find_parent_org(dbs, user_org_id)
    if user_org_id != user_parent_org_id:
        org_ids.append(user_org_id)
    meetings = dbs.query(HasMeeting.id,
                         HasMeeting.name,
                         HasMeeting.description,
                         HasMeeting.start_date,
                         HasMeeting.end_date,
                         HasMeeting.start_time,
                         HasMeeting.end_time,
                         HasMeeting.create_user,
                         HasMeeting.repeat,         # 重复会议的结束类型 no: 无结束时间, 数字:重复次数, 日期: 截止日期
                         HasMeeting.repeat_date,    # 重复的周天，0～6,如：1,3,5
                         SysUser.user_name,
                         HasMeetBdr.boardroom_id) \
        .outerjoin(SysUser, SysUser.id == HasMeeting.create_user) \
        .outerjoin(SysOrg, HasMeeting.org_id == SysOrg.id) \
        .outerjoin(HasMeetBdr, HasMeetBdr.meeting_id == HasMeeting.id)
    if org_ids and len(org_ids) > 0:
        meetings = meetings.filter(SysOrg.id.in_(org_ids))
    if room_id:
        meetings = meetings.filter(HasMeetBdr.boardroom_id == room_id)

    meeting_list = meetings.order_by(HasMeetBdr.meeting_date.desc())
    results = meeting_list.all()

    lists = []
    for obj in results:
        meeting_id = obj[0] if obj[0] else ''
        name = obj[1] if obj[1] else ''
        description = obj[2] if obj[2] else ''
        start_date = obj[3] if obj[3] else ''
        end_date = obj[4] if obj[4] else ''
        start_time = obj[5] if obj[5] else ''
        end_time = obj[6] if obj[6] else ''
        create_user = obj[7] if obj[7] else ''
        repeat = obj[8] if obj[8] else ''
        repeat_date = obj[9] if obj[9] else ''
        user_name = obj[10] if obj[10] else ''
        room_id = obj[11] if obj[11] else ''
        temp_dict = {
            'id': meeting_id,
            # 'event_pid': '0',
            'event_length': get_event_length(start_time, end_time),      # TODO 夸天会议
            'text': name,
            'desc': description,
            'start_date': start_date + " " + start_time,
            'end_date': end_date + " " + end_time,
            'rec_pattern': repeat_date if repeat_date and repeat else '',
            'rec_type': (repeat_date + "#" + repeat) if repeat_date and repeat else '',
            'user_name': user_name,
            'room_id': room_id,
            '': (repeat_date + "#" + repeat) if repeat_date and repeat else ''
        }
        if create_user != user_id:  # or temp_dict['rec_type']:
            temp_dict['readonly'] = True

        lists.append(temp_dict)
    return lists


def get_event_length(start_time, end_time):
    start = int(start_time[0:2]) * 3600 + int(start_time[3:5]) * 60
    end = int(end_time[0:2]) * 3600 + int(end_time[3:5]) * 60
    return end - start


def add(dbs, meeting, room_id):
    """
    PC添加会议
    :param dbs:
    :param meeting:
    :param room_id
    :return:
    """
    error_msg = ''
    try:
        # 添加会议
        dbs.add(meeting)
        dbs.flush()
        logger.debug("会议添加完毕，meeting_id:" + str(meeting.id))
        if room_id != 0:
            if meeting.repeat != '':
                dates = get_weekday(meeting.start_date, meeting.end_date, meeting.repeat_date.split('_')[4].split(','))
                result, occupies = check_repeat_occupy(dbs, room_id, meeting.start_time, meeting.end_time, meeting.repeat_date.split('_')[4].split(','), dates=dates)
                if result != 0:
                    delete_meeting(dbs, meeting.id, meeting.create_user)
                    return json.dumps(occupies, ensure_ascii=False), 0
            else:
                dates = [meeting.start_date]

            for mdate in dates:
                add_meeting_bdr(dbs, meeting.id, room_id, mdate, meeting.create_user)
                error_msg = add_booking(dbs, room_id, mdate, meeting.start_time, meeting.end_time)
                if error_msg:
                    delete_meeting(dbs, meeting.id, meeting.create_user)
                    return error_msg, 0
            logger.debug("会议会议室关联添加完毕")
    except Exception as e:
        logger.error(e)
        error_msg = '新增会议失败，请核对后重试'
    return error_msg, meeting.id


def update(dbs, meeting, room_id, old_meeting=None):
    """
    会议更新
    :param dbs:
    :param meeting:
    :param room_id:
    :param old_meeting:
    :return:
    """
    with transaction.manager as tm:
        try:
            rooms = dbs.query(HasMeetBdr).filter(HasMeetBdr.meeting_id == old_meeting.id).all()
            date_time = datetime.now().strftime('%Y-%m-%d')
            if meeting.start_date < date_time or meeting.end_date < date_time:
                error_msg = '该会议已过期'
                return error_msg
            # 删除旧的会议室预定信息
            for room in rooms:
                error_msg = delete_booking(dbs, room.boardroom_id, room.meeting_date, old_meeting.start_time,
                                           old_meeting.end_time)
                if error_msg:
                    tm.abort()
                    return error_msg
                dbs.delete(room)
            # 添加新的会议室预定信息
            if room_id != 0:
                if meeting.repeat != '':
                    dates = get_weekday(meeting.start_date, meeting.end_date, meeting.repeat_date.split('_')[4].split(','))
                    result, occupies = check_repeat_occupy(dbs, room_id, meeting.start_time, meeting.end_time,
                                                           meeting.repeat_date.split('_')[4].split(','), dates=dates)
                    if result != 0:
                        tm.abort()
                        error_msg = json.dumps(occupies, ensure_ascii=False)
                        return error_msg
                else:
                    dates = [meeting.start_date]

                for mdate in dates:
                    add_meeting_bdr(dbs, meeting.id, room_id, mdate, meeting.create_user)
                    error_msg = add_booking(dbs, room_id, mdate, meeting.start_time, meeting.end_time)
                    if error_msg:
                        tm.abort()
                        return error_msg
            dbs.merge(meeting)
        except Exception as e:
            logger.error(e)
            return '修改会议失败，请核对后重试'


def delete_meeting(dbs, meeting_id, user_id):
    """
    删除会议，先判断会议创建者是不是当前用户
    :param dbs:
    :param meeting_id:
    :param user_id:
    :return:
    """
    error_msg = ''
    try:
        with transaction.manager:
            meeting = dbs.query(HasMeeting).filter(HasMeeting.id == meeting_id).filter(
                HasMeeting.create_user == user_id).first()
            rooms = dbs.query(HasMeetBdr).filter(HasMeetBdr.meeting_id == meeting_id).all()
            if not meeting:
                error_msg = '该会议不是该用户创建，请查询后操作。'
            else:
                date_time = datetime.now().strftime('%Y-%m-%d')
                if meeting.start_date < date_time or meeting.end_date < date_time:
                    error_msg = '该会议已过期'
                else:
                    for room in rooms:
                        error_msg = delete_booking(dbs, room.boardroom_id, room.meeting_date, meeting.start_time,
                                                   meeting.end_time)
                        if error_msg:
                            dbs.rollback()
                            return error_msg
                        dbs.delete(room)
                    dbs.delete(meeting)
    except Exception as e:
        logger.error(e)
        error_msg = '删除会议失败，请核对后重试'
    return error_msg


def find_meeting_bdr(dbs, meeting_id):
    """
    获取会议以及会议室关联的名称
    :param dbs:
    :param meeting_id:
    :return:
    """
    meet_bdr = {}
    meeting = dbs.query(HasMeeting, HasMeetBdr.boardroom_id)\
        .outerjoin(HasMeetBdr, HasMeetBdr.meeting_id == HasMeeting.id)\
        .outerjoin(HasBoardroom, HasBoardroom.id == HasMeetBdr.boardroom_id)\
        .filter(HasMeeting.id == meeting_id).first()
    if meeting:
        meet_bdr = {
            'id': meeting.HasMeeting.id,
            'name': meeting.HasMeeting.name,
            'description': meeting.HasMeeting.description,
            'start_date': meeting.HasMeeting.start_date,
            'end_date': meeting.HasMeeting.end_date,
            'start_time': meeting.HasMeeting.start_time,
            'end_time': meeting.HasMeeting.end_time,
            'boardroom_id': meeting.boardroom_id
        }
    return meet_bdr


def find_meeting(dbs, meeting_id):
    """
    获取会议以及会议室关联的名称
    :param dbs:
    :param meeting_id:
    :return:
    """
    meeting = dbs.query(HasMeeting)\
        .filter(HasMeeting.id == meeting_id).first()
    return meeting


def find_rooms(dbs):
    """
    当前用户可以申请的会议室（机构权限过滤）
    :param dbs:
    :return:
    """
    rooms = dbs.query(HasBoardroom).all()
    return rooms


def add_meeting_bdr(dbs, meeting_id, room_id, meeting_date, create_user):
    """

    :param dbs:
    :param meeting_id:
    :param room_id:
    :param meeting_date:
    :param create_user:
    :return:
    """
    meet_bdr = HasMeetBdr()
    meet_bdr.meeting_id = meeting_id
    meet_bdr.boardroom_id = room_id
    meet_bdr.meeting_date = meeting_date
    meet_bdr.create_user = create_user
    meet_bdr.create_time = date_now()
    dbs.add(meet_bdr)


def find_user_period(dbs, start_date, end_date, user_id):
    """
    查看用户可预订期限
    :param dbs:
    :param start_date:
    :param end_date:
    :param user_id:
    :return:
    """
    user = dbs.query(SysUser).filter(SysUser.id == user_id).first()
    error_massage = ''
    max_date = add_date(user.max_period)
    if (start_date > max_date) | (end_date > max_date):
        error_massage = '会议预定时间超出可预订范围！'
    return error_massage
