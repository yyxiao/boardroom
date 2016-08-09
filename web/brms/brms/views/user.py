#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-09
"""

from datetime import datetime
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from ..models.model import SysUser
from ..common.password import get_password, init_password
from ..service.user_service import find_users, find_user, add, update, delete, send_email
from ..service.org_service import find_branch
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
    branches = find_branch(dbs)
    return render_to_response('user/user.html', locals(), request)


@view_config(route_name='list_user')
@request_login
def list_user(request):
    '''
    用户列表
    :param request:
    :return:
    '''
    dbs = request.dbsession
    user_account = request.params['user_account']
    user_name = request.params['user_name']
    org_id = request.params['org_id']
    role_name = request.params['role_name']
    page = int(request.params['page'])

    (users, paginator) = find_users(dbs, user_account, user_name, org_id, role_name, page)

    return render_to_response('user/list.html', locals(), request)


@view_config(route_name='to_add_user')
@request_login
def to_add(request):
    dbs = request.dbsession
    branches = find_branch(dbs)
    return render_to_response('user/add.html', locals(), request)


@view_config(route_name='add_user', renderer='json')
@request_login
def add_user(request):
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
        user.org_id = request.POST.get('org_id', 0)
        user.position = request.POST.get('position', '')
        user.create_time = datetime.now().strftime(datetime_format)
        user.create_user = request.session['userId']
        user.state = '1'

        init_pwd = init_password()
        user.user_pwd = get_password(init_pwd)
        error_msg = add(dbs, user)
        if error_msg:
            json = {
                'resultFlag': 'failed',
                'error_msg': error_msg
            }
        else:
            # send_email(user.email, init_pwd)
            json = {
                'resultFlag': 'success'
            }
        return json
    else:
        return {}


@view_config(route_name='to_update_user')
@request_login
def to_update_user(request):
    '''
    更新用户
    :param request:
    :return:
    '''
    dbs = request.dbsession
    branches = find_branch(dbs)
    user_id = request.params['user_id']
    user = find_user(dbs, user_id)
    return render_to_response('user/add.html', locals(), request)


@view_config(route_name='update_user', renderer='json')
@request_login
def update_user(request):
    if request.method == 'POST':
        dbs = request.dbsession
        user = SysUser()
        user.id = request.POST.get('user_id')
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
        print('update1')
        error_msg = update(dbs, user)
        if error_msg:
            json = {
                'resultFlag': 'failed',
                'error_msg': error_msg
            }
        else:
            json = {
                'resultFlag': 'success'
            }
        return json
    else:
        return {}


@view_config(route_name='delete_user', renderer='json')
@request_login
def delete_user(request):
    if request.method == 'POST':
        dbs = request.dbsession
        user_id = int(request.POST.get('id', 0))
        error_msg = delete(dbs, user_id)
        if error_msg:
            json = {
                'success': 'false',
                'error_msg': error_msg
            }
        else:
            json = {
                'success': 'true'
            }

        return json
    else:
        return {}
