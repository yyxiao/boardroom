#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/8
"""

from ..models.model import *
from ..common.paginator import Paginator
import transaction
import logging

logger = logging.getLogger('operator')


def find_roles(dbs, role_name=None, page_no=1):
    """
    角色列表
    :param dbs:
    :param role_name:
    :param page_no:
    :return:
    """
    roles = dbs.query(SysRole.role_id,
                      SysRole.role_name,
                      SysRole.role_desc,
                      SysUser.user_name,
                      SysRole.create_time)\
        .outerjoin(SysUser, SysUser.id == SysRole.create_user)
    if role_name:
        roles = roles.filter(SysRole.role_name.like('%'+role_name+'%'))
    role_list = roles.order_by(SysRole.create_time)
    if page_no == 0:
        results = role_list.all()
        paginator = None
    else:
        results, paginator = Paginator(role_list, page_no).to_dict()
    lists = []
    for obj in results:
        role_id = obj[0] if obj[0] else ''
        role_name = obj[1] if obj[1] else ''
        role_desc = obj[2] if obj[2] else ''
        create_user = obj[3] if obj[3] else ''
        create_time = obj[4] if obj[4] else ''
        temp_dict = {
            'role_id': role_id,
            'role_name': role_name,
            'role_desc': role_desc,
            'create_user': create_user,
            'create_time': create_time,
        }
        lists.append(temp_dict)
    return lists, paginator


def add(dbs, role):
    error_msg = ''
    try :
        with transaction.manager:
            dbs.add(role)
    except Exception as e:
        logger.error(e)
        error_msg = '新增角色失败，请核对后重试'
    return error_msg


def delete_role(dbs, role_id):
    error_msg = ''
    try:
        with transaction.manager:
            dbs.query(SysRole).filter(SysRole.role_id == role_id).delete()
    except Exception as e:
        logger.error(e)
        error_msg = '删除角色失败，请核对后重试'
    return error_msg


def find_role(dbs, role_id):
    role = dbs.query(SysRole).filter(SysRole.role_id == role_id).first()
    return role


def role_menu(dbs, role_id, create_user, menu_list, now):
    """
    角色授权菜单信息
    :param dbs:
    :param role_id:
    :param create_user:
    :param menu_list:
    :param now:
    :return:
    """
    msg = ''
    try:
        dbs.query(SysRoleMenu).filter(SysRoleMenu.role_id == role_id).delete()
        logger.info("清除角色授权菜单信息成功！")

        for menu_id in menu_list:
            _role_menu = SysRoleMenu(role_id=role_id, menu_id=menu_id, create_user=create_user, create_time=now)
            dbs.merge(_role_menu)
    except Exception as e:
        logger.error(e)
        msg = '角色授权失败，请稍后重试！'
    return msg
