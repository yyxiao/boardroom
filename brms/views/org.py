#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-15
"""
import json
from datetime import datetime

from pyramid.renderers import render_to_response
from pyramid.view import view_config

from ..common.dateutils import datetime_format
from ..service.loginutil import request_login
from ..service.org_service import *
from ..service.log_service import HyLog


@view_config(route_name='to_org')
@request_login
def to_org(request):
    """
    打开机构管理页面
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_org_id = request.session['userOrgId']
    # branches = find_branch(dbs, user_org_id, '0')
    branch_json = json.dumps(find_branch_json(dbs, user_org_id))
    return render_to_response('org/org.html', locals(), request)


@view_config(route_name='list_org')
@request_login
def list_org(request):
    """
    机构列表
    :param request:
    :return:
    """
    if request.method == 'POST':
        dbs = request.dbsession
        org_name = request.POST.get('org_name', '')
        parent_id = request.POST.get('parent_id', 0)
        org_id = request.session['userOrgId']
        address = request.POST.get('address', '')
        page_no = int(request.POST.get('page', 1))
        (orgs, paginator) = find_orgs(dbs, org_name, parent_id, address, org_id, page_no=page_no)
        HyLog.log_research(request.client_addr, request.session['userAccount'],
                           ';'.join([org_name, str(parent_id), address]), 'org')
        return render_to_response('org/list.html', locals(), request)


@view_config(route_name='to_add_org')
@request_login
def to_add_org(request):
    """

    :param request:
    :return:
    """
    dbs = request.dbsession
    user_org_id = request.session['userOrgId']
    branches = find_branch(dbs, user_org_id, '0')
    return render_to_response('org/add.html', locals(), request)


@view_config(route_name='add_org', renderer='json')
@request_login
def add_org(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        dbs = request.dbsession
        org = SysOrg()
        org.org_name = request.POST.get('org_name', '')
        # org.org_type = request.POST.get('org_type', '')
        org.parent_id = request.POST.get('parent_id', 0)
        org_seq = request.POST.get('org_seq', '')
        if org_seq:
            org.org_seq = int(org_seq)
        else:
            org.org_seq = 1000
        org.org_type = request.POST.get('org_type', '0')
        org.org_manager = request.POST.get('org_manager', '')
        org.phone = request.POST.get('phone', '')
        org.address = request.POST.get('address', '')
        org.state = request.POST.get('state', 1)
        org.create_time = datetime.now().strftime(datetime_format)
        org.create_user = request.session['userId']
        msg = check_org_name(dbs, org_name=request.POST.get('org_name', ''), parent_id=request.POST.get('parent_id', 0))
        if not msg:
            msg = add(dbs, org)
        json1 = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        if not msg:
            HyLog.log_add(request.client_addr, request.session['userAccount'],
                          request.POST.get('org_name', '') + ' success', 'org')

        return json1
    return {}


@view_config(route_name='to_update_org')
@request_login
def to_update_org(request):
    """

    :param request:
    :return:
    """
    dbs = request.dbsession
    user_org_id = request.session['userOrgId']
    branches = find_branch(dbs, user_org_id, '0')
    org_id = request.POST.get('org_id', 0)
    org = find_org_by_id(dbs, org_id)
    return render_to_response('org/add.html', locals(), request)


@view_config(route_name='update_org', renderer='json')
@request_login
def update_org(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        dbs = request.dbsession
        org_id = request.POST.get('org_id', 0)
        org = find_org_by_id(dbs, org_id)
        old_org_name = org.org_name
        old_org_parent = str(org.parent_id)
        if not org_id:
            msg = '更新失败，请刷新页面后重试'
        else:
            org.org_name = request.POST.get('org_name', '')
            # org.org_type = request.POST.get('org_type')
            org_seq = request.POST.get('org_seq', '')
            if org_seq:
                org.org_seq = int(org_seq)
            else:
                org.org_seq = 1000
            org.parent_id = request.POST.get('parent_id', 0)
            org.org_type = request.POST.get('org_type', '0')
            org.org_manager = request.POST.get('org_manager', '')
            org_name = request.POST.get('org_name', '')
            parent_id = request.POST.get('parent_id', 0)
            org.phone = request.POST.get('phone', '')
            org.address = request.POST.get('address', '')
            org.state = request.POST.get('state', 1)
            org.update_time = datetime.now().strftime(datetime_format)
            if old_org_name == org_name and old_org_parent == parent_id:
                msg = update(dbs, org)
            else:
                # 检查是否重复
                msg = check_org_name(dbs, org_name=request.POST.get('org_name', ''),
                                     parent_id=request.POST.get('parent_id', 0))
                if not msg:
                    msg = update(dbs, org)
        json1 = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        if not msg:
            HyLog.log_update(request.client_addr, request.session['userAccount'],
                             str(org_id) + ' success', 'org')
        return json1
    return {}


@view_config(route_name='delete_org', renderer='json')
@request_login
def delete_org(request):
    """
    删除机构，同时删除机构下的用户，pad，用户授权中的本机构
    :param request:
    :return:
    """
    if request.method == 'POST':
        dbs = request.dbsession
        org_id = request.POST.get('org_id', 0)
        msg = delete(dbs, org_id)
        json1 = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        if not msg:
            HyLog.log_delete(request.client_addr, request.session['userAccount'], str(org_id)+' success', 'org')
        return json1
    return {}
