#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/8
"""

import copy
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ..common.dateutils import datetime_format
from ..service.meeting_service import *
from ..service.loginutil import request_login


@view_config(route_name='to_meeting')
@request_login
def to_meeting(request):
    """
    会议管理
    :param request:
    :return:
    """
    dbs = request.dbsession
    url = request.path
    return render_to_response('meeting/meeting.html', locals(), request)


@view_config(route_name='list_meeting')
@request_login
def list_meeting(request):
    dbs = request.dbsession
    meeting_name = request.POST.get('name', '')
    room_name = request.POST.get('room_name', '')
    start_date = request.POST.get('start_date', '')
    end_date = request.POST.get('end_date', '')
    # flag判断是我的预定还是会议管理
    flag = request.POST.get('flag', '')
    if flag == 'my':
        create_user = request.session['userId']
        user_org_id = None
    else:
        create_user = request.POST.get('create_user', '')
        user_org_id = request.session['userOrgId']
    page_no = int(request.POST.get('page', '1'))
    (meetings, paginator) = find_meetings(dbs, meeting_name, create_user, flag, user_org_id, room_name, start_date,
                                          end_date, page_no)
    return render_to_response('meeting/list.html', locals(), request)


@view_config(route_name='to_add_meeting')
@request_login
def to_add(request):
    dbs = request.dbsession
    rooms = find_rooms(dbs)
    return render_to_response('meeting/add.html', locals(), request)


@view_config(route_name='add_meeting', renderer='json')
@request_login
def add_meeting(request):
    dbs = request.dbsession
    meeting = HasMeeting()
    # if pad_code:
    #     # 查找pad对应的会议室
    #     board_room = dbs.query(HasBoardroom.id, HasBoardroom.name).\
    #         outerjoin(HasPad, HasPad.id == HasBoardroom.pad_id).\
    #         filter(HasPad.pad_code == pad_code)
    #     if board_room:
    room_id = int(request.POST.get('room_id', 0))
    meeting.name = request.POST.get('name', '')
    meeting.description = request.POST.get('desc', '')
    meeting.start_date = request.POST.get('start_date', '')
    meeting.end_date = request.POST.get('end_date', '')
    meeting.start_time = request.POST.get('start_time', '')
    meeting.end_time = request.POST.get('end_time', '')
    meeting.org_id = int(request.POST.get('org_id', 0))
    meeting.repeat = REPEAT_YES if request.POST.get('is_repeat', 'false') == 'true' else ''
    meeting.repeat_date = request.POST.get('weekday[]', '')
    meeting.create_user = request.session['userId']
    meeting.create_time = datetime.now().strftime(datetime_format)
    error_msg = find_user_period(dbs, meeting.start_date, meeting.end_date, meeting.create_user)
    if not error_msg:
        error_msg = add(dbs, meeting, room_id)
    if error_msg:
        json_str = {
            'success': False,
            'error_msg': error_msg,
        }
    else:
        json_str = {
            'success': True,
        }
    return json_str


@view_config(route_name='delete_meeting', renderer='json')
@request_login
def del_meeting(request):
    dbs = request.dbsession
    meeting_id = int(request.POST.get('id', 0))
    user_id = request.session['userId']
    error_msg = delete_meeting(dbs, meeting_id, user_id)
    if error_msg:
        json_str = {
            'success': False,
            'error_msg': error_msg,
        }
    else:
        json_str = {
            'success': True,
        }
    return json_str


@view_config(route_name='to_update_meeting')
def to_update(request):
    dbs = request.dbsession
    meeting_id = int(request.POST.get('id', 0))
    rooms = find_rooms(dbs)
    meeting = find_meeting_bdr(dbs, meeting_id)
    return render_to_response('meeting/add.html', locals(), request)


@view_config(route_name='to_update_meeting_calender', renderer='json')
@request_login
def to_update_calender(request):
    dbs = request.dbsession
    meeting_id = int(request.POST.get('id', 0))
    meeting = find_meeting_bdr(dbs, meeting_id)
    return json.dumps(meeting)


@view_config(route_name='update_meeting', renderer='json')
@request_login
def update_meeting(request):
    dbs = request.dbsession
    meeting_id = int(request.POST.get('id', 0))

    room_id = int(request.POST.get('room_id', 0))
    meeting = find_meeting(dbs, meeting_id)

    old_meeting = copy.deepcopy(meeting)

    meeting.name = request.POST.get('name', '')
    meeting.description = request.POST.get('desc', '')
    meeting.repeat = REPEAT_YES if request.POST.get('is_repeat', 'false') == 'true' else ''
    meeting.start_date = request.POST.get('start_date', '')
    meeting.end_date = request.POST.get('end_date', '')
    meeting.start_time = request.POST.get('start_time', '')
    meeting.end_time = request.POST.get('end_time', '')

    error_msg = find_user_period(dbs, meeting.start_date, meeting.end_date, meeting.create_user)
    if not error_msg:
        error_msg = update(dbs, meeting, room_id, old_meeting=old_meeting)
    if error_msg:
        json_str = {
            'success': False,
            'error_msg': error_msg,
        }
    else:
        json_str = {
            'success': True,
        }
    return json_str


@view_config(route_name='my_meeting')
@request_login
def my_meeting(request):
    dbs = request.dbsession
    return render_to_response('meeting/mymeeting.html', locals(), request)
