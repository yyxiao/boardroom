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


def find_menu_json_check(dbs, role_id):
    """
    获取菜单树
    :param dbs:
    :param role_id:
    :return:
    """
    menu_branches = []
    menus = dbs.query(SysMenu.id, SysMenu.name, SysMenu.parent_id).all()
    curs = dbs.query(SysRoleMenu.menu_id).filter(SysRoleMenu.role_id == role_id).all()
    for rec in menus:
        branch = {}
        branch['id'] = rec[0]
        branch['name'] = rec[1]
        branch['pId'] = rec[2]
        if rec[2] == 0:
            branch['open'] = True
        for menu in curs:
            if rec[0] == menu[0]:
                branch['checked'] = True
        menu_branches.append(branch)
    return menu_branches
