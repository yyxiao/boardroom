#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-16
"""

from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ..service.loginutil import request_login
from ..service.org_service import find_branch
from ..service.boardroom_service import *
from ..service.meeting_service import *


@view_config(route_name='meeting_booking')
@request_login
def meeting_booking(request):
    '''
    会议预订
    :param request:
    :return:
    '''
    dbs = request.dbsession
    branches = find_branch(dbs)
    return render_to_response('booking/booking.html', locals(), request)


@view_config(route_name='check_available')
@request_login
def check_available(request):
    '''
    检查是否可预订
    :param request:
    :return:
    '''


@view_config(route_name='list_by_org', renderer='json')
@request_login
def list_by_org(request):
    '''

    :param request:
    :return:
    '''
    if request.method == 'POST':
        dbs = request.dbsession
        org_id = int(request.POST.get('org_id', 0))
        (boardrooms, paginator) = find_boardrooms(dbs, org_id=org_id)
        json = {
            'resultFlag': 'success',
            'brs': boardrooms
        }
        print(json)
        return json
    return {}


@view_config(route_name='list_by_br', renderer='json')
@request_login
def list_by_br(request):
    '''

    :param request:
    :return:
    '''

    if request.method == 'POST':
        dbs = request.dbsession
        org_id = int(request.POST.get('org_id', 0))
        br_id = int(request.POST.get('br_id', 0))

        # TODO page_size 临时解决方法，最终不分页
        (meetings, paginator) = find_meetings(dbs, page_size=100, org_id=org_id, room_id=br_id)
        json = {
            'resultFlag': 'success',
            'meetings': meetings
        }
        print(json)
        return json
    return {}




