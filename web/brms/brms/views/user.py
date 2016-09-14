#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-09
"""
import json
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from ..common.password import get_password, DEFAULT_PASSWORD
from ..service.user_service import *
from ..service.org_service import find_branch, find_branch_json
from ..service.role_service import find_roles
from ..service.loginutil import request_login
from ..service.log_service import HyLog
from ..common.dateutils import datetime_format


@view_config(route_name='to_user')
@request_login
def user_index(request):
    """
    用户管理
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_org_id = request.session['userOrgId']
    branch_json = json.dumps(find_branch_json(dbs, user_org_id))
    return render_to_response('user/user.html', locals(), request)


@view_config(route_name='list_user')
@request_login
def list_user(request):
    """
    用户列表
    :param request:
    :return:
    """
    if request.method == 'POST':
        dbs = request.dbsession
        user_account = request.POST.get('user_account', '')
        user_name = request.POST.get('user_name', '')
        role_name = request.POST.get('role_name', '')
        # show_child = request.POST.get('show_child', 'false') == 'true'
        org_id = request.POST.get('org_id', '')
        if not org_id:
            org_id = request.session['userOrgId']
            show_child = True
        else:
            show_child = False
        page = int(request.POST.get('page', 1))

        (users, paginator) = find_users(dbs, org_id, user_account, user_name, role_name, page, show_child=show_child)
        HyLog.log_research(request.client_addr, request.session['userAccount'],
                           ';'.join([str(org_id), user_account, user_name, role_name]), 'user')
        return render_to_response('user/list.html', locals(), request)

    return Response('', 404)


@view_config(route_name='to_add_user')
@request_login
def to_add(request):
    """
    打开添加用户对话框
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_org_id = request.session['userOrgId']
    branches = find_branch(dbs, user_org_id)
    (roles, paginator) = find_roles(dbs, page_no=0, filter_sys=True)
    return render_to_response('user/add.html', locals(), request)


@view_config(route_name='add_user', renderer='json')
@request_login
def add_user(request):
    """
    添加用户
    :param request:
    :return:
    """
    if request.method == 'POST':
        dbs = request.dbsession
        user_account = request.POST.get('user_account', '')
        msg = check_user_account(dbs, user_account)
        if not msg:
            user = SysUser()
            user.user_account = user_account
            user.user_name = request.POST.get('user_name', '')
            user.phone = request.POST.get('phone', '')
            user.address = request.POST.get('address', '')
            user.email = request.POST.get('email', '')
            user.max_period = request.POST.get('max_period', 7)
            user.user_type = request.POST.get('user_type', 0)
            user.org_id = request.POST.get('org_id', 0)
            user.position = request.POST.get('position', '')
            user.create_time = datetime.now().strftime(datetime_format)
            user.create_user = request.session['userId']
            user.state = request.POST.get('state', 1)
            role_id = request.POST.get('role_id', 0)

            init_pwd = DEFAULT_PASSWORD  # init_password()
            user.user_pwd = get_password(init_pwd)
            msg = add(dbs, user, role_id, request.session['userId'])
        json_str = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        if not msg:
            HyLog.log_add(request.client_addr, request.session['userAccount'], user_account+' success', 'user')
        return json_str

    return {}


@view_config(route_name='to_update_user')
@request_login
def to_update_user(request):
    """
    打开更新用户对话框
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_org_id = request.session['userOrgId']
    branches = find_branch(dbs, user_org_id)
    user_id = request.POST.get('user_id', 0)
    user = find_user(dbs, user_id)
    (roles, paginator) = find_roles(dbs, page_no=0, filter_sys=True)
    return render_to_response('user/add.html', locals(), request)


@view_config(route_name='update_user', renderer='json')
@request_login
def update_user(request):
    """
    更新用户
    :param request:
    :return:
    """
    if request.method == 'POST':
        dbs = request.dbsession
        user = find_user_by_id(dbs, request.POST.get('user_id', 0))
        user.user_account = request.POST.get('user_account', '')
        user.user_name = request.POST.get('user_name', '')
        user.phone = request.POST.get('phone', '')
        user.address = request.POST.get('address', '')
        user.email = request.POST.get('email', '')
        user.max_period = request.POST.get('max_period', 7)
        user.user_type = request.POST.get('user_type', 0)
        user.position = request.POST.get('position', '')
        user.state = request.POST.get('state', '')

        org_id = request.POST.get('org_id', 0)
        role_id = request.POST.get('role_id', 0)

        user.update_time = datetime.now().strftime(datetime_format)
        msg = update(dbs, user, role_id, org_id, request.session['userId'])
        json_str = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        if not msg:
            HyLog.log_update(request.client_addr, request.session['userAccount'],
                             request.POST.get('user_id', '') + ' success', 'user')
        return json_str

    return {}


@view_config(route_name='delete_user', renderer='json')
@request_login
def delete_user(request):
    """
    删除用户
    :param request:
    :return:
    """
    if request.method == 'POST':
        dbs = request.dbsession
        user_id = int(request.POST.get('id', 0))
        msg = delete(dbs, user_id)
        json_str = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        if not msg:
            HyLog.log_delete(request.client_addr, request.session['userAccount'], str(user_id)+' success', 'user')
        return json_str

    return {}


@view_config(route_name='to_user_setting')
@request_login
def to_user_setting(request):
    """
    打开用户设置页面
    :param request:
    :return:
    """

    dbs = request.dbsession
    user_id = request.session['userId']
    user = find_user_by_id(dbs, user_id)
    return render_to_response('user/user_setting.html', locals(), request)


@view_config(route_name='user_setting', renderer='json')
@request_login
def user_setting(request):
    """
    用户设置
    :param request:
    :return:
    """
    if request.method == 'POST':
        dbs = request.dbsession
        local_id = request.session['userId']
        user_id = int(request.POST.get('user_id', 0))
        if local_id != user_id:
            msg = '非法请求'
        else:
            user = find_user_by_id(dbs, local_id)
            if user.user_pwd != get_password(request.POST.get('passwd_old', '')):
                msg = '原密码错误！'
            else:
                user.user_pwd = get_password(request.POST.get('passwd_new', ''))
                user.user_name = request.POST.get('user_name', '')
                user.phone = request.POST.get('phone', '')
                msg = update(dbs, user)
        json_str = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        if not msg:
            HyLog.log_update(request.client_addr, request.session['userAccount'],
                             request.POST.get('user_id', '') + ' change pwd success', 'user')
        return json_str
    return {}
