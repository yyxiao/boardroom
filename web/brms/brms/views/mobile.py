#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/31
"""
import base64
from pyramid.view import view_config
from pyramid.response import Response
from ..common.dateutils import date_now, datetime_format, date_pattern1
from ..common.jsonutils import serialize
from ..common.password import get_password, DEFAULT_PASSWORD
from ..service.loginutil import UserTools
from ..service.mobile_service import *
from ..service.meeting_service import add, find_user_period, find_meeting
from ..service.user_service import find_user_by_id, update

logger = logging.getLogger(__name__)


@view_config(route_name='mobile_login', renderer='json')
def mobile_login(request):
    """
    登录
    :param request:
    :return:
    """
    error_msg = ''
    dbs = request.dbsession
    user_account = request.POST.get('user_account', '')
    meeting_date = request.POST.get('meeting_date', datetime.now().strftime(date_pattern1))
    password = request.POST.get('password', '')   # base64.encodebytes(request.POST.get('password', '').encode()).decode('utf-8').replace('\n', '')
    logger.info('mobile_login--user_account:' + user_account)
    user = dbs.query(SysUser).filter(SysUser.user_account == user_account).first()
    if not user:
        error_msg = '用户不存在'
    elif password != user.user_pwd:
        error_msg = '密码错误'
        UserTools.count_err(user)
        dbs.flush()
    else:
        # 获取该用户最大可申请期限
        org_rooms = find_org_rooms(dbs, user.id, meeting_date)
    if error_msg:
        json_a = {
            'status': 'false',
            'error_msg': error_msg,
        }
    else:
        json_a = {
            'status': 'true',
            'error_msg': error_msg,
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
    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.json = json_a
    return resp


@view_config(route_name='mobile_update_user', renderer='json')
def mobile_update_user(request):
    error_msg = ''
    dbs = request.dbsession
    user_id = request.POST.get('user_id', 0)
    if user_id == 1:
        return {
            'status': 'false',
            'error_msg': '无权修改此用户信息！'
        }
    user = find_user_by_id(dbs, user_id)
    logger.info('mobile_update_user--user_id:' + user_id)
    if user.user_pwd != get_password(request.POST.get('passwd_old', '')):
        error_msg = '原密码错误！'
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
            'error_msg': error_msg,
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
    """
    获取会议列表
    :param request:
    :return:
    """
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
            'error_msg': error_msg,
            'meetings': meetings
        }
    return json_a


@view_config(route_name='mobile_room_list', renderer='json')
def mobile_room_list(request):
    """
    获取会议室列表
    :param request:
    :return:
    """
    error_msg = ''
    dbs = request.dbsession
    user_id = request.POST.get('user_id', '')
    org_id = request.POST.get('org_id', '')
    logger.info('mobile_room_list--user_id:' + user_id)
    if not user_id:
        error_msg = '用户ID不能为空！'
    else:
        rooms = mob_find_boardrooms(dbs, user_id, org_id)
    if error_msg:
        json_a = {
            'status': 'false',
            'error_msg': error_msg,
        }
    else:
        json_a = {
            'status': 'true',
            'error_msg': error_msg,
            'rooms': rooms
        }
    return json_a


@view_config(route_name='mobile_add_meeting', renderer='json')
def mobile_add_meeting(request):
    """
    手机端添加会议
    :param request:
    :return:
    """

    dbs = request.dbsession
    user_id = request.POST.get('user_id', '')
    meeting = HasMeeting()

    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    room_id = request.POST.get('room_id')
    meeting_id = ''
    if start_date and end_date:
        meeting.name = request.POST.get('meeting_name', '')
        meeting.description = request.POST.get('description', '')
        meeting.start_date = start_date[0:10]
        meeting.start_time = start_date[11:16]
        meeting.end_date = end_date[0:10]
        meeting.end_time = end_date[11:16]

        org_id = dbs.query(SysUser.org_id).filter(SysUser.id == user_id)
        meeting.org_id = org_id
        meeting.repeat = ''
        meeting.repeat_date = ''
        meeting.create_user = user_id
        meeting.create_time = datetime.now().strftime(datetime_format)
        error_msg = find_user_period(dbs, meeting.start_date, meeting.end_date, meeting.create_user)
        if not error_msg:
            error_msg, meeting_id = add(dbs, meeting, room_id)
    else:
        error_msg = '开始时间和结束时间不能为空'
    if error_msg:
        json_str = {
            'status': False,
            'meeting': '',
            'error_msg': error_msg
        }
    else:
        meeting_dict = mob_find_meeting(dbs, meeting_id)
        json_str = {
            'status': True,
            'meeting': meeting_dict,
            'error_msg': ''
        }
    return json_str


@view_config(route_name='mobile_update_meeting', renderer='json')
def mobile_update_meeting(request):
    """
    手机端更新会议
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_id = int(request.POST.get('user_id', 0))
    meeting_id = int(request.POST.get('meeting_id', 0))
    meeting = find_meeting(dbs, meeting_id)

    if meeting.repeat_date:
        error_msg = '重复会议不可修改，请到pc端修改！'
    else:
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        room_id = request.POST.get('room_id')
        meeting_id = ''
        if start_date and end_date:
            meeting.name = request.POST.get('meeting_name', '')
            meeting.description = request.POST.get('description', '')
            meeting.start_date = start_date[0:10]
            meeting.start_time = start_date[11:16]
            meeting.end_date = end_date[0:10]
            meeting.end_time = end_date[11:16]

            error_msg = find_user_period(dbs, meeting.start_date, meeting.end_date, user_id)
            if not error_msg:
                error_msg, meeting_id = add(dbs, meeting, room_id)
        else:
            error_msg = '开始时间和结束时间不能为空'
    if error_msg:
        json_str = {
            'status': False,
            'meeting': '',
            'error_msg': error_msg
        }
    else:
        meeting_dict = mob_find_meeting(dbs, meeting_id)
        json_str = {
            'status': True,
            'meeting': meeting_dict,
            'error_msg': ''
        }
    return json_str


@view_config(route_name='mobile_user_meeting_list', renderer='json')
def mobile_user_meeting_list(request):
    """
    返回用户会议列表
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_id = request.POST.get('user_id', '')
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    error_msg = ''
    if not user_id:
        error_msg = '用户ID不能为空！'
    elif not start_date:
        error_msg = '开始时间不能为空！'
    elif not end_date:
        error_msg = '结束时间不能为空！'
    else:
        meetings = mob_find_user_meetings(dbs, user_id, start_date, end_date)
    if error_msg:
        json_str = {
            'status': False,
            'meeting': '',
            'error_msg': error_msg
        }
    else:
        json_str = {
            'status': True,
            'meeting': meetings,
            'error_msg':error_msg
        }
    return json_str


@view_config(route_name='mobile_org_meeting_list', renderer='json')
def mobile_org_meeting_list(request):
    """
    返回机构会议列表
    :param request:
    :return:
    """
    dbs = request.dbsession
    org_id = request.POST.get('org_id', '')
    meeting_date = request.POST.get('meeting_date', '')
    error_msg = ''
    if not org_id:
        error_msg = '机构ID不能为空！'
    elif not meeting_date:
        error_msg = '会议时间不能为空！'
    else:
        rooms = mob_find_org_meetings(dbs, org_id, meeting_date)
    if error_msg:
        json_str = {
            'status': False,
            'rooms': '',
            'error_msg': error_msg
        }
    else:
        json_str = {
            'status': True,
            'rooms': rooms,
            'error_msg':error_msg
        }
    return json_str


@view_config(route_name='mobile_delete_meeting', renderer='json')
def mobile_delete_meeting(request):
    dbs = request.dbsession
    user_id = request.POST.get('user_id', '')
    meeting_id = request.POST.get('meeting_id', '')
    if not user_id:
        error_msg = '用户id不能为空'
    elif not meeting_id:
        error_msg = '会议id不能为空'
    else:
        error_msg = delete_meeting(dbs, meeting_id, user_id)
    logger.info('delMeeting--user_id:' + user_id + ',meeting_id:' + meeting_id)
    if error_msg:
        json = {
            'status': False,
            'error_msg': error_msg
        }
    else:
        json = {
            'status': True,
            'error_msg':error_msg
        }
    resp = Response()
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.json = json
    return resp
