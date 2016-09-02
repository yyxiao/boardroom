#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-16
"""

from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ..service.loginutil import request_login
from ..service.boardroom_service import *
from ..service.meeting_service import *
from ..service.booking_service import *
from ..service.org_service import find_branch_json_4booking


@view_config(route_name='meeting_booking')
@request_login
def meeting_booking(request):
    """
    会议预订
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_id = request.session['userId']
    user_org_id = request.session['userOrgId']
    branch_json = json.dumps(find_branch_json_4booking(dbs, user_id, user_org_id))
    return render_to_response('booking/booking.html', locals(), request)


@view_config(route_name='check_available', renderer='json')
@request_login
def check_available(request):
    """
    检查是否可预订
    :param request:
    :return:
    """

    if request.method == 'POST':
        dbs = request.dbsession
        room_id = int(request.POST.get('room_id', 0))
        date = request.POST.get('date', '')
        start_time = request.POST.get('start_time', '')
        end_time = request.POST.get('end_time', '')

        msg = check_occupy(dbs, room_id, date, start_time, end_time)
        json_str = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        return json_str
    return {}


@view_config(route_name='list_by_org', renderer='json')
@request_login
def list_by_org(request):
    if request.method == 'POST':
        dbs = request.dbsession
        org_ids = json.loads(request.POST.get('org_ids', ''))
        boardrooms = []
        for org_id in org_ids:
            (rooms, paginator) = find_boardrooms(dbs, org_id=org_id, page_no=0)
            boardrooms.extend(rooms)
        json_str = {
            'resultFlag': 'success',
            'brs': boardrooms
        }
        return json_str
    return {}


@view_config(route_name='list_by_br', renderer='json')
@request_login
def list_by_br(request):
    if request.method == 'POST':
        dbs = request.dbsession
        org_ids = json.loads(request.POST.get('org_ids', ''))
        room_id = int(request.POST.get('room_id', 0))
        user_id = request.session['userId']
        meetings = find_meeting_calendar(dbs, user_id=user_id, org_ids=org_ids, room_id=room_id)
        json_str = {
            'resultFlag': 'success',
            'meetings': meetings
        }
        return json_str
    return {}


@view_config(route_name='org_room_list', renderer='json')
@request_login
def org_room_list(request):
    dbs = request.dbsession
    user_id = request.session['userId']
    org_ids = json.loads(request.POST.get('org_ids', ''))
    room_id = int(request.POST.get('room_id', 0))
    org_room = find_orgs(dbs, user_id=user_id, org_ids=org_ids, room_id=room_id)
    json_str = {
        'org_room': org_room
    }
    return json_str
