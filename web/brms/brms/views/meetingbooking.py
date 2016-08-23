#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-16
"""

import json
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ..service.loginutil import request_login
from ..service.org_service import find_branch_json
from ..service.boardroom_service import *
from ..service.meeting_service import *
from ..service.booking_service import *


@view_config(route_name='meeting_booking')
@request_login
def meeting_booking(request):
    '''
    会议预订
    :param request:
    :return:
    '''
    dbs = request.dbsession
    branch_json = json.dumps(find_branch_json(dbs))
    return render_to_response('booking/booking.html', locals(), request)


@view_config(route_name='check_available', renderer='json')
@request_login
def check_available(request):
    '''
    检查是否可预订
    :param request:
    :return:
    '''

    if request.method == 'POST':
        dbs = request.dbsession
        room_id = int(request.POST.get('room_id', 0))
        date = request.POST.get('date', '')
        start_time = request.POST.get('start_time', '')
        end_time = request.POST.get('end_time', '')

        msg = check_occupy(dbs, room_id, date, start_time, end_time)
        json = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        return json
    return {}


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
        return json
    return {}




