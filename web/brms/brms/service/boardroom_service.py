#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-10
"""
import os
import shutil
import qrcode
import logging
import transaction
from io import BytesIO
from PIL import Image
from datetime import datetime
from ..common.constant import IMG_RPATH
from ..common.paginator import Paginator
from ..models.model import SysOrg, HasBoardroom
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
                           HasBoardroom.logo,
                           HasBoardroom.button_img,
                           HasBoardroom.background,
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
        logo = obj[3] if obj[3] else ''
        button_img = obj[4] if obj[4] else ''
        background = obj[5] if obj[5] else ''
        config = obj[6] if obj[6] else ''
        description = obj[7] if obj[7] else ''
        org_id = obj[8] if obj[8] else ''
        org_name = obj[9] if obj[9] else ''
        pad_code = obj[10] if obj[10] else ''
        state = obj[11] if obj[11] else ''

        temp_dict = {
            'br_id': br_id,
            'br_name': br_name,
            'picture': picture,
            'logo': logo,
            'button_img': button_img,
            'background': background,
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
            # dbs.flush()
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
                delete_pic(br.picture, app_path)
                delete_pic(br.logo, app_path)
                delete_pic(br.button_img, app_path)
                delete_pic(br.background, app_path)
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


def delete_pic(filename, app_path=None):
    """
    删除会议室图片
    :param filename:
    :param app_path:
    :return:
    """

    if not filename:
        return

    file_path = os.path.join(app_path, 'boardroom_manage/web/brms/brms/', filename)
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


def move_piv_org(old_db_path, new_db_path, app_apth=None):
    """
    会议室机构发生改变时，移动图片到新机构目录下
    :param old_db_path:
    :param new_db_path:
    :param app_apth:
    :return:
    """
    src_path = app_apth + 'boardroom_manage/web/brms/brms/' + old_db_path
    target_path = app_apth + 'boardroom_manage/web/brms/brms/' + new_db_path
    try:
        shutil.move(src_path, target_path)
    except Exception as e:
        logger.error(e)


def update_pic(old_br, new_br):
    """
    图片在不同机构间的移动
    :param old_br:
    :param new_br:
    :return:
    """

    if old_br.picture == new_br.picture:
        new_br.picture = IMG_RPATH + str(new_br.org_id) + '/' + new_br.picture.split('/')[-1]
    if old_br.logo == new_br.logo:
        new_br.logo = IMG_RPATH + str(new_br.org_id) + '/' + new_br.logo.split('/')[-1]
    if old_br.button_img == new_br.button_img:
        new_br.button_img = IMG_RPATH + str(new_br.org_id) + '/' + new_br.button_img.split('/')[-1]
    if old_br.background == new_br.background:
        new_br.background = IMG_RPATH + str(new_br.org_id) + '/' + new_br.background.split('/')[-1]


def make_qrcode(dbs, url, room_id, user_id, app_path):
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
    logo = os.path.join(app_path, 'boardroom_manage/web/brms/brms/static/img/logo.png')
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
