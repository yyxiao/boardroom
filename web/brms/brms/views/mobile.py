#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/31
"""
import base64
from pyramid.view import view_config
from ..common.dateutils import date_now
from ..common.jsonutils import serialize
from ..common.password import get_password, DEFAULT_PASSWORD
from ..service.loginutil import UserTools
from ..service.mobile_service import *
from ..service.meeting_service import delete_meeting, find_meeting, find_user_period
from ..service.user_service import find_user_by_id, update
import transaction

logger = logging.getLogger('operator')


@view_config(route_name='mobile_login', renderer='json')
def mobile_login(request):
    error_msg = ''
    dbs = request.dbsession
    user_account = request.POST.get('user_account', '')
    password = base64.encodebytes(request.POST.get('password', '').encode()).decode('utf-8').replace('\n', '')
    logger.info('mobile_login--user_account:' + user_account)
    with transaction.manager:
        user = dbs.query(SysUser).filter(SysUser.user_account == user_account).first()
        if not user:
            error_msg = '用户不存在'
        elif password != user.user_pwd:
            error_msg = '密码错误'
            UserTools.count_err(user)
            dbs.flush()
        else:
            # 获取该用户最大可申请期限
            org_rooms = find_org_rooms(dbs, user.id)
    if error_msg:
        json_a = {
            'status': 'false',
            'error_msg': error_msg,
        }
    else:
        json_a = {
            'status': 'true',
            'org_rooms': org_rooms,
            'user': {
                "id": user.id,
                "org_id": user.org_id,
                "position": user.position if user.position else '',
                "email": user.email if user.email else '',
                "user_name": user.user_name if user.user_name else '',
                "address": user.address if user.address else '',
                'max_period': user.max_period if user.max_period else 0,
                "phone": user.phone if user.phone else ''
            }
        }
    return json_a


@view_config(route_name='mobile_update_user', renderer='json')
def mobile_update_user(request):
    error_msg = ''
    dbs = request.dbsession
    user_id = request.POST.get('user_id', 0)
    user = find_user_by_id(dbs, user_id)
    logger.info('mobile_update_user--user_id:' + user_id)
    if user.user_pwd != get_password(request.POST.get('passwd_old', '')):
        msg = '原密码错误！'
    else:
        if request.POST.get('passwd_new'):
            user.user_pwd = get_password(request.POST.get('passwd_new', ''))
        if request.POST.get('user_name'):
            user.user_name = request.POST.get('user_name', '')
        if request.POST.get('phone'):
            user.phone = request.POST.get('phone', '')
        if request.POST.get('address'):
            user.address = request.POST.get('address', '')
        if request.POST.get('email'):
            user.email = request.POST.get('email', '')
        if request.POST.get('position'):
            user.position = request.POST.get('position', '')

        org_id = request.POST.get('org_id', 0)
        role_id = request.POST.get('role_id', 0)
        user.update_time = date_now()
        error_msg = update(dbs, user, role_id, org_id, user_id)
    if error_msg:
        json_a = {
            'status': 'false',
            'error_msg': error_msg,
        }
    else:
        json_a = {
            'status': 'true',
            'user': {
                "id": user.id,
                "org_id": user.org_id,
                "position": user.position if user.position else '',
                "email": user.email if user.email else '',
                "user_name": user.user_name if user.user_name else '',
                "address": user.address if user.address else '',
                'max_period': user.max_period if user.max_period else 0,
                "phone": user.phone if user.phone else ''
            }
        }
    return json_a


@view_config(route_name='mobile_meeting_list', renderer='json')
def mobile_meeting_list(request):
    error_msg = ''
    dbs = request.dbsession
    user_id = request.POST.get('user_id', '')
    room_id = request.POST.get('room_id', '')
    logger.info('mobile_meeting_list--user_id:' + user_id + ',room_id:' + room_id)
    if not user_id:
        error_msg = '用户ID不能为空！'
    elif not room_id:
        error_msg = '会议室ID不能为空！'
    else:
        meetings = mob_find_meetings(dbs, user_id, room_id)
    if error_msg:
        json_a = {
            'status': 'false',
            'error_msg': error_msg,
        }
    else:
        json_a = {
            'status': 'true',
            'meetings': meetings
        }
    return json_a


@view_config(route_name='mobile_room_list', renderer='json')
def mobile_room_list(request):
    error_msg = ''
    dbs = request.dbsession
    user_id = request.POST.get('user_id', '')
    logger.info('mobile_room_list--user_id:' + user_id)
    if not user_id:
        error_msg = '用户ID不能为空！'
    else:
        rooms = mob_find_boardrooms(dbs, user_id)
    if error_msg:
        json_a = {
            'status': 'false',
            'error_msg': error_msg,
        }
    else:
        json_a = {
            'status': 'true',
            'rooms': rooms
        }
    return json_a
