#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/8
"""


from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ..service.terminal_service import find_terminals, add, delete_terminal, find_terminal
from ..models.model import HasPad
from ..common.dateutils import date_now


@view_config(route_name='to_terminal')
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
def list_terminal(request):
    dbs = request.dbsession
    pad_code = request.POST.get('search_code', '')
    meeting_name = request.POST.get('search_meeting_name', '')
    page_no = int(request.POST.get('page', '1'))
    (terminals, paginator) = find_terminals(dbs, pad_code, meeting_name, page_no)
    return render_to_response('terminal/list.html', locals(), request)


@view_config(route_name='to_add_terminal')
def to_add(request):
    dbs = request.dbsession
    # terminal_name = find_terminal(dbs)
    return render_to_response('terminal/add.html', locals(), request)


@view_config(route_name='add_terminal', renderer='json')
def add_terminal(request):
    dbs = request.dbsession
    terminal = HasPad()
    terminal.terminal_name = request.POST.get('name', '')
    terminal.terminal_desc = request.POST.get('desc', '')
    terminal.create_user = request.session['userId']
    terminal.create_time = date_now()
    error_msg = add(dbs, terminal)
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
def to_update(request):
    dbs = request.dbsession
    terminal_id = request.POST.get('id', '')
    terminal = find_terminal(dbs, terminal_id)
    return render_to_response('terminal/add.html', locals(), request)


@view_config(route_name='update_terminal', renderer='json')
def update_terminal(request):
    dbs = request.dbsession
    terminal_id = request.POST.get('id', '')
    terminal = find_terminal(dbs, terminal_id)
    terminal.terminal_name = request.POST.get('name', '')
    terminal.terminal_desc = request.POST.get('desc', '')
    terminal.create_user = request.session['userId']
    terminal.create_time = date_now()
    error_msg = add(dbs, terminal)
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