#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-08
"""

import json

from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import view_config

from brms.common.constant import BRMS_URL
from ..common.dateutils import datetime_format
from ..service.boardroom_service import *
from ..service.loginutil import request_login
from ..service.org_service import find_branch, find_branch_json


@view_config(route_name='to_brs_info')
@request_login
def boardroom_info(request):
    """
    会议室简介
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_org_id = request.session['userOrgId']
    branch_json = json.dumps(find_branch_json(dbs, user_org_id, '0'))
    return render_to_response('boardroom/boardroom_info.html', locals(), request)


@view_config(route_name='to_br')
@request_login
def to_boardrooms(request):
    """
    会议室管理主页
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_org_id = request.session['userOrgId']
    branch_json = json.dumps(find_branch_json(dbs, user_org_id, '0'))
    return render_to_response('boardroom/boardroom.html', locals(), request)


@view_config(route_name='list_br')
@request_login
def boardroom_list(request):
    """
    会议室列表查询
    :param request:
    :return:
    """
    if request.method == 'POST':
        dbs = request.dbsession
        name = request.POST.get('br_name', '')
        config = request.POST.get('br_config', '')
        org_id = request.POST.get('org_id', '')
        if org_id == '':
            org_id = request.session['userOrgId']
        show_child = request.POST.get('show_child', 'false') == 'true'
        flag = request.POST.get('flag', '')
        page_no = int(request.POST.get('page', ''))
        (boardrooms, paginator) = find_boardrooms(dbs, name=name, config=config, org_id=org_id, page_no=page_no,
                                                  show_child=show_child)
        return render_to_response('boardroom/list.html', locals(), request)

    return Response('', 404)


@view_config(route_name='to_add_br')
@request_login
def to_add_br(request):
    """
    添加会议室
    :param request:
    :return:
    """

    dbs = request.dbsession
    user_org_id = request.session['userOrgId']
    branches = find_branch(dbs, user_org_id, '0')
    return render_to_response('boardroom/add.html', locals(), request)


@view_config(route_name='br_upload_pic', renderer='json')
@request_login
def upload_pic(request):
    """
    上传会议室图片
    :param request:
    :return:
    """
    if request.method == 'POST':
        app_path = request.registry.settings['app_path']
        file = request.POST.get('br_pic', '')
        save_name = ''
        if file != '':
            upload_name = file.filename
            save_name = get_save_name(upload_name)
            msg = writefile(file.file, save_name, app_path=app_path)

            if not msg:
                request.session[upload_name] = save_name
        else:
            msg = 'file name is null'

        json_str = {
            'resultFlag': 'failed' if msg else 'success',
            'name': save_name,
            'error_msg': msg
        }
        return json_str

    return {}


@view_config(route_name='add_br', renderer='json')
@request_login
def add_br(request):
    """
    添加会议室
    :param request:
    :return:
    """

    if request.method == 'POST':
        app_path = request.registry.settings['app_path']
        dbs = request.dbsession

        br = HasBoardroom()
        br.name = request.POST.get('br_name', '')
        br.org_id = request.POST.get('org_id', 0)
        br.config = request.POST.get('br_config', '')
        br.description = request.POST.get('br_desc', '')
        pic_name = request.POST.get('br_pic', '')
        if pic_name:
            br.picture = request.session[pic_name]
        br.state = request.POST.get('state', 1)
        br.create_time = datetime.now().strftime(datetime_format)
        br.create_user = request.session['userId']

        br_pic = br.picture
        org_id = br.org_id
        msg = add(dbs, br)
        if not msg and pic_name:
            move_pic(br_pic, org_id, app_path)

        json_str = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        return json_str

    return {}


@view_config(route_name='delete_br', renderer='json')
@request_login
def delete_br(request):
    """
    删除会议室
    :param request:
    :return:
    """

    if request.method == 'POST':
        app_path = request.registry.settings['app_path']
        dbs = request.dbsession
        br_id = request.POST.get('br_id')

        msg = delete(dbs, br_id, app_path)

        json_str = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        return json_str

    return {}


@view_config(route_name='to_update_br', renderer='json')
@request_login
def to_update_br(request):
    """
    更新会议室页面
    :param request:
    :return:
    """

    dbs = request.dbsession
    user_org_id = request.session['userOrgId']
    branches = find_branch(dbs, user_org_id, '0')
    br_id = request.POST.get('br_id')
    boardroom = find_boardroom(dbs, br_id)
    return render_to_response('boardroom/add.html', locals(), request)


@view_config(route_name='update_br', renderer='json')
@request_login
def update_br(request):
    """
    更新会议室
    :param request:
    :return:
    """

    if request.method == 'POST':
        dbs = request.dbsession
        app_path = request.registry.settings['app_path']
        br = dbs.query(HasBoardroom).filter(HasBoardroom.id == request.POST.get('br_id', 0)).first()
        old_pic = br.picture
        old_org = br.org_id
        br.name = request.POST.get('br_name', '')
        br.org_id = request.POST.get('org_id', 0)
        br.config = request.POST.get('br_config', '')
        br.description = request.POST.get('br_desc', '')
        pic_name = request.POST.get('br_pic', '')
        if pic_name:
            br.picture = request.session[pic_name]
        br.state = request.POST.get('state', 1)
        br_pic = br.picture
        org_id = br.org_id
        msg = update(dbs, br)
        if not msg and pic_name:
            delete_pic(old_pic, old_org, app_path)
            move_pic(br_pic, org_id, app_path)

        json_str = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }

        return json_str

    return {}


@view_config(route_name='to_room_qrcode')
@request_login
def to_room_qrcode(request):
    """
    :return:
    """
    dbs = request.dbsession
    return render_to_response('boardroom/qrcode.html', locals(), request)


@view_config(route_name='room_qrcode')
@request_login
def room_qrcode(request):
    """
    生成二维码
    :param request:
    :return:
    """
    dbs = request.dbsession
    url = BRMS_URL
    room_id = request.GET.get('room_id', 0)
    user_id = request.session['userId']
    image_stream = make_qrcode(dbs, url, room_id, user_id)
    response = Response(
        image_stream,
        request=request,
        content_type='image/png'
    )
    return response
