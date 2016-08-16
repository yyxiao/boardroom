#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/11
"""
import base64
import transaction
from pyramid.view import view_config

from ..models.model import *
from ..common.dateutils import date_now
from ..service.loginutil import UserTools
from ..service.pad_service import find_pad_by_id, find_meetings, update_last_time
from ..service.meeting_service import add_by_pad, delete_meeting, update_by_pad
from ..service.user_service import user_checking


@view_config(route_name='padLogin', renderer='json')
def pad_login(request):
    """
    设备初始化登录
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_account = request.POST.get('user_account', '')
    pad_code = request.POST.get('pad_code', '')
    password = base64.encodebytes(request.params['password'].encode()).decode('utf-8').replace('\n', '')
    error_msg = ''
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
                pad, error_msg = find_pad_by_id(dbs, pad_code, user.id)
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
    error_msg = ''
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
    error_msg = ''
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
        meeting.name = request.POST.get('meeting_name', '')
        meeting.description = request.POST.get('description', '')
        meeting.start_date = request.POST.get('start_date', '')
        meeting.end_date = request.POST.get('end_date', '')
        meeting.start_time = request.POST.get('start_time', '')
        meeting.end_time = request.POST.get('end_time', '')
        meeting.create_user = user_id
        meeting.create_time = date_now()
        error_msg = add_by_pad(dbs, meeting, pad_code)
    update_last_time(dbs, pad_code, 'addMeeting')
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
    dbs = request.dbsession
    user_id = request.POST.get('user_id', '')
    meeting_id = request.POST.get('meeting_id', '')
    pad_code = request.POST.get('pad_code', '')
    if not user_id:
        error_msg = '用户ID不能为空！'
    elif not pad_code:
        error_msg = '终端编码不能为空！'
    elif not meeting_id:
        error_msg = '会议ID不能为空！'
    else:
        meeting = dbs.query(HasMeeting).filter(HasMeeting.id == meeting_id)\
            .filter(HasMeeting.create_user == user_id).first()
        if not meeting:
            error_msg = '未查找到该会议记录，请查看会议ID、用户ID是否正确！'
        else:
            meeting.name = request.POST.get('meeting_name', '')
            meeting.description = request.POST.get('description', '')
            meeting.start_date = request.POST.get('start_date', '')
            meeting.end_date = request.POST.get('end_date', '')
            meeting.start_time = request.POST.get('start_time', '')
            meeting.end_time = request.POST.get('end_time', '')
            meeting.create_time = date_now()
            error_msg = update_by_pad(dbs, meeting, pad_code)
    update_last_time(dbs, pad_code, 'updateMeeting')
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
