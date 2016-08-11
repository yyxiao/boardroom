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
from ..common.jsonutils import serialize
from ..service.loginutil import UserTools
from ..service.pad_service import find_pad_by_id, find_meetings
from ..service.user_service import user_checking


@view_config(route_name='padLogin', renderer='json')
def pad_login(request):
    """
    设备初始化登录
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_account = request.params['userAccount']
    pad_code = request.params['padCode']
    password = base64.encodestring(request.params['password'].encode()).decode('utf-8').replace('\n', '')
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
            pad_d = serialize(pad)
    if error_msg:
        json_a = {
            'success': 'false',
            'error_msg': error_msg,
        }
    else:
        json_a = {
            'success': 'true',
            'pad': pad_d
        }
    return json_a


@view_config(route_name='userCheck', renderer='json')
def user_check(request):
    """
    设备初始化登录
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_account = request.params['userAccount']
    pad_code = request.params['padCode']
    password = base64.encodestring(request.params['password'].encode()).decode('utf-8').replace('\n', '')
    error_msg = ''
    if not pad_code:
        error_msg = '终端编码不能为空'
    elif not user_account:
        error_msg = '用户账号不能为空'
    else:
        with transaction.manager:
            users = dbs.query(SysUser).filter(SysUser.user_account == user_account)
            if not users:
                error_msg = '用户不存在'
            else:
                user = users.filter(SysUser.user_pwd == password).first()
                if not user:
                    error_msg = '密码错误'
                    UserTools.count_err(user)
                    dbs.flush()
                else:
                    pad, error_msg = user_checking(dbs, pad_code, user.id)
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


@view_config(route_name='meetingList', renderer='json')
def meeting_list(request):
    """
    会议list
    :param request:
    :return:
    """
    dbs = request.dbsession
    pad_code = request.params['padCode']
    error_msg = ''
    if not pad_code:
        error_msg = '终端编码不能为空'
    else:
        meetings, error_msg = find_meetings(dbs, pad_code)
        if not meetings:
            error_msg = '无会议信息'
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
