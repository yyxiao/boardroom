#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'cuizc'
__mtime__ = '2016-08-03'
"""

from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ..models.model import SysDict
from datetime import datetime
import transaction


@view_config(route_name='login')
def login(request):
    '''
    登录
    :param request:
    :return:
    '''
    session = request.dbsession
    with transaction.manager:
        print('create a user')
        sys_dict = SysDict()
        sys_dict.dict_name = '会议室1'
        sys_dict.dict_type = '多媒体会议室'
        sys_dict.create_time = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        session.add(sys_dict)
        session.flush()

    return render_to_response('login.html', locals(), request)


@view_config(route_name='home')
def index(request):
    return render_to_response('index.html', locals(), request)


@view_config(route_name='resetpwd')
def restpwd(request):

    return render_to_response('resetpwd.html', locals(), request)


@view_config(route_name='checkout')
def checkout(request):

    return render_to_response('index.html', locals(), request)

