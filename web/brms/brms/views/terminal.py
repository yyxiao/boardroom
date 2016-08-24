#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/8
"""


from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ..service.terminal_service import *
from ..service.loginutil import request_login
from ..models.model import HasPad
from ..common.dateutils import date_now


@view_config(route_name='to_terminal')
@request_login
def to_terminal(request):
    """
    终端管理
    :param request:
    :return:
    """
    dbs = request.dbsession
    url = request.path
    return render_to_response('terminal/terminal.html', locals(), request)


@view_config(route_name='list_terminal')
@request_login
def list_terminal(request):
    dbs = request.dbsession
    pad_code = request.POST.get('search_code', '')
    meeting_name = request.POST.get('search_meeting_name', '')
    page_no = int(request.POST.get('page', '1'))
    user_org_id = request.session['userOrgId']
    (terminals, paginator) = find_terminals(dbs, pad_code, meeting_name, page_no, user_org_id)
    return render_to_response('terminal/list.html', locals(), request)


@view_config(route_name='to_add_terminal')
@request_login
def to_add(request):
    user_id = request.session['userId']
    dbs = request.dbsession
    rooms = find_rooms(dbs, user_id)
    # terminal_name = find_terminal(dbs)
    return render_to_response('terminal/add.html', locals(), request)


@view_config(route_name='add_terminal', renderer='json')
@request_login
def add_terminal(request):
    dbs = request.dbsession
    room_id = request.POST.get('room_id', '')
    terminal = HasPad()
    terminal.pad_code = request.POST.get('pad_code', '')
    terminal.create_user = request.session['userId']
    terminal.create_time = date_now()
    error_msg = add(dbs, terminal, room_id)
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


@view_config(route_name='delete_terminal', renderer='json')
@request_login
def del_terminal(request):
    dbs = request.dbsession
    terminal_id = request.POST.get('id', '')
    error_msg = delete_terminal(dbs, terminal_id)
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


@view_config(route_name='to_update_terminal')
@request_login
def to_update(request):
    dbs = request.dbsession
    user_id = request.session['userId']
    terminal_id = request.POST.get('id', '')
    terminal = find_terminal(dbs, terminal_id)
    rooms = find_rooms(dbs, user_id)
    return render_to_response('terminal/add.html', locals(), request)


@view_config(route_name='update_terminal', renderer='json')
@request_login
def update_terminal(request):
    dbs = request.dbsession
    room_id = request.POST.get('room_id', '')
    terminal_id = request.POST.get('id', '')
    terminal = dbs.query(HasPad).filter(HasPad.id == terminal_id).first()
    terminal.pad_code = request.POST.get('pad_code', '')
    terminal.create_user = request.session['userId']
    terminal.create_time = date_now()
    error_msg = add(dbs, terminal, room_id)
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