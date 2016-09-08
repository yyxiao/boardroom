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
from pyramid.view import view_config

from brms.service.loginutil import request_login, UserTools
from ..models.model import SysUser
from ..common.dateutils import get_welcome
from ..service.menu_service import get_user_menu


@view_config(route_name='home')
def index(request):
    welcome = get_welcome()
    if 'loginUserSession' not in request.session:
        try:
            user_id = request.session['userId']
        except:
            return HTTPFound(request.route_url('login'))

        dbs = request.dbsession
        sys_menu_list = get_user_menu(dbs, user_id)
        login_user_session = {
            'sys_menu': True if len(sys_menu_list) > 0 else False,
            'sysMenuList': sys_menu_list,
        }
        request.session['loginUserSession'] = login_user_session
    return render_to_response('index.html', locals(), request)


@view_config(route_name='reset_pwd')
def reset_pwd(request):
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
                        request.session['userOrgId'] = user.org_id
                        request.session['user_name_db'] = user.user_name
                        return HTTPFound(request.route_url("home"))
                    else:
                        error_msg = '密码错误超过5次，账号已冻结，次日解冻'
                elif password != user.user_pwd:
                    error_msg = '密码错误'
                    UserTools.count_err(user)
                    dbs.flush()
                else:
                    request.session['userAccount'] = user_name
                    request.session['userId'] = user.id
                    request.session['userOrgId'] = user.org_id
                    request.session['user_name_db'] = user.user_name
                    return HTTPFound(request.route_url("home"))

        if error_msg:
            request.session['error_msg'] = error_msg
            return render_to_response('login.html', locals(), request)
    else:
        return render_to_response('login.html', {}, request)


@view_config(route_name='logout')
def logout(request):
    try:
        del(request.session['userAccount'])
        del(request.session['userId'])
        del(request.session['userOrgId'])
        del(request.session['user_name_db'])
        del(request.session['loginUserSession'])
    except:
        pass
    return HTTPFound(request.route_url('login'))
