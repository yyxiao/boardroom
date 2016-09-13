#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-08
"""


import json
import copy
import logging

from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.view import view_config

from ..common.dateutils import datetime_format
from ..service.boardroom_service import *
from ..service.loginutil import request_login
from ..service.org_service import find_branch_json_4booking


logger = logging.getLogger('operator')


@view_config(route_name='to_brs_info')
@request_login
def boardroom_info(request):
    """
    会议室简介
    :param request:
    :return:
    """
    dbs = request.dbsession
    user_id = request.session['userId']
    user_org_id = request.session['userOrgId']
    branch_json = json.dumps(find_branch_json_4booking(dbs, user_id, user_org_id))
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
    user_id = request.session['userId']
    user_org_id = request.session['userOrgId']
    branch_json = json.dumps(find_branch_json_4booking(dbs, user_id, user_org_id))
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
        user_id = request.session['userId']
        # if org_id == '':
        #     org_id = request.session['userOrgId']
        show_child = request.POST.get('show_child', 'false') == 'true'
        flag = request.POST.get('flag', '')
        page_no = int(request.POST.get('page', ''))
        (boardrooms, paginator) = find_boardrooms(dbs, user_id, name=name, config=config, org_id=org_id,
                                                  page_no=page_no, show_child=show_child)
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
    user_id = request.session['userId']
    user_org_id = request.session['userOrgId']
    branches = find_branch_json_4booking(dbs, user_id, user_org_id, tree=False)
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

        pic_id = request.POST.get('pic_id', '')
        file = request.POST.get('br_pic', '')

        save_name = ''
        if file != '':
            upload_name = file.filename
            save_name = get_save_name(upload_name)
            msg = writefile(file.file, save_name, app_path=app_path)

            if not msg:
                request.session[pic_id] = save_name
                logger.info('[upload] ip:' + request.client_addr + ' \"' + request.session[
                    'userAccount'] + '\" upload pic' + save_name)
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

        # 记录各图片路径
        room_pic = request.POST.get('room_pic', '')
        if room_pic:
            room_pic = request.session['#room_pic']
            br.picture = IMG_RPATH + br.org_id + '/' + room_pic
        room_logo1 = request.POST.get('room_logo1', '')
        if room_logo1:
            room_logo1 = request.session['#room_logo1']
            br.logo1 = IMG_RPATH + br.org_id + '/' + room_logo1
        room_logo2 = request.POST.get('room_logo2', '')
        if room_logo2:
            room_logo2 = request.session['#room_logo2']
            br.logo2 = IMG_RPATH + br.org_id + '/' + room_logo2
        room_btn = request.POST.get('room_btn', '')
        if room_btn:
            room_btn = request.session['#room_btn']
            br.button_img = IMG_RPATH + br.org_id + '/' + room_btn
        room_bgd = request.POST.get('room_bgd', '')
        if room_bgd:
            room_bgd = request.session['#room_bgd']
            br.background = IMG_RPATH + br.org_id + '/' + room_bgd

        br.state = request.POST.get('state', 1)
        br.create_time = datetime.now().strftime(datetime_format)
        br.create_user = request.session['userId']

        org_id = br.org_id
        msg = check_brm_name(dbs, room_name=request.POST.get('br_name', ''), org_id=request.POST.get('org_id', 0))
        if not msg:
            msg = add(dbs, br)

        if not msg and room_pic:
            move_pic(room_pic, org_id, app_path)
        if not msg and room_logo1:
            move_pic(room_logo1, org_id, app_path)
        if not msg and room_logo2:
            move_pic(room_logo2, org_id, app_path)
        if not msg and room_btn:
            move_pic(room_btn, org_id, app_path)
        if not msg and room_bgd:
            move_pic(room_bgd, org_id, app_path)

        json_str = {
            'resultFlag': 'failed' if msg else 'success',
            'error_msg': msg
        }
        logger.info(
            '[upload] ip:' + request.client_addr + ' \"' + request.session['userAccount'] + '\" add boardroom ' +
            ('failed' if msg else 'success'))
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
    user_id = request.session['userId']
    branches = find_branch_json_4booking(dbs, user_id, user_org_id, tree=False)
    br_id = request.POST.get('br_id')
    boardroom = find_boardroom(dbs, user_id, br_id)
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
        old_br = copy.deepcopy(br)
        new_name = request.POST.get('br_name', '')
        if old_br.name != new_name:
            msg = check_brm_name(dbs, room_name=request.POST.get('br_name', ''), org_id=request.POST.get('org_id', 0))
            if not msg:
                br.name = new_name
            else:
                return {
                        'resultFlag': 'failed',
                        'error_msg': msg
                    }
        br.org_id = request.POST.get('org_id', 0)
        br.config = request.POST.get('br_config', '')
        br.description = request.POST.get('br_desc', '')

        room_pic = request.POST.get('room_pic', '')
        if room_pic:
            room_pic = request.session['#room_pic']
            br.picture = IMG_RPATH + str(br.org_id) + '/' + room_pic
        room_logo1 = request.POST.get('room_logo1', '')
        if room_logo1:
            room_logo1 = request.session['#room_logo1']
            br.logo1 = IMG_RPATH + str(br.org_id) + '/' + room_logo1
        room_logo2 = request.POST.get('room_logo2', '')
        if room_logo2:
            room_logo2 = request.session['#room_logo2']
            br.logo2 = IMG_RPATH + str(br.org_id) + '/' + room_logo2
        room_btn = request.POST.get('room_btn', '')
        if room_btn:
            room_btn = request.session['#room_btn']
            br.button_img = IMG_RPATH + str(br.org_id) + '/' + room_btn
        room_bgd = request.POST.get('room_bgd', '')
        if room_bgd:
            room_bgd = request.session['#room_bgd']
            br.background = IMG_RPATH + str(br.org_id) + '/' + room_bgd

        br.state = request.POST.get('state', 1)
        org_id = br.org_id
        if old_br.org_id != int(org_id):
            update_pic(old_br, br)
        new_br = copy.deepcopy(br)
        msg = update(dbs, br)

        if not msg:
            if room_pic:
                delete_pic(old_br.picture, app_path)
                move_pic(room_pic, org_id, app_path)
            elif old_br.org_id != int(org_id):
                move_piv_org(old_br.picture, new_br.picture, app_path)
            if room_logo1:
                delete_pic(old_br.logo1, app_path)
                move_pic(room_logo1, org_id, app_path)
            elif old_br.org_id != int(org_id):
                move_piv_org(old_br.logo1, new_br.logo1, app_path)
            if room_logo2:
                delete_pic(old_br.logo2, app_path)
                move_pic(room_logo2, org_id, app_path)
            elif old_br.org_id != int(org_id):
                move_piv_org(old_br.logo2, new_br.logo2, app_path)
            if room_btn:
                delete_pic(old_br.button_img, app_path)
                move_pic(room_btn, org_id, app_path)
            elif old_br.org_id != int(org_id):
                move_piv_org(old_br.button_img, new_br.button_img, app_path)
            if room_bgd:
                delete_pic(old_br.background, app_path)
                move_pic(room_bgd, org_id, app_path)
            elif old_br.org_id != int(org_id):
                move_piv_org(old_br.background, new_br.background, app_path)

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
    url = request.registry.settings['brms_pad_url']
    room_id = request.GET.get('room_id', 0)
    user_id = request.session['userId']
    app_path = request.registry.settings['app_path']
    image_stream = make_qrcode(dbs, url, room_id, user_id, app_path)
    response = Response(
        image_stream,
        request=request,
        content_type='image/png'
    )
    return response
