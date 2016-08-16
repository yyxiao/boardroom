#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-16
"""

from ..models.model import SysMenu, SysRole, SysRoleMenu, SysUserRole


def get_user_menu(dbs, user_id):
    '''
    根据用户id查找用户菜单
    :param dbs:
    :param user_id:
    :return:
    '''

    menus = dbs.query(SysMenu).filter(SysMenu.id == SysRoleMenu.menu_id,
                                      SysRoleMenu.role_id == SysRole.role_id,
                                      SysRole.role_id == SysUserRole.role_id,
                                      SysUserRole.user_id == user_id).all()

    return menus
