#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/19
"""

import json
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
from ..service.user_service import *
from ..service.org_service import find_branch_json
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
    org_ids = request.POST.get('org_ids', '')
    branch_json = json.dumps(find_branch_json(dbs))
    return render_to_response('auth/user_auth.html', locals(), request)
