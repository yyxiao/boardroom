#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-18
"""

import transaction
import logging
from functools import reduce
from ..common.dateutils import get_weekday
from ..models.model import *

logger = logging.getLogger(__name__)


def check_occupy(dbs, room_id, mdate, start_time, end_time):
    """
    检查给定时间范围内是否已经有被预约过
    :param room_id:
    :param mdate:
    :param start_time:
    :param end_time:
    :return:
    """

    occupy = dbs.query(HasRoomOccupy).filter(HasRoomOccupy.room_id == room_id,
                                             HasRoomOccupy.date == mdate).first()
    if occupy:
        if occupy.code:
            binary = get_binary(start_time, end_time)
            result, flag = compare_bin(binary, occupy.code)
            if not result:
                return '开始时间冲突' if flag < 0 else ('结束时间冲突' if flag > 0 else '全部时间冲突')
    return ''


def add_booking(dbs, room_id, mdate, start_time, end_time):
    """
    添加会议室占用情况
    :param dbs:
    :param room_id:
    :param mdate:
    :param start_time:
    :param end_time:
    :return:
    """

    if room_id == 0:
        return ''
    occupy = dbs.query(HasRoomOccupy).filter(HasRoomOccupy.room_id == room_id,
                                             HasRoomOccupy.date == mdate).first()
    if not occupy:
        occupy = HasRoomOccupy()
        occupy.room_id = room_id
        occupy.date = mdate
        occupy.code = get_binary(start_time, end_time)
    else:
        result, flag = compare_bin(get_binary(start_time, end_time), occupy.code)
        if result == 0:
            return '时间冲突，添加失败'
        occupy.code = result

    try:
        # with transaction.manager:
        dbs.add(occupy)
        # dbs.flush()
        return ''
    except Exception as e:
        logger.error(e)
        return '添加占用失败'


def update_booking(dbs, old_room_id, new_room_id, old_meeting, new_meeting):
    """
    更新会议预定
    :param dbs:
    :param old_room_id:
    :param new_room_id:
    :param old_meeting:
    :param new_meeting:
    :return:
    """

    occupy = None
    if old_room_id != 0:
        occupy = dbs.query(HasRoomOccupy).filter(HasRoomOccupy.room_id == old_room_id,
                                                 HasRoomOccupy.date == old_meeting.start_date).first()
        if occupy:
            old_bin = get_binary(old_meeting.start_time, old_meeting.end_time)
            tmp = delete_bin(old_bin, occupy.code)
            occupy.code = tmp

    if new_room_id != 0:
        m_bin = get_binary(new_meeting.start_time, new_meeting.end_time)
        if old_room_id == new_room_id and old_meeting.start_date == new_meeting.start_date and occupy:
            br_bin = occupy.code
        else:
            occupy = dbs.query(HasRoomOccupy).filter(HasRoomOccupy.room_id == new_room_id,
                                                     HasRoomOccupy.date == new_meeting.start_date).first()
            if occupy:
                br_bin = occupy.code
            else:
                occupy = HasRoomOccupy()
                occupy.room_id = new_room_id
                occupy.date = new_meeting.start_date
                br_bin = 0

        result, flag = compare_bin(m_bin, br_bin)
        if result == 0:
            return '时间冲突，添加失败'
        occupy.code = result
        dbs.add(occupy)
        return ''


def delete_booking(dbs, room_id, mdate, start_time, end_time):
    """
    删除占用
    :param dbs:
    :param room_id:
    :param mdate:
    :param start_time:
    :param end_time:
    :return:
    """
    occupy = dbs.query(HasRoomOccupy).filter(HasRoomOccupy.room_id == room_id,
                                             HasRoomOccupy.date == mdate).first()
    if not occupy:
        return ''
    else:
        occupy.code = delete_bin(get_binary(start_time, end_time), occupy.code)

    try:
        # with transaction.manager:
        if occupy.code == 0:
            dbs.delete(occupy)
        else:
            dbs.merge(occupy)
        # dbs.flush()
        return ''
    except Exception as e:
        logger.error(e)
        return '删除占用失败'


def check_repeat_occupy(dbs, room_id, start_time, end_time, week_nums, start_date=None, end_date=None, dates=None, repeat=None):
    """
    检查重复会议是否冲突
    :param dbs:
    :param room_id:
    :param start_time:
    :param end_time:
    :param week_nums:
    :param start_date:
    :param end_date:
    :param dates:
    :param repeat:
    :return:   result: 0      没有冲突
                       other  有
               occupies:      冲突日期及冲突信息字典
    """
    if not dates:
        dates = get_weekday(start_date, end_date, week_nums, repeat)
    occupies = {}
    for mdate in dates:
        msg = check_occupy(dbs, room_id, mdate, start_time, end_time)
        if msg:
            occupies[mdate] = msg
    result = len(occupies)
    return result, occupies


def add_repeat_booking(dbs, room_id, start_time, end_time, week_num, start_date, end_date, dates=None, repeat=None):
    """
    添加重复会议
    :param dbs:
    :param room_id:
    :param start_time:
    :param end_time:
    :param week_num:
    :param start_date:
    :param end_date:
    :param dates:
    :param repeat:
    :return:
    """

    if not dates:
        dates = get_weekday(start_date, end_date, week_num, repeat)

    result, occupies = check_repeat_occupy(dbs, room_id, start_time, end_time, week_num, dates=dates, repeat=repeat)
    if result != 0:
        result = '会议室预约有冲突'
        return result, occupies
    else:
        try:
            for mdate in dates:
                msg = add_booking(dbs, room_id, mdate, start_time, end_time)
                if msg:
                    return msg, None
            return '', None
        except Exception as e:
            logger.error(e)
            return '添加会议室预约失败'


def compare_bin(mt_bin, br_bin):
    """
    比较二进制判断是否有重复
    :param mt_bin: 会议时间范围对应二进制数
    :param br_bin: 会议室已占用时间范围二进制数
    :return: result: 0 有冲突, 此时flag才有意义;
                     other 新的二进制数;
             flag:   -1 开始时间冲突;
                     0 全部时间冲突;
                     1 结束时间冲突;
    """
    if isinstance(mt_bin, str):
        mt_bin = int(mt_bin)
    if isinstance(br_bin, str):
        br_bin = int(br_bin)

    if br_bin == 0:
        return mt_bin, 0

    flag = mt_bin & br_bin
    result = 0
    if mt_bin == br_bin or flag == mt_bin or flag == br_bin:
        flag = 0
    elif flag:
        if flag < mt_bin < br_bin:
            flag = 1
        elif flag < br_bin < mt_bin:
            flag = -1
    else:
        result = mt_bin | br_bin
    return result, flag


def delete_bin(mt_bin, br_bin):
    """
    删除会议时,清除此会议的占用值
    :param mt_bin:
    :param br_bin:
    :return:
    """

    result, flag = compare_bin(mt_bin, br_bin)
    return (mt_bin ^ br_bin) if result == 0 and flag == 0 else br_bin


def get_binary(start_time, end_time, start=7, hours=14):
    """
    根据时间范围生成梳型二进制数对应整形数
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param start: 允许预订的最早时间
    :param hours: 允许预订的时间长度
    :return: -1: 超出时间范围, other int:
    """

    s_h, s_m = start_time.split(':')
    e_h, e_m = end_time.split(':')

    left = (int(s_h) - start) * 2 + (int(s_m) // 30)
    right = (int(e_h) - start) * 2 + (int(e_m) // 30)

    if left < 0 or (right > hours * 2):
        return -1

    binary = reduce((lambda x, y: x + 2 ** y), range(left, right), 0)
    return binary


def find_orgs(dbs, user_id, org_ids=None, room_id=None, show_child=False):
    """
    机构会议室树
    :param dbs:
    :param user_id:
    :param org_ids:
    :param room_id:
    :param show_child:
    :return:
    """
    orgs = dbs.query(SysOrg.id, SysOrg.org_name, SysOrg.parent_id)
    if room_id:
        orgs = orgs.outerjoin(HasBoardroom, SysOrg.id == HasBoardroom.org_id)\
            .filter(HasBoardroom.id == room_id)
    elif org_ids and len(org_ids) > 0:
        orgs = orgs.filter(SysOrg.id.in_(org_ids))
    else:
        orgs = orgs.outerjoin(SysUser, SysUser.org_id == SysOrg.id)\
            .filter(SysUser.id == user_id)

    rooms = dbs.query(HasBoardroom.id, HasBoardroom.name, HasBoardroom.org_id)
    if room_id:
        rooms = rooms.filter(HasBoardroom.id == room_id)
    elif org_ids and len(org_ids) > 0:
        rooms = rooms.outerjoin(SysOrg, SysOrg.id == HasBoardroom.org_id)\
            .filter(SysOrg.id.in_(org_ids))
    else:
        rooms = rooms.outerjoin(SysOrg, SysOrg.id == HasBoardroom.org_id) \
            .outerjoin(SysUser, SysUser.org_id == SysOrg.id) \
            .filter(SysUser.id == user_id)

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
                    'key': room.id,
                    'label': room.name
                }
                room_list.append(room_dict)
        temp_dict = {
            'org_id': org_id,
            'label': org_name,
            'open': True,
            'children': room_list
        }
        lists.append(temp_dict)
    return lists
