#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-10
"""
import logging
import transaction
import os
import shutil
import qrcode
from PIL import Image
from io import BytesIO
from datetime import datetime
from ..models.model import SysOrg, HasBoardroom
from ..common.paginator import Paginator
from ..service.org_service import find_branch_json


logger = logging.getLogger('operator')


def find_boardrooms(dbs, br_id=None, name=None, config=None, org_id=None, page_no=1, show_child=False):
    """
    查询符合条件的办公室，返回列表和分页对象
    :param dbs:
    :param br_id:
    :param name:
    :param config:
    :param org_id:
    :param page_no:
    :param show_child:
    :return:
    """
    boardrooms = dbs.query(HasBoardroom.id,
                           HasBoardroom.name,
                           HasBoardroom.picture,
                           HasBoardroom.config,
                           HasBoardroom.description,
                           HasBoardroom.org_id,
                           SysOrg.org_name,
                           HasBoardroom.pad_id,
                           HasBoardroom.state)\
        .outerjoin(SysOrg, SysOrg.id == HasBoardroom.org_id)

    if name:
        boardrooms = boardrooms.filter(HasBoardroom.name.like('%' + name + '%'))
    if config:
        boardrooms = boardrooms.filter(HasBoardroom.config.like('%' + config + '%'))
    if org_id:
        if show_child:
            tmp = find_branch_json(dbs, org_id)
            child_org = list(map((lambda x: x['id']), tmp))
            boardrooms = boardrooms.filter(HasBoardroom.org_id.in_(child_org))
        else:
            boardrooms = boardrooms.filter(HasBoardroom.org_id == org_id)
    if br_id:
        boardrooms = boardrooms.filter(HasBoardroom.id == br_id)

    boardrooms = boardrooms.order_by(HasBoardroom.create_time.desc())
    if page_no == 0:
        results = boardrooms.all()
        paginator = None
    else:
        results, paginator = Paginator(boardrooms, page_no).to_dict()
    lists = []
    for obj in results:
        br_id = obj[0] if obj[0] else ''
        br_name = obj[1] if obj[1] else ''
        picture = obj[2] if obj[2] else ''
        config = obj[3] if obj[3] else ''
        description = obj[4] if obj[4] else ''
        org_id = obj[5] if obj[5] else ''
        org_name = obj[6] if obj[6] else ''
        pad_code = obj[7] if obj[7] else ''
        state = obj[8] if obj[8] else ''

        temp_dict = {
            'br_id': br_id,
            'br_name': br_name,
            'picture': (str(org_id) + '/' + picture) if picture else '',
            'config': config,
            'description': description,
            'org_id': org_id,
            'org_name': org_name,
            'pad_code': pad_code,
            'state': state
        }
        lists.append(temp_dict)
    return lists, paginator


def find_boardroom(dbs, br_id):
    """
    根据id查找会议室
    :param dbs:
    :param br_id:
    :return:
    """
    (brs, paginator) = find_boardrooms(dbs, br_id=br_id)
    if len(brs) >= 1:
        return brs[0]
    return None


def add(dbs, boardroom):
    """
    添加会议室到数据库
    :param dbs:
    :param boardroom:
    :return:
    """
    try:
        with transaction.manager:
            dbs.add(boardroom)
            dbs.flush()
        return ''
    except Exception as e:
        logger.error(e)
        return '添加会议室失败，请核对后重试'


def update(dbs, boardroom):
    """
    更新会议室信息到数据库
    :param dbs:
    :param boardroom:
    :return:
    """
    try:
        with transaction.manager:
            dbs.merge(boardroom)
        msg = ''
    except Exception as e:
        logger.error(e)
        msg = '更新会议室信息失败，请核对后重试'
    return msg


def delete(dbs, br_id, app_path=None):
    """
    删除会议室
    :param dbs:
    :param br_id:
    :param app_path:
    :return:
    """

    try:
        with transaction.manager:
            br = dbs.query(HasBoardroom).filter(HasBoardroom.id == br_id).first()
            if br.picture:
                delete_pic(br.picture, br.org_id, app_path)
            dbs.delete(br)

        return ''
    except Exception as e:
        logger.error(e)
        return '删除用户失败！'


def writefile(file, filename, org_id=None, app_path=None):
    """

    :param file:
    :param filename:
    :param org_id:
    :param app_path:
    :return:
    """

    file_path = get_pic_path(filename, org_id, app_path)
    try:
        with open(file_path, 'wb') as fp:
            fp.write(file.read())
        msg = ''
    except IOError:
        msg = 'file write error'
    return msg


def delete_pic(filename, org_id=None, app_path=None):
    """
    删除会议室图片
    :param filename:
    :param org_id:
    :param app_path:
    :return:
    """

    if not filename:
        return

    file_path = get_pic_path(filename, org_id, app_path=app_path, create_dirs=False)
    if os.path.exists(file_path):
        os.remove(file_path)


def get_pic_path(filename, org_id=None, app_path=None, create_dirs=True):
    """

    :param filename:
    :param org_id:
    :param app_path:
    :param create_dirs:
    :return:
    """
    # 若org_id为空，则写入到临时目录
    if not org_id:
        org_id = 'tmp'
    else:
        org_id = 'org/' + str(org_id)

    path = os.path.join(app_path, 'boardroom_manage/web/brms/brms/static/img/boardroom/', org_id)
    if create_dirs:
        os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, filename)
    return file_path


def get_save_name(filename):
    """
    获取文件扩展名
    :param filename:
    :return:
    """
    name = str(int(datetime.now().timestamp() * 1000000))
    return name + os.path.splitext(filename)[1]


def move_pic(br_pic, org_id, app_path=None):
    """
    从临时目录移动图片到对应机构下
    :param br_pic:
    :param org_id:
    :param app_path:
    :return:
    """
    src_path = get_pic_path(br_pic, app_path=app_path, create_dirs=False)
    target_path = get_pic_path(br_pic, org_id, app_path=app_path)

    try:
        shutil.move(src_path, target_path)
    except Exception as e:
        logger.error(e)


def make_qrcode(dbs, url, room_id, user_id):
    room = dbs.query(HasBoardroom).filter(HasBoardroom.id == room_id).first()
    json1 = {
        'url': url,
        'room_id': room.id,
        'room_name': room.name,
        'user_id': user_id,
        'img': {
            'logo': room.logo if room.logo else '',
            'button': room.button_img if room.button_img else '',
            'background': room.background if room.background else ''
        }
    }
    # 设置生成二维码格式
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=4,
    )
    qr.add_data(json1)
    qr.make(fit=True)
    img = qr.make_image()
    img = img.convert("RGBA")
    logo = os.path.abspath('')+'/brms/static/img/logo.png'
    if logo and os.path.exists(logo):
        try:
            icon = Image.open(logo)
            img_w, img_h = img.size
        except Exception as e:
            print(e)
    factor = 4
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)
    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    icon = icon.convert("RGBA")
    img.paste(icon, (w, h), icon)
    buf = BytesIO()
    img.save(buf, 'jpeg')
    image_stream = buf.getvalue()
    return image_stream
