#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-09
"""

import transaction
import logging
from ..models.model import SysUser, SysRole, SysOrg, SysUserRole
from ..common.paginator import Paginator

logger = logging.getLogger('operator')


def find_users(dbs, user_account=None, user_name=None, org_id=None, role_name=None, page_no=1, user_id=None):
    '''
    查找符合条件的用户， 返回用户列表和分页对象
    :param dbs:
    :param user_account:
    :param user_name:
    :param org_id:
    :param role_name:
    :param page_no:
    :param user_id:
    :return:
    '''

    users = dbs.query(SysUser.id,
                      SysUser.user_account,
                      SysUser.user_name,
                      SysOrg.org_name,
                      SysRole.role_name,            # TODO 多角色情况
                      SysUser.max_period,
                      SysUser.user_type,
                      SysUser.email,
                      SysUser.phone,
                      SysUser.position,
                      SysUser.state,
                      SysUser.create_time,
                      SysUser.org_id,) \
        .outerjoin(SysOrg, SysOrg.id == SysUser.org_id)\
        .outerjoin(SysUserRole, SysUser.id == SysUserRole.user_id)\
        .outerjoin(SysRole, SysUserRole.role_id == SysRole.role_id)

    if user_account:
        users = users.filter(SysUser.user_account.like('%' + user_account + '%'))
    if user_name:
        users = users.filter(SysUser.user_name.like('%' + user_name + '%'))
    if org_id:
        users = users.filter(SysUser.org_id == org_id)
    if role_name:
        users = users.filter(SysRole.role_name.like('%' + role_name + '%'))
    if user_id:
        users = users.filter(SysUser.id == user_id)

    user_list = users.order_by(SysUser.create_time)
    results, paginator = Paginator(user_list, page_no).to_dict()
    lists = []
    for obj in results:
        user_id = obj[0] if obj[0] else ''
        user_account = obj[1] if obj[1] else ''
        user_name = obj[2] if obj[2] else ''
        org_name = obj[3] if obj[3] else ''
        role_name = obj[4] if obj[4] else ''
        max_period = obj[5] if obj[5] else ''
        user_type = obj[6] if obj[6] else ''
        email = obj[7] if obj[7] else ''
        phone = obj[8] if obj[8] else ''
        position = obj[9] if obj[9] else ''
        state = obj[10] if obj[10] else ''
        create_time = obj[11] if obj[11] else ''
        org_id = obj[12] if obj[12] else ''
        temp_dict = {
            'user_id': user_id,
            'user_account': user_account,
            'user_name': user_name,
            'org_name': org_name,
            'role_name': role_name,
            'max_period': max_period,
            'user_type': user_type,
            'email': email,
            'phone': phone,
            'position': position,
            'state': state,
            'create_time': create_time,
            'org_id': org_id
        }
        lists.append(temp_dict)
    return lists, paginator


def find_user(dbs, user_id):
    '''
    根据用户id查找用户
    :param dbs:
    :param user_id:
    :return:
    '''
    (users, paginator) = find_users(dbs, user_id=user_id)

    if len(users) >= 1:
        return users[0]
    return None


def add(dbs, user):
    '''
    添加用户
    :param dbs:
    :param user:
    :return:
    '''
    try:
        with transaction.manager:
            dbs.add(user)
            dbs.flush()
        return ''
    except Exception as e:
        logger.error(e)
        return '添加用户失败, 请核对后重试！'


def update(dbs, user):
    '''
    更新用户信息
    :param dbs:
    :param user:
    :return:
    '''
    try:
        with transaction.manager:
            print(user.id)
            user_old = dbs.query(SysUser).filter(SysUser.id == user.id).first()
            if user_old:
                user_old.user_name = user.user_name
                user_old.phone = user.phone
                user_old.address = user.address
                user_old.email = user.email
                user_old.max_period = user.max_period
                user_old.user_type = user.user_type
                user_old.org_id = user.org_id
                user_old.position = user.position
                user_old.state = user.state
        return ''
    except Exception as e:
        logger.error(e)
        return '更新用户失败，请核对后重试！'


def delete(dbs, user_id):
    '''
    删除用户
    :param dbs:
    :param user_id:
    :return:
    '''
    try:
        with transaction.manager:
            dbs.query(SysUser).filter(SysUser.id == user_id).delete()
        return ''
    except Exception as e:
        logger.error(e)
        return '删除用户失败！'


def send_email(address, content):
    '''发送密码到用户email'''
    print(content)
    pass
    # TODO

