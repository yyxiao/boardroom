#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-09
"""

import transaction
import logging
from sqlalchemy.orm import aliased
from ..models.model import SysOrg, SysUser, SysUserOrg
from ..common.paginator import Paginator

logger = logging.getLogger('operator')


def find_branch(dbs, user_org_id=None):
    branches = []
    sql = 'WITH RECURSIVE r AS ( SELECT * FROM brms.sys_org '
    if user_org_id:
        sql += ' WHERE id = %s' % user_org_id
    else:
        sql += ' WHERE id = 1'
    sql += ' union   ALL SELECT sys_org.* FROM brms.sys_org, r WHERE sys_org.parent_id = r.id ) ' \
           'SELECT id,org_name,parent_id FROM r ORDER BY id'
    curs = dbs.execute(sql)
    for rec in curs:
        branch = {}
        branch['org_id'] = rec[0]
        branch['org_name'] = rec[1]
        branches.append(branch)
    return branches


def find_branch_json(dbs, user_org_id=None):
    """
    获取未分配的机构树
    :param dbs:
    :param user_org_id:
    :return:
    """
    branches = []
    sql = 'WITH RECURSIVE r AS ( SELECT * FROM brms.sys_org '
    if user_org_id:
        sql += ' WHERE id = %s' % user_org_id
    else:
        sql += ' WHERE id = 1'
    sql += ' union   ALL SELECT sys_org.* FROM brms.sys_org, r WHERE sys_org.parent_id = r.id ) ' \
           'SELECT id,org_name,parent_id FROM r ORDER BY id'
    curs = dbs.execute(sql)
    for rec in curs:
        branch = {}
        branch['id'] = rec[0]
        branch['name'] = rec[1]
        branch['pId'] = rec[2]
        if rec[2] == 0:
            branch['open'] = True
        branches.append(branch)
    return branches


def find_branch_json_check(dbs, user_id):
    """
    获取机构树
    :param dbs:
    :param user_id:
    :return:
    """
    branches = []
    orgs = dbs.query(SysOrg.id, SysOrg.org_name, SysOrg.parent_id).all()
    curs = dbs.query(SysUserOrg.org_id).filter(SysUserOrg.user_id == user_id).all()
    for rec in orgs:
        branch = {}
        branch['id'] = rec[0]
        branch['name'] = rec[1]
        branch['pId'] = rec[2]
        if rec[2] == 0:
            branch['open'] = True
        for org in curs:
            if rec[0] == org[0]:
                branch['checked'] = True
        branches.append(branch)
    return branches


def find_orgs(dbs, org_name=None, parent_id=None, address=None, org_id=None, page_no=1):
    """
    查询org列表
    :param dbs:
    :param org_name:
    :param parent_id:
    :param address:
    :param org_id:
    :param page_no:
    :return:
    """
    sysorg1 = aliased(SysOrg)
    orgs = dbs.query(SysOrg.id,
                     SysOrg.org_name,
                     SysOrg.org_type,
                     sysorg1.org_name,
                     SysOrg.org_manager,
                     SysOrg.phone,
                     SysOrg.address,
                     SysOrg.state,
                     SysUser.user_name,
                     SysOrg.create_time)\
        .outerjoin(SysUser, SysUser.id == SysOrg.create_user)\
        .outerjoin(sysorg1, SysOrg.parent_id == sysorg1.id)

    if org_name:
        orgs = orgs.filter(SysOrg.org_name.like('%' + org_name + '%'))
    if parent_id:
        orgs = orgs.filter(SysOrg.parent_id == parent_id)
    if address:
        orgs = orgs.filter(SysOrg.address.like('%' + address + '%'))
    if org_id:
        orgs = orgs.filter(SysOrg.id == org_id)

    orgs = orgs.order_by(SysOrg.create_time)
    results, paginator = Paginator(orgs, page_no).to_dict()
    lists = []
    for obj in results:
        id = obj[0] if obj[0] else ''
        org_name = obj[1] if obj[1] else ''
        org_type = obj[2] if obj[2] else ''
        parent_name = obj[3] if obj[3] else ''
        org_manager = obj[4] if obj[4] else ''
        phone = obj[5] if obj[5] else ''
        address = obj[6] if obj[6] else ''
        state = obj[7] if obj[7] else ''
        user_name = obj[8] if obj[8] else ''
        create_time = obj[9] if obj[9] else ''
        temp_dict = {
            'id': id,
            'org_name': org_name,
            'org_type': org_type,
            'parent_name': parent_name,
            'org_manager': org_manager,
            'phone': phone,
            'address': address,
            'state': state,
            'user_name': user_name,
            'create_time': create_time
        }
        lists.append(temp_dict)
    return lists, paginator


def find_org(dbs, org_id):
    '''

    :param dbs:
    :param org_id:
    :return:
    '''
    (orgs, paginator) = find_orgs(dbs, org_id=org_id)
    if len(orgs) >= 1:
        return orgs[0]
    return None


def find_org_by_id(dbs, org_id):
    '''

    :param dbs:
    :param org_id:
    :return:
    '''
    user = dbs.query(SysOrg).filter(SysOrg.id == org_id).first()
    if user:
        return user
    else:
        return None


def add(dbs, org):
    '''
    添加机构
    :param dbs:
    :param org:
    :return:
    '''
    try:
        with transaction.manager:
            dbs.add(org)
            dbs.flush()
        return ''
    except Exception as e:
        logger.error(e)
        return '添加机构失败，请重试！'


def update(dbs, org):
    '''
    更新机构信息
    :param dbs:
    :param org:
    :return:
    '''
    try:
        with transaction.manager:
            dbs.merge(org)
            dbs.flush()
        return ''
    except Exception as e:
        logger.error(e)
        return '更新机构信息失败，请重试！'


def delete(dbs, org_id):
    '''
    删除机构
    :param dbs:
    :param org_id:
    :return:
    '''
    try:
        with transaction.manager:
            dbs.query(SysOrg).filter(SysOrg.id == org_id).delete()
            dbs.flush()
        return ''
    except Exception as e:
        logger.error(e)
        return '删除机构失败，请重试！'











