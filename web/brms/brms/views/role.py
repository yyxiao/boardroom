#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/8
"""


from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ..service.role_service import find_roles, add, delete_role, find_role
from ..service.loginutil import request_login
from ..models.model import SysRole
from ..common.dateutils import datetime_format
from datetime import datetime


@view_config(route_name='to_role')
@request_login
def to_role(request):
    """
    角色管理
    :param request:
    :return:
    """
    dbs = request.dbsession
    url = request.path
    return render_to_response('role/role.html', locals(), request)


@view_config(route_name='list_role')
@request_login
def list_role(request):
    dbs = request.dbsession
    role_name = request.POST.get('name', '')
    page_no = int(request.POST.get('page', '1'))
    (roles, paginator) = find_roles(dbs, role_name, page_no)
    return render_to_response('role/list.html', locals(), request)


@view_config(route_name='to_add_role')
@request_login
def to_add(request):
    dbs = request.dbsession
    # role_name = find_role(dbs)
    return render_to_response('role/add.html', locals(), request)


@view_config(route_name='add_role', renderer='json')
@request_login
def add_role(request):
    dbs = request.dbsession
    role = SysRole()
    role.role_name = request.POST.get('name', '')
    role.role_desc = request.POST.get('desc', '')
    role.create_user = request.session['userId']
    role.create_time = datetime.now().strftime(datetime_format)
    error_msg = add(dbs, role)
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


@view_config(route_name='delete_role', renderer='json')
@request_login
def del_role(request):
    dbs = request.dbsession
    role_id = request.POST.get('id', '')
    error_msg = delete_role(dbs, role_id)
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


@view_config(route_name='to_update_role')
@request_login
def to_update(request):
    dbs = request.dbsession
    role_id = request.POST.get('id', '')
    role = find_role(dbs, role_id)
    return render_to_response('role/add.html', locals(), request)


@view_config(route_name='update_role', renderer='json')
@request_login
def update_role(request):
    dbs = request.dbsession
    role_id = request.POST.get('id', '')
    role = find_role(dbs, role_id)
    role.role_name = request.POST.get('name', '')
    role.role_desc = request.POST.get('desc', '')
    role.create_user = request.session['userId']
    role.create_time = datetime.now().strftime(datetime_format)
    error_msg = add(dbs, role)
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