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