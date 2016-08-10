#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'cuizc'
__mtime__ = '2016-08-03'
"""

import base64

import transaction
from pyramid.httpexceptions import HTTPFound
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import view_config

from brms.service.loginutil import request_login, UserTools
from ..models.model import SysUser
from ..common.dateutils import get_welcome


@view_config(route_name='home')
@request_login
def index(request):
    welcome = get_welcome()
    # user_name = request.session['userName']
    # dbs = request.dbsession
    sys_menu_list = [{'url': '/user/to_user', 'icon': 'fa fa-user', 'name': '用户管理'},
                     {'url': '/org/to_org', 'icon': 'fa fa-sitemap', 'name': '机构管理'},
                     {'url': '/role/to_role', 'icon': 'fa fa-user-secret', 'name': '角色管理'},
                     {'url': '/auth/to_auth', 'icon': 'fa fa-unlock-alt', 'name': '授权管理'},
                     {'url': '/boardroom/to_br', 'icon': 'fa fa-university', 'name': '会议室管理'},
                     {'url': '/terminal/to_terminal', 'icon': 'fa fa-television', 'name': '终端管理'},
                     {'url': '/meeting/to_meeting', 'icon': 'fa fa-television', 'name': '会议管理'}]
    login_user_session = {
        'sys_menu': True,
        'sysMenuList': sys_menu_list,
    }
    request.session['loginUserSession'] = login_user_session
    return render_to_response('index.html', locals(), request)


@view_config(route_name='reset_pwd')
def restpwd(request):
    # TODO
    return render_to_response('reset_pwd.html', locals(), request)


@view_config(route_name='login')
def login(request):
    if request.method == 'POST':
        # code = request.params['validate']
        # if code:
        #     if code != request.session['validate']:
        #         error_msg = '验证码错误'
        #         request.session['error_msg'] = error_msg
        #         return render_to_response('index.html', locals(), request)

        dbs = request.dbsession
        user_name = request.params['userName']
        password = base64.encodestring(request.params['password'].encode()).decode('utf-8').replace('\n', '')
        error_msg = None
        user = None
        if not user_name:
            error_msg = '用户名不能为空'
        elif not password:
            error_msg = '密码不能为空'
        else:
            with transaction.manager:
                user = dbs.query(SysUser).filter(SysUser.user_account == user_name).first()
                if not user:
                    error_msg = '用户不存在'
                elif user.err_count >= 5:
                    if UserTools.unlock(user):
                        request.session['userAccount'] = user_name
                        request.session['userId'] = user.id
                        request.session['user_name_db'] = user.user_name
                        return HTTPFound(request.route_url("home"))
                    else:
                        error_msg = '密码错误超过5次，帐号已冻结，次日解冻'
                elif password != user.user_pwd:
                    error_msg = '密码错误'
                    UserTools.count_err(user)
                    dbs.flush()
                else:
                    request.session['userAccount'] = user_name
                    request.session['userId'] = user.id
                    request.session['user_name_db'] = user.user_name
                    return HTTPFound(request.route_url("home"))

        if error_msg:
            request.session['error_msg'] = error_msg
            return render_to_response('login.html', locals(), request)
    else:
        return render_to_response('login.html', {}, request)


@view_config(route_name='logout')
@request_login
def logout(request):
    del(request.session['userAccount'])
    del(request.session['userId'])
    del(request.session['user_name_db'])
    del(request.session['loginUserSession'])
    return render_to_response('login.html', {}, request)


@view_config(route_name='padLogin', renderer='json')
def pad_login(request):
    if request.method == 'POST':
        dbs = request.dbsession
        user_account = request.params['user_account']
        pad_code = request.params['pad_code']
        password = base64.encodestring(request.params['password'].encode()).decode('utf-8').replace('\n', '')
        error_msg = ''
        if not pad_code:
            error_msg = '终端编码不能为空'
        elif not user_account:
            error_msg = '用户账号不能为空'
        else:
            with transaction.manager:
                user = dbs.query(SysUser).filter(SysUser.user_account == user_account).first()
                if not user:
                    error_msg = '用户不存在'
                elif password != user.user_pwd:
                    error_msg = '密码错误'
                    UserTools.count_err(user)
                    dbs.flush()
        if error_msg:
            request.session['error_msg'] = error_msg
            return render_to_response('login.html', locals(), request)
    else:
        return render_to_response('login.html', {}, request)
