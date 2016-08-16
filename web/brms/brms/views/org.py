#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-15
"""
from datetime import datetime
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ..service.loginutil import request_login
from ..service.org_service import *
from ..common.dateutils import datetime_format


@view_config(route_name='to_org')
@request_login
def to_org(request):
    '''
    打开机构管理页面
    :param request:
    :return:
    '''
    dbs = request.dbsession
    branches = find_branch(dbs)
    return render_to_response('org/org.html', locals(), request)


@view_config(route_name='list_org')
@request_login
def list_org(request):
    '''
    机构列表
    :param request:
    :return:
    '''
    if request.method == 'POST':
        dbs = request.dbsession
        org_name = request.POST.get('org_name', '')
        parent_id = request.POST.get('parent_id', 0)
        address = request.POST.get('address', '')
        page_no = request.POST.get('page', 1)
        (orgs, paginator) = find_orgs(dbs, org_name, parent_id, address, page_no=page_no)
        return render_to_response('org/list.html', locals(), request)


@view_config(route_name='to_add_org')
@request_login
def to_add_org(request):
    '''

    :param request:
    :return:
    '''

    dbs = request.dbsession
    branches = find_branch(dbs)
    return render_to_response('org/add.html', locals(), request)


@view_config(route_name='add_org', renderer='json')
@request_login
def add_org(request):
    '''

    :param request:
    :return:
    '''
    if request.method == 'POST':
        dbs = request.dbsession
        org = SysOrg()
        org.org_name = request.POST.get('org_name', '')
        # org.org_type = request.POST.get('org_type', '')
        org.parent_id = request.POST.get('parent_id', 0)
        org.org_seq = request.POST.get('org_seq', 0)
        org.org_manager = request.POST.get('org_manager', '')
        org.phone = request.POST.get('phone', '')
        org.address = request.POST.get('address', '')
        org.state = request.POST.get('state', 1)
        org.create_time = datetime.now().strftime(datetime_format)
        org.create_user = request.session['userId']
        msg = add(dbs, org)
        json = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }

        return json
    return {}


@view_config(route_name='to_update_org')
@request_login
def to_update_org(request):
    '''

    :param request:
    :return:
    '''
    dbs = request.dbsession
    branches = find_branch(dbs)
    org_id = request.POST.get('org_id', 0)
    org = find_org(dbs, org_id)
    return render_to_response('org/add.html', locals(), request)


@view_config(route_name='update_org')
@request_login
def update_org(request):
    '''

    :param request:
    :return:
    '''
    if request.method == 'POST':
        dbs = request.dbsession
        org_id = request.POST.get('org_id', 0)
        org = find_org_by_id(dbs, org_id)
        if not org_id:
            msg = '更新失败，请刷新页面后重试'
        else:
            org.org_name = request.POST.get('org_name', '')
            # org.org_type = request.POST.get('org_type')
            org.org_seq = request.POST.get('org_seq', 0)
            org.parent_id = request.POST.get('parent_id', 0)
            org.org_manager = request.POST.get('org_manager', '')
            org.phone = request.POST.get('phone', '')
            org.address = request.POST.get('address', '')
            org.state = request.POSt.get('state', 1)
            org.update_time = datetime.now().strftime(datetime_format)
            msg = update(dbs, org)
        json = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        return json
    return {}


@view_config(route_name='delete_org')
@request_login
def delete_org(request):
    '''

    :param request:
    :return:
    '''
    if request.method == 'POST':
        dbs = request.dbsession
        org_id = request.POST.get('org_id', 0)
        msg = delete(dbs, org_id)
        json = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        return json
    return {}


