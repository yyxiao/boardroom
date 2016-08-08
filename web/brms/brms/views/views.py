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
from ..service.role_service import find_roles


@view_config(route_name='home')
@request_login
def index(request):
    welcome = get_welcome()
    # user_name = request.session['userName']
    # dbs = request.dbsession
    sys_menu_list = [{'url': '/touser', 'icon': 'fa fa-user', 'name': '用户管理'},
                     {'url': '/toorg', 'icon': 'fa fa-sitemap', 'name': '机构管理'},
                     {'url': '/torole', 'icon': 'fa fa-user-secret', 'name': '角色管理'},
                     {'url': '/toauthorization', 'icon': 'fa fa-unlock-alt', 'name': '授权管理'},
                     {'url': '/toboardroom', 'icon': 'fa fa-university', 'name': '会议室管理'},
                     {'url': '/toterminal', 'icon': 'fa fa-television', 'name': '终端管理'}]
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
        print('######## login')
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
                        request.session['userName'] = user_name
                        request.session['user_name_db'] = user.user_name
                        return HTTPFound(request.route_url("home"))
                    else:
                        error_msg = '密码错误超过5次，帐号已冻结，次日解冻'
                elif password != user.user_pwd:
                    error_msg = '密码错误'
                    UserTools.count_err(user)
                    dbs.flush()
                else:
                    request.session['userName'] = user_name
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
    del(request.session['userName'])
    del(request.session['user_name_db'])
    del(request.session['loginUserSession'])
    return render_to_response('login.html', {}, request)


@view_config(route_name='list_role')
def list_role(request):
    dbs = request.dbsession
    role_name = request.POST.get('name', '')
    page_no = int(request.POST.get('page', '1'))
    (roles, paginator) = find_roles(dbs, role_name, page_no)
    return render_to_response('role/list.html', locals(), request)


# 仅供测试
@view_config(route_name='add_user')
def add_user(request):
    if request.method == 'POST':
        # TODO
        print('######## add user')
        dbs = request.dbsession
        with transaction.manager:
            user = SysUser()
            user.user_account = 'sysadmin'
            user.user_name = '系统管理员'
            user.user_pwd = 'MDAwMDAw'
            user.max_period = 30
            user.position = '系统管理员'
            user.org_id = 0
            user.user_type = 0
            user.user_no = '0'
            user.state = '1'

            dbs.add(user)
            dbs.flush()

        return HTTPFound(request.route_url("login"))
    else:
        # TODO 编写模板
        return Response('add user')