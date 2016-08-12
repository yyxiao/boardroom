#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-08
"""

import os
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from ..service.boardroom_service import find_boardrooms, find_boardroom
from ..service.org_service import find_branch
from ..service.loginutil import request_login
import time


@view_config(route_name='to_brs_info')
@request_login
def boardroom_info(request):
    """
    会议室简介
    :param request:
    :return:
    """
    dbs = request.dbsession
    branches = find_branch(dbs)
    return render_to_response('boardroom/boardroom_info.html', locals(), request)


@view_config(route_name='to_br')
@request_login
def boardrooms(request):
    """
    会议室管理主页
    :param request:
    :return:
    """
    dbs = request.dbsession
    branches = find_branch(dbs)
    return render_to_response('boardroom/boardroom.html', locals(), request)


@view_config(route_name='list_br')
@request_login
def boardroom_list(request):
    """
    会议室列表查询
    :param request:
    :return:
    """
    dbs = request.dbsession
    name = request.params['br_name']
    config = request.params['br_config']
    org_id = request.params['org_id']
    flag = request.params['flag']
    (boardrooms, paginator) = find_boardrooms(dbs, name=name, config=config, org_id=org_id)
    return render_to_response('boardroom/list.html', locals(), request)


@view_config(route_name='to_add_br')
@request_login
def to_add_br(request):
    '''
    添加会议室
    :param request:
    :return:
    '''

    dbs = request.dbsession
    branches = find_branch(dbs)
    return render_to_response('boardroom/add.html', locals(), request)


@view_config(route_name='br_upload_pic', renderer='json')
@request_login
def upload_pic(request):
    '''
    上传会议室图片
    :param request:
    :return:
    '''
    print(os.getcwd())
    # print(request)
    if request.method == 'POST':
        for key in request.params.keys():
            print(key)
        file = request.params['photoimg']
        try:
            filename = file.filename
        except:
            json = {
                'resultFlag': 'success',
                'name': '',
                'error_msg': 'default2.jpg'
            }
            return json
        filepath = os.path.join(os.getcwd(), 'brms/static/img/boardroom/'+filename)  # 存放内容的目标文件路径
        with open(filepath, 'wb') as fp:
            fp.write(file.file.read())
        json = {
            'resultFlag': 'success',
            'name': filename,
            'error_msg': 'default2.jpg'
        }
        return json
