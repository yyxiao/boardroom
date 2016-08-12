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
from datetime import datetime
from ..models.model import SysOrg, HasBoardroom
from ..common.paginator import Paginator


logger = logging.getLogger('operator')


def find_boardrooms(dbs, br_id=None, name=None, config=None, org_id=None, page_no=1):
    '''
    查询符合条件的办公室，返回列表和分页对象
    :param dbs:
    :param br_id:
    :param name:
    :param config:
    :param org_id:
    :param page_no:
    :return:
    '''
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
        boardrooms = boardrooms.filter(HasBoardroom.org_id == org_id)
    if br_id:
        boardrooms = boardrooms.filter(HasBoardroom.id == br_id)

    boardrooms = boardrooms.order_by(HasBoardroom.create_time)
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
    '''
    根据id查找会议室
    :param dbs:
    :param br_id:
    :return:
    '''
    (brs, paginator) = find_boardrooms(dbs, br_id=br_id)
    if len(brs) >= 1:
        return brs[0]
    return None


def add(dbs, boardroom):
    '''
    添加会议室到数据库
    :param dbs:
    :param boardroom:
    :return:
    '''
    try:
        with transaction.manager:
            dbs.add(boardroom)
            dbs.flush()
        return ''
    except Exception as e:
        logger.error(e)
        return '添加会议室失败，请核对后重试'


def update(dbs, boardroom):
    '''
    更新会议室信息到数据库
    :param dbs:
    :param boardroom:
    :return:
    '''
    try:
        with transaction.manager:
            dbs.merge(boardroom)
        msg = ''
    except Exception as e:
        logger.error(e)
        msg = '更新会议室信息失败，请核对后重试'
    return msg


def delete(dbs, br_id):
    '''
    删除会议室
    :param dbs:
    :param br_id:
    :return:
    '''

    try:
        with transaction.manager:
            br = dbs.query(HasBoardroom).filter(HasBoardroom.id == br_id).first()
            if br.picture:
                delete_pic(br.picture, br.org_id)
            dbs.delete(br)

        return ''
    except Exception as e:
        logger.error(e)
        return '删除用户失败！'


def writefile(file, filename, org_id=None):
    '''

    :param file:
    :param filename:
    :param org_id:
    :return:
    '''

    file_path = get_pic_path(filename, org_id)
    try:
        with open(file_path, 'wb') as fp:
            fp.write(file.read())
        msg = ''
    except IOError:
        msg = 'file write error'
    return msg


def delete_pic(filename, org_id=None):
    '''
    删除会议室图片
    :param filename:
    :param org_id:
    :return:
    '''

    file_path = get_pic_path(filename, org_id, create_dirs=False)
    if os.path.exists(file_path):
        os.remove(file_path)


def get_pic_path(filename, org_id=None, create_dirs=True):
    '''

    :param filename:
    :param org_id:
    :param create_dirs:
    :return:
    '''
    # 若org_id为空，则写入到临时目录
    if not org_id:
        org_id = 'tmp'
    else:
        org_id = 'org/' + str(org_id)

    path = os.path.join(os.getcwd(), 'brms/static/img/boardroom/', org_id)
    if create_dirs:
        os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, filename)
    return file_path


def get_save_name(filename):
    '''
    获取文件扩展名
    :param filename:
    :return:
    '''
    name = str(int(datetime.now().timestamp() * 1000000))
    return name + os.path.splitext(filename)[1]


def move_pic(br_pic, org_id):
    '''
    从临时目录移动图片到对应机构下
    :param br_pic:
    :param org_id:
    :return:
    '''
    src_path = get_pic_path(br_pic, create_dirs=False)
    target_path = get_pic_path(br_pic, org_id)

    try:
        shutil.move(src_path, target_path)
    except Exception as e:
        logger.error(e)




