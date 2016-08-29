#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-09
"""

import transaction
import logging
from ..models.model import *
from ..common.paginator import Paginator
from ..common.dateutils import date_now
from .org_service import find_branch_json

logger = logging.getLogger('operator')


def find_users(dbs, org_id=None, user_account=None, user_name=None, role_name=None, page_no=1, user_id=None, show_child=True):
    '''
    查找符合条件的用户， 返回用户列表和分页对象
    :param dbs:
    :param org_id:
    :param user_account:
    :param user_name:
    :param role_name:
    :param page_no:
    :param user_id:
    :param show_child:
    :return:
    '''

    users = dbs.query(SysUser.id,
                      SysUser.user_account,
                      SysUser.user_name,
                      SysOrg.org_name,
                      SysRole.role_name,
                      SysUser.max_period,
                      SysUser.user_type,
                      SysUser.email,
                      SysUser.phone,
                      SysUser.position,
                      SysUser.state,
                      SysUser.create_time,
                      SysUser.org_id,
                      SysRole.role_id,) \
        .outerjoin(SysOrg, SysOrg.id == SysUser.org_id)\
        .outerjoin(SysUserRole, SysUser.id == SysUserRole.user_id)\
        .outerjoin(SysRole, SysUserRole.role_id == SysRole.role_id)

    if org_id:
        if show_child:
            tmp = find_branch_json(dbs, org_id)
            child_org = list(map((lambda x: x['id']), tmp))
            users = users.filter(SysUser.org_id.in_(child_org))
        else:
            users = users.filter(SysUser.org_id == org_id)

    if user_account:
        users = users.filter(SysUser.user_account.like('%' + user_account + '%'))
    if user_name:
        users = users.filter(SysUser.user_name.like('%' + user_name + '%'))

    if role_name:
        users = users.filter(SysRole.role_name.like('%' + role_name + '%'))
    if user_id:
        users = users.filter(SysUser.id == user_id)

    user_list = users.order_by(SysUser.create_time.desc())
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
        role_id = obj[13] if obj[13] else ''
        temp_dict = {
            'user_id': user_id,
            'user_account': user_account,
            'user_name': user_name,
            'org_name': org_name,
            'role_name': role_name,
            'role_id': role_id,
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
    根据用户id查找用户, 返回用户信息字典对象
    :param dbs:
    :param user_id:
    :return:
    '''
    (users, paginator) = find_users(dbs, user_id=user_id)

    if len(users) >= 1:
        return users[0]
    return None


def find_user_by_id(dbs, user_id):
    '''
    根据用户id查找用户，返回用户模型对象
    :param dbs:
    :param user_id:
    :return:
    '''
    user = dbs.query(SysUser).filter(SysUser.id == user_id).first()
    if user:
        return user
    return None


def add(dbs, user, role_id=None, create_user=None):
    '''
    添加用户
    :param dbs:
    :param user:
    :param role_id:
    :param create_user:
    :return:
    '''
    try:
        dbs.add(user)
        dbs.flush()
        sys_user_org = SysUserOrg(user_id=user.id, org_id=user.org_id, create_user=create_user, create_time=date_now())
        dbs.merge(sys_user_org)
        if role_id != '' and role_id != 0:
            user_role = SysUserRole()
            user_role.user_id = user.id
            user_role.create_user = create_user
            user_role.create_time = date_now()
            user_role.role_id = role_id
            dbs.add(user_role)
        return ''
    except Exception as e:
        logger.error(e)
        return '添加用户失败, 请核对后重试！'


def update(dbs, user, role_id=None, create_user=None):
    '''
    更新用户信息
    :param dbs:
    :param user:
    :param role_id:
    :param create_user:
    :return:
    '''
    try:
        with transaction.manager:
            dbs.merge(user)
            sys_user_org = SysUserOrg(user_id=user.id, org_id=user.org_id, create_user=create_user,
                                      create_time=date_now())
            dbs.merge(sys_user_org)
            if role_id != '' and role_id != 0:
                user_role = dbs.query(SysUserRole).filter(SysUserRole.user_id == user.id).first()
                if not user_role:
                    user_role = SysUserRole()
                    user_role.user_id = user.id
                    user_role.create_user = create_user
                    user_role.create_time = date_now()
                user_role.role_id = role_id
                dbs.add(user_role)
        return ''
    except Exception as e:
        logger.error(e)
        return '更新用户失败，请核对后重试！'


def delete(dbs, user_id):
    """
    删除用户
    :param dbs:
    :param user_id:
    :return:
    """
    try:
        with transaction.manager:
            dbs.query(SysUser).filter(SysUser.id == user_id).delete()
        return ''
    except Exception as e:
        logger.error(e)
        return '删除用户失败！'


def send_email(address, content):
    """
    发送密码到用户email
    :param address:
    :param content:
    :return:
    """
    print(content)
    pass
    # TODO


def user_checking(dbs, pad_code, user_id):
    """
    验证用户是否可以使用该pad申请会议
    :param dbs:
    :param pad_code:
    :param user_id:
    :return:
    """
    msg = ''
    try:
        orgs = dbs.query(HasBoardroom, SysUserOrg.org_id) \
            .outerjoin(SysUserOrg, SysUserOrg.org_id == HasBoardroom.org_id) \
            .outerjoin(SysUser, SysUser.id == SysUserOrg.user_id)\
            .outerjoin(HasPad, HasBoardroom.pad_id == HasPad.id)
        if user_id:
            orgs.filter(SysUser.id == user_id)
        if pad_code:
            org_list = orgs.filter(HasPad.pad_code == pad_code).all()
        # if not org_list:
        #     msg = '该pad没有匹配会议室，请稍后重试！'
    except Exception as e:
        logger.error(e)
        msg = '验证用户失败！'
    return msg


def user_org(dbs, user_id, create_user, org_list, now):
    """
    用户授权机构信息
    :param dbs:
    :param user_id:
    :param create_user:
    :param org_list:
    :param now:
    :return:
    """
    msg = ''
    try:
        dbs.query(SysUserOrg).filter(SysUserOrg.user_id == user_id).delete()
        logger.info("清除用户授权机构信息成功！")
        for org_id in org_list:
            userorg = SysUserOrg(user_id=user_id, org_id=org_id, create_user=create_user, create_time=now)
            dbs.merge(userorg)
    except Exception as e:
        logger.error(e)
        msg = '用户授权失败，请稍后重试！'
    return msg
