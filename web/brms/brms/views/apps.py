#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/11
"""
import base64
from pyramid.view import view_config
from ..common.jsonutils import serialize
from ..service.loginutil import UserTools
from ..service.pad_service import *
from ..service.meeting_service import delete_meeting, find_meeting
from ..service.user_service import user_checking
import transaction


@view_config(route_name='padLogin', renderer='json')
def pad_login(request):
    """
    设备初始化登录
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_id = request.POST.get('user_id', '')
    pad_code = request.POST.get('pad_code', '')
    if not pad_code:
        error_msg = '终端编码不能为空'
    elif not user_id:
        error_msg = '用户ID不能为空'
    else:
        with transaction.manager:
            user = dbs.query(SysUser).filter(SysUser.id == user_id).first()
            if not user:
                error_msg = '用户不存在'
            else:
                pad, error_msg = find_pad_by_id(dbs, pad_code, user.id, user.org_id)
    update_last_time(dbs, pad_code, 'padLogin')
    if error_msg:
        json_a = {
            'success': 'false',
            'error_msg': error_msg,
        }
    else:
        json_a = {
            'success': 'true',
            'pad': pad
        }
    return json_a


@view_config(route_name='userCheck', renderer='json')
def user_check(request):
    """
    验证用户是否可以使用该pad申请会议
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_account = request.POST.get('user_account', '')
    pad_code = request.POST.get('pad_code', '')
    password = base64.encodebytes(request.POST.get('password', '').encode()).decode('utf-8').replace('\n', '')
    if not pad_code:
        error_msg = '终端编码不能为空'
    elif not user_account:
        error_msg = '用户账号不能为空'
    else:
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
                max_period = user.max_period
                user_id = user.id
                error_msg = user_checking(dbs, pad_code, user.id)
    update_last_time(dbs, pad_code, 'userCheck')
    if error_msg:
        json_a = {
            'success': 'false',
            'error_msg': error_msg,
        }
    else:
        json_a = {
            'success': 'true',
            'user_id': user_id,
            'max_period': max_period
        }
    return json_a


@view_config(route_name='meetingList', renderer='json')
def meeting_list(request):
    """
    会议list
    :param request:
    :return:
    """
    dbs = request.dbsession
    pad_code = request.POST.get('pad_code', '')
    if not pad_code:
        error_msg = '终端编码不能为空'
    else:
        meetings, error_msg = find_meetings(dbs, pad_code)
    update_last_time(dbs, pad_code, 'meetingList')
    if error_msg:
        json_a = {
            'success': 'false',
            'error_msg': error_msg,
        }
    else:
        json_a = {
            'success': 'true',
            'meeting': meetings
        }
    return json_a


@view_config(route_name='app_index', renderer='json')
def index(request):
    """
    :return:
    """
    json_a = {
        'success': 'true',
    }
    return json_a


@view_config(route_name='pad_add_meeting', renderer='json')
def pad_add_meeting(request):
    dbs = request.dbsession
    meeting = HasMeeting()
    user_id = request.POST.get('user_id', '')
    pad_code = request.POST.get('pad_code', '')
    if not user_id:
        error_msg = '用户ID不能为空！'
    elif not pad_code:
        error_msg = '终端编码不能为空'
    else:
        user = dbs.query(SysUser).filter(SysUser.id == user_id).first()
        meeting.name = request.POST.get('meeting_name', '')
        meeting.description = request.POST.get('description', '')
        meeting.start_date = request.POST.get('start_date', '')
        meeting.end_date = request.POST.get('end_date', '')
        meeting.start_time = request.POST.get('start_time', '')
        meeting.end_time = request.POST.get('end_time', '')
        meeting.org_id = user.org_id
        meeting.create_user = user_id
        meeting.create_time = date_now()
        error_msg, meeting_id = add_by_pad(dbs, meeting, pad_code)
    update_last_time(dbs, pad_code, 'addMeeting')
    if error_msg:
        json = {
            'success': 'false',
            'error_msg': error_msg,
        }
    else:
        meeting_dict = pad_find_meeting(dbs, meeting_id)
        json = {
            'success': 'true',
            'meeting': meeting_dict
        }
    return json


@view_config(route_name='pad_del_meeting', renderer='json')
def del_meeting(request):
    dbs = request.dbsession
    user_id = request.POST.get('user_id', '')
    pad_code = request.POST.get('pad_code', '')
    meeting_id = request.POST.get('meeting_id', '')
    if not user_id:
        error_msg = '用户id不能为空'
    elif not meeting_id:
        error_msg = '会议id不能为空'
    elif not pad_code:
        error_msg = '终端编码不能为空'
    else:
        error_msg = delete_meeting(dbs, meeting_id, user_id)
    update_last_time(dbs, pad_code, 'delMeeting')
    if error_msg:
        json = {
            'success': 'false',
            'error_msg': error_msg,
        }
    else:
        json = {
            'success': 'true',
        }
    return json


@view_config(route_name='pad_update_meeting', renderer='json')
def pad_update_meeting(request):
    """
    更新会议
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_id = request.POST.get('user_id', '')
    meeting_id = request.POST.get('meeting_id', '')
    pad_code = request.POST.get('pad_code', '')
    update_last_time(dbs, pad_code, 'updateMeeting')
    if not user_id:
        error_msg = '用户ID不能为空！'
    elif not pad_code:
        error_msg = '终端编码不能为空！'
    elif not meeting_id:
        error_msg = '会议ID不能为空！'
    else:
        meeting = find_meeting(dbs, meeting_id)
        if not meeting:
            error_msg = '未查找到该会议记录，请查看会议ID、用户ID是否正确！'
        else:
            if str(meeting.create_user) != user_id:
                error_msg = '该会议不是该用户创建，请查询后操作。'
            else:
                # 临时保存历史会议
                old_meeting = HasMeeting()
                old_meeting.start_date = meeting.start_date
                old_meeting.start_time = meeting.start_time
                old_meeting.end_date = meeting.end_date
                old_meeting.end_time = meeting.end_time

                meeting.name = request.POST.get('meeting_name', '')
                meeting.description = request.POST.get('description', '')
                meeting.start_date = request.POST.get('start_date', '')
                meeting.end_date = request.POST.get('end_date', '')
                meeting.start_time = request.POST.get('start_time', '')
                meeting.end_time = request.POST.get('end_time', '')
                meeting.create_time = date_now()
                error_msg = update_by_pad(dbs, meeting, pad_code, old_meeting=old_meeting)
    if error_msg:
        json = {
            'success': 'false',
            'error_msg': error_msg,
        }
    else:
        meeting_dict = pad_find_meeting(dbs, meeting_id)
        json = {
            'success': 'true',
            'meeting': meeting_dict
        }
    return json


@view_config(route_name='pad_org_list', renderer='json')
def pad_org_list(request):
    """
    机构列表
    :param request:
    :return:
    """
    error_msg = ''
    dbs = request.dbsession
    user_id = request.POST.get('user_id', '')
    pad_code = request.POST.get('pad_code', '')
    if not user_id:
        error_msg = '用户ID不能为空！'
    elif not pad_code:
        error_msg = '终端编码不能为空！'
    else:
        orgs = pad_find_orgs(dbs, user_id)
    update_last_time(dbs, pad_code, 'orgList')
    if error_msg:
        json = {
            'success': 'false',
            'error_msg': error_msg,
        }
    else:
        json = {
            'success': 'true',
            'orgs': orgs
        }
    return json


@view_config(route_name='pad_set_room', renderer='json')
def pad_set_room(request):
    """
    pad修改关联会议室
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_id = request.POST.get('user_id', '')
    room_id = request.POST.get('room_id', '')
    pad_code = request.POST.get('pad_code', '')
    if not user_id:
        error_msg = '用户ID不能为空！'
    elif not pad_code:
        error_msg = '终端编码不能为空！'
    elif not room_id:
        error_msg = '会议室ID不能为空！'
    else:
        room, error_msg = set_room(dbs, user_id, pad_code, room_id)
        room = serialize(room)
    update_last_time(dbs, pad_code, 'setRoom')
    if error_msg:
        json = {
            'success': 'false',
            'error_msg': error_msg,
        }
    else:
        json = {
            'success': 'true',
            'room': room
        }
    return json


@view_config(route_name='pad_qr_code', renderer='json')
def pad_qr_code(request):
    """
    设备初始化登录
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_id = request.POST.get('user_id', '')
    pad_code = request.POST.get('pad_code', '')
    room_id = request.POST.get('room_id', '')
    if not pad_code:
        error_msg = '终端编码不能为空'
    elif not user_id:
        error_msg = '用户ID不能为空'
    elif not room_id:
        error_msg = '会议室ID不能为空'
    else:
        room, error_msg = set_rooms_by_qrcode(dbs, user_id, pad_code, room_id)
        room = serialize(room)
    update_last_time(dbs, pad_code, 'padQrCode')
    if error_msg:
        json_a = {
            'success': 'false',
            'error_msg': error_msg,
        }
    else:
        json_a = {
            'success': 'true',
            'room': room
        }
    return json_a
