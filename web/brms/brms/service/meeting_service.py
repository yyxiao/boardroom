#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/8
"""

from datetime import datetime
from ..models.model import *
from ..common.paginator import Paginator
from ..common.dateutils import date_now
from ..service.booking_service import check_occupy, add_booking, update_booking, delete_booking
from ..service.org_service import find_org_ids
import transaction
import logging


logger = logging.getLogger('operator')


def find_meetings(dbs, meeting_name=None, create_user=None, user_org_id=None, room_name=None, start_date=None, end_date=None,
                  page_no=1, page_size=10, org_id=None, room_id=None):
    """
    会议列表
    :param dbs:
    :param meeting_name:
    :param create_user:
    :param user_org_id:
    :param room_name:
    :param start_date:
    :param end_date:
    :param page_no:
    :param page_size:
    :param org_id:
    :param room_id:
    :return:
    """
    branches = find_org_ids(dbs, user_org_id)               # 获取当前用户所属机构及下属机构id
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
        .outerjoin(SysOrg, SysUser.org_id == SysOrg.id)\
        .outerjoin(HasMeetBdr, HasMeetBdr.meeting_id == HasMeeting.id)\
        .outerjoin(HasBoardroom, HasBoardroom.id == HasMeetBdr.boardroom_id)\
        .outerjoin(HasPad, HasPad.id == HasBoardroom.pad_id)
    if meeting_name:
        meetings = meetings.filter(HasMeeting.name.like('%'+meeting_name+'%'))
    if create_user:
        meetings = meetings.filter(HasMeeting.create_user == create_user)
    if user_org_id and branches:
        meetings = meetings.filter(SysOrg.id.in_(branches))
    if start_date:
        meetings = meetings.filter(HasMeeting.start_date >= start_date)
    if end_date:
        meetings = meetings.filter(HasMeeting.end_date <= end_date)
    if room_name:
        meetings = meetings.filter(HasBoardroom.name.like('%' + room_name + '%'))
    if room_id:
        meetings = meetings.filter(HasMeetBdr.boardroom_id == room_id)
    if not room_id and org_id:
        meetings = meetings.filter(HasMeeting.org_id == org_id)

    user_list = meetings.order_by(HasMeeting.create_time.desc())
    results, paginator = Paginator(user_list, page_no, page_size).to_dict()
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
        room_name = obj[9] if obj[9] else ''
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
            'room_name': room_name
        }
        lists.append(temp_dict)
    return lists, paginator


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
            meet_bdr = HasMeetBdr()  # 会议室会议关联信息
            meet_bdr.meeting_id = meeting.id
            meet_bdr.boardroom_id = room_id
            meet_bdr.create_user = meeting.create_user
            meet_bdr.create_time = date_now()
            dbs.add(meet_bdr)
            error_msg = add_booking(dbs, room_id, meeting.start_date, meeting.start_time, meeting.end_time)
            if error_msg:
                delete_meeting(dbs, meeting.id, meeting.create_user)
                return error_msg
            logger.debug("会议会议室关联添加完毕")
    except Exception as e:
        logger.error(e)
        error_msg = '新增会议失败，请核对后重试'
    return error_msg


def update(dbs, meeting, room_id, old_meeting=None):
    """
    PAD更新会议
    :param dbs:
    :param meeting:
    :param room_id:
    :param old_meeting:
    :return:
    """
    with transaction.manager:
        try:
            # 查询meeting_id对应的boardroom_id
            meet_bdr = dbs.query(HasMeetBdr)\
                .filter(HasMeetBdr.meeting_id == meeting.id).first()
            if not meet_bdr:                                       # 不存在
                meet_bdr = HasMeetBdr()  # 会议室会议关联信息
                meet_bdr.meeting_id = meeting.id
                meet_bdr.boardroom_id = room_id
                meet_bdr.create_user = meeting.create_user
                create_time = date_now()
                meet_bdr.create_time = create_time
                dbs.add(meet_bdr)
                error_msg = add_booking(dbs, room_id, meeting.start_date, meeting.start_time, meeting.end_time)
                if error_msg:
                    dbs.query(HasMeetBdr).filter(HasMeetBdr.meeting_id == meeting.id,
                                                 HasMeetBdr.boardroom_id == room_id,
                                                 HasMeetBdr.create_time == create_time).delete()
                    return error_msg
            else:
                # 更新会议
                dbs.add(meeting)
                # dbs.flush()
                old_room_id = meet_bdr.boardroom_id
                meet_bdr.boardroom_id = room_id
                dbs.add(meet_bdr)
                error_msg = update_booking(dbs, old_room_id, room_id, old_meeting, meeting)
                if error_msg:
                    dbs.rollback()
                logger.debug("会议更新完毕，meeting_id:" + str(meeting.id))
        except Exception as e:
            logger.error(e)
            dbs.rollback()
            error_msg = '更新会议失败，请核对后重试'
    return error_msg


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
            meeting = dbs.query(HasMeeting).filter(HasMeeting.id == meeting_id).filter(HasMeeting.create_user == user_id).first()
            room = dbs.query(HasMeetBdr).filter(HasMeetBdr.meeting_id == meeting_id).first()
            if not meeting:
                error_msg = '该会议不是该用户创建，请查询后操作。'
            else:
                error_msg = delete_booking(dbs, room.boardroom_id, meeting.start_date, meeting.start_time, meeting.end_time)
                if error_msg:
                    dbs.rollback()
                    return error_msg
                dbs.delete(meeting)
                dbs.delete(room)
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
            'end_time': meeting.HasMeeting.end_time
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
