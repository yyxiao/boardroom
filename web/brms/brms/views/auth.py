#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/19
"""

import json
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ..service.user_service import user_org
from ..service.org_service import find_branch_json, find_branch_json_check
from ..service.loginutil import request_login
from ..common.dateutils import date_now


@view_config(route_name='to_auth')
@request_login
def auth_index(request):
    """
    授权管理
    :param request:
    :return:
    """
    dbs = request.dbsession
    branch_json = json.dumps(find_branch_json(dbs))
    return render_to_response('auth/auth.html', locals(), request)


@view_config(route_name='to_auth_user')
@request_login
def auth_user(request):
    dbs = request.dbsession
    user_id = request.POST.get('id', '')
    branch_json = json.dumps(find_branch_json_check(dbs, user_id))
    return render_to_response('auth/user_auth.html', locals(), request)


@view_config(route_name='update_auth_user', renderer='json')
@request_login
def update_auth_user(request):
    user_id = request.POST.get('user_id', '')
    org_ids = request.POST.get('org_ids', '')
    create_user = request.session['userId']
    if not user_id:
        error_msg = '用户ID不能为空！'
    else:
        error_msg = '用户ID不能为空！'
    dbs = request.dbsession
    org_list = org_ids.split(',')
    error_msg = user_org(dbs, user_id, create_user, org_list, date_now())
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

