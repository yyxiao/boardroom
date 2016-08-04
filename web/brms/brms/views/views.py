#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'cuizc'
__mtime__ = '2016-08-03'
"""

from pyramid.view import view_config
from pyramid.renderers import render_to_response


@view_config(route_name='login')
def login(request):
    '''
    登录
    :param request:
    :return:
    '''

    return render_to_response('login.html', locals(), request)


@view_config(route_name='home')
def index(request):
    x = 2
    y = 4
    return render_to_response('index.html', locals(), request)


@view_config(route_name='resetpwd')
def index(request):

    return render_to_response('resetpwd.html', locals(), request)


@view_config(route_name='checkout')
def checkout(request):

    return render_to_response('index.html', locals(), request)

