#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/8
"""


from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from ..service.role_service import find_roles, add
from ..models.model import SysRole
from ..common.dateutils import datetime_format
from datetime import datetime


@view_config(route_name='to_role')
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
def list_role(request):
    dbs = request.dbsession
    role_name = request.POST.get('name', '')
    page_no = int(request.POST.get('page', '1'))
    (roles, paginator) = find_roles(dbs, role_name, page_no)
    return render_to_response('role/list.html', locals(), request)


@view_config(route_name='to_add')
def to_add(request):
    dbs = request.dbsession
    # role_name = find_role(dbs)
    return render_to_response('role/add.html', locals(), request)


@view_config(route_name='add', renderer='json')
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
