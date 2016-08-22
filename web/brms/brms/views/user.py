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
from ..common.password import get_password, init_password
from ..service.user_service import *
from ..service.org_service import find_branch, find_branch_json
from ..service.role_service import find_roles
from ..service.loginutil import request_login
from ..common.dateutils import datetime_format


@view_config(route_name='to_user')
@request_login
def user_index(request):
    '''
    用户管理
    :param request:
    :return:
    '''
    dbs = request.dbsession
    branch_json = json.dumps(find_branch_json(dbs))
    return render_to_response('user/user.html', locals(), request)


@view_config(route_name='list_user')
@request_login
def list_user(request):
    '''
    用户列表
    :param request:
    :return:
    '''
    if request.method == 'POST':
        dbs = request.dbsession
        user_account = request.POST.get('user_account', '')
        user_name = request.POST.get('user_name', '')
        org_id = request.POST.get('org_id', '')
        role_name = request.POST.get('role_name', '')
        page = int(request.POST.get('page', 1))

        (users, paginator) = find_users(dbs, user_account, user_name, org_id, role_name, page)

        return render_to_response('user/list.html', locals(), request)

    return Response('', 404)


@view_config(route_name='to_add_user')
@request_login
def to_add(request):
    '''
    打开添加用户对话框
    :param request:
    :return:
    '''
    dbs = request.dbsession
    branches = find_branch(dbs)
    (roles, paginator) = find_roles(dbs)
    return render_to_response('user/add.html', locals(), request)


@view_config(route_name='add_user', renderer='json')
@request_login
def add_user(request):
    '''
    添加用户
    :param request:
    :return:
    '''
    if request.method == 'POST':
        dbs = request.dbsession
        # TODO 判断用户名是否重复
        user = SysUser()
        user.user_account = request.POST.get('user_account', '')
        user.user_name = request.POST.get('user_name', '')
        user.phone = request.POST.get('phone', '')
        user.address = request.POST.get('address', '')
        user.email = request.POST.get('email', '')
        user.max_period = request.POST.get('max_period', 7)
        user.user_type = request.POST.get('user_type', 0)
        user.org_id = request.POST.get('org_id', 0)             # TODO org_id 不能为空
        user.position = request.POST.get('position', '')
        user.create_time = datetime.now().strftime(datetime_format)
        user.create_user = request.session['userId']
        user.state = request.POST.get('state', 1)
        role_id = request.POST.get('role_id', 0)

        init_pwd = init_password()
        user.user_pwd = get_password(init_pwd)
        msg = add(dbs, user, role_id, request.session['userId'])
        json = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        return json

    return {}


@view_config(route_name='to_update_user')
@request_login
def to_update_user(request):
    '''
    打开更新用户对话框
    :param request:
    :return:
    '''
    dbs = request.dbsession
    branches = find_branch(dbs)
    user_id = request.POST.get('user_id', 0)
    user = find_user(dbs, user_id)
    (roles, paginator) = find_roles(dbs)
    return render_to_response('user/add.html', locals(), request)


@view_config(route_name='update_user', renderer='json')
@request_login
def update_user(request):
    '''
    更新用户
    :param request:
    :return:
    '''
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
        user.org_id = request.POST.get('org_id', 0)
        user.position = request.POST.get('position', '')
        user.state = request.POST.get('state', '')
        role_id = request.POST.get('role_id', 0)
        user.update_time = datetime.now().strftime(datetime_format)
        msg = update(dbs, user, role_id, request.session['userId'])
        json = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        return json

    return {}


@view_config(route_name='delete_user', renderer='json')
@request_login
def delete_user(request):
    '''
    删除用户
    :param request:
    :return:
    '''
    if request.method == 'POST':
        dbs = request.dbsession
        user_id = int(request.POST.get('id', 0))
        msg = delete(dbs, user_id)
        json = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }

        return json

    return {}


@view_config(route_name='to_user_setting')
@request_login
def to_user_setting(request):
    '''
    打开用户设置页面
    :param request:
    :return:
    '''

    dbs = request.dbsession
    user_id = request.session['userId']
    user = find_user_by_id(dbs, user_id)
    return render_to_response('user/user_setting.html', locals(), request)


@view_config(route_name='user_setting', renderer='json')
@request_login
def user_setting(request):
    '''
    用户设置
    :param request:
    :return:
    '''
    if request.method == 'POST':
        dbs = request.dbsession
        local_id = request.session['userId']
        user_id = int(request.POST.get('user_id', 0))
        if local_id != user_id:
            print(local_id, user_id)
            print(type(local_id), type(user_id))
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
        json = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        return json
    return {}

