#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/8
"""


from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from ..service.meeting_service import find_meetings, add, delete_meeting, find_meeting
from ..models.model import HasMeeting
from ..common.dateutils import datetime_format
from datetime import datetime


@view_config(route_name='to_meeting')
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
def list_meeting(request):
    dbs = request.dbsession
    meeting_name = request.POST.get('name', '')
    create_user = request.POST.get('create_user', '')
    page_no = int(request.POST.get('page', '1'))
    (meetings, paginator) = find_meetings(dbs, meeting_name, create_user, page_no)
    return render_to_response('meeting/list.html', locals(), request)


@view_config(route_name='to_add_meeting')
def to_add(request):
    dbs = request.dbsession
    # meeting_name = find_meeting(dbs)
    return render_to_response('meeting/add.html', locals(), request)


@view_config(route_name='add_meeting', renderer='json')
def add_meeting(request):
    dbs = request.dbsession
    meeting = HasMeeting()
    meeting.name = request.POST.get('name', '')
    meeting.description = request.POST.get('desc', '')
    meeting.create_user = request.session['userId']
    meeting.create_time = datetime.now().strftime(datetime_format)
    error_msg = add(dbs, meeting)
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


@view_config(route_name='delete_meeting', renderer='json')
def del_meeting(request):
    dbs = request.dbsession
    meeting_id = request.POST.get('id', '')
    error_msg = delete_meeting(dbs, meeting_id)
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


@view_config(route_name='to_update_meeting')
def to_update(request):
    dbs = request.dbsession
    meeting_id = request.POST.get('id', '')
    meeting = find_meeting(dbs, meeting_id)
    return render_to_response('meeting/add.html', locals(), request)


@view_config(route_name='update_meeting', renderer='json')
def update_meeting(request):
    dbs = request.dbsession
    meeting_id = request.POST.get('id', '')
    meeting = find_meeting(dbs, meeting_id)
    meeting.name = request.POST.get('name', '')
    meeting.description = request.POST.get('desc', '')
    meeting.create_user = request.session['userId']
    meeting.create_time = datetime.now().strftime(datetime_format)
    error_msg = add(dbs, meeting)
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