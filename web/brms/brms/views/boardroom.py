#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-08
"""

from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ..service.boardroom_service import find_boardrooms, find_boardroom
from ..service.org_service import find_branch


@view_config(route_name='to_brs_info')
def boardroom_info(request):
    """
    会议室简介
    :param request:
    :return:
    """
    dbs = request.dbsession
    branches = find_branch(dbs)
    return render_to_response('boardroom/boardroom_info.html', locals(), request)


@view_config(route_name='to_br')
def boardrooms(request):
    """
    会议室管理主页
    :param request:
    :return:
    """
    return render_to_response('boardroom/boardroom.html', locals(), request)


@view_config(route_name='list_br')
def boardroom_list(request):
    """
    会议室列表查询
    :param request:
    :return:
    """
    dbs = request.dbsession
    name = request.params['br_name']
    config = request.params['br_config']
    org_id = request.params['org_id']
    (boardrooms, paginator) = find_boardrooms(dbs, name=name, config=config, org_id=org_id)
    return render_to_response('boardroom/list.html', locals(), request)



