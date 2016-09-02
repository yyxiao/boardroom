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
from ..common.dateutils import date_now
from ..common.paginator import Paginator

logger = logging.getLogger('operator')


def find_branch(dbs, user_org_id=None, org_type=None):
    """
    获取机构列表
    :param dbs:
    :param user_org_id:
    :param org_type:0公司，1部门
    :return:
    """
    branches = []
    sql = 'WITH RECURSIVE r AS ( SELECT * FROM brms.sys_org '
    if user_org_id:
        sql += ' WHERE id = %s' % user_org_id
    else:
        sql += ' WHERE id = 1'
    sql += ' union   ALL SELECT sys_org.* FROM brms.sys_org, r WHERE sys_org.parent_id = r.id '
    if org_type:
        sql += ' and sys_org.org_type = \'' + org_type + '\''
    sql += ') SELECT id,org_name,parent_id FROM r ORDER BY id'
    curs = dbs.execute(sql)
    for rec in curs:
        branch = {}
        branch['org_id'] = rec[0]
        branch['org_name'] = rec[1]
        branches.append(branch)
    return branches


def find_branch_json(dbs, user_org_id=None, org_type=None):
    """
    获取未分配的机构树
    :param dbs:
    :param user_org_id:
    :param org_type:0公司，1部门
    :return:
    """
    branches = []
    sql = 'WITH RECURSIVE r AS ( SELECT * FROM brms.sys_org '
    if user_org_id:
        sql += ' WHERE id = %s' % user_org_id
    else:
        sql += ' WHERE id = 1'
    sql += ' union   ALL SELECT sys_org.* FROM brms.sys_org, r WHERE sys_org.parent_id = r.id '
    if org_type:
        sql += ' and sys_org.org_type = \'' + org_type + '\''
    sql += ') SELECT id,org_name,parent_id FROM r ORDER BY id'
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


def find_branch_json_check(dbs, user_id, user_now=None):
    """
    获取机构树
    :param dbs:
    :param user_id:
    :param user_now:
    :return:
    """
    branches = []
    orgs = dbs.query(SysOrg.id, SysOrg.org_name, SysOrg.parent_id).all()
    # 当前的登录用户可分配的机构
    user_orgs = dbs.query(SysUserOrg.org_id).filter(SysUserOrg.user_id == user_now).all()
    user_org_list = []
    for rec in user_orgs:
        user_org_list.append(rec[0])
    user_tuple = tuple(user_org_list)
    # 当前勾选的用户已分配的机构
    curs = dbs.query(SysUserOrg.org_id).filter(SysUserOrg.user_id == user_id).all()
    for rec in orgs:
        branch = {}
        branch['id'] = rec[0]
        branch['name'] = rec[1]
        branch['pId'] = rec[2]
        if rec[2] == 0:
            branch['open'] = True
        if rec[0] in user_tuple:
            branch['doCheck'] = True
        else:
            branch['doCheck'] = False
            branch['name'] += '(不可选)'
        for org in curs:
            if rec[0] == org[0]:
                branch['checked'] = True
        branches.append(branch)
    return branches


def find_branch_json_4booking(dbs, user_id, user_org_id):
    """
    获取机构树
    :param dbs:
    :param user_id:
    :param user_org_id:
    :return:
    """
    user_orgs = dbs.query(SysUserOrg.org_id)\
        .outerjoin(SysOrg, SysOrg.id == SysUserOrg.org_id)\
        .filter(SysUserOrg.user_id == user_id, SysOrg.org_type == '0').all()
    orgs_ids = [i.org_id for i in user_orgs]

    user_orgs = dbs.query(SysOrg.id, SysOrg.org_name, SysOrg.parent_id).filter(SysOrg.id.in_(orgs_ids)).all()
    org_dict = {}
    for org in user_orgs:
        branch = dict()
        branch['id'] = org[0]
        branch['name'] = org[1]
        branch['pId'] = org[2]
        branch['doCheck'] = True
        if org[2] == 0:
            branch['open'] = True
        if org[0] == user_org_id:
            branch['checked'] = True
        org_dict[org[0]] = branch
    for org_id in orgs_ids:
        find_parents(dbs, org_dict[org_id]['pId'], org_dict, is_open=(org_id == user_org_id))

    return [v for k, v in org_dict.items()]


def find_parents(dbs, parent_id, org_dict, is_open=False):
    """
    查找父机构并加入到字典中
    :param dbs:
    :param parent_id:
    :param org_dict:
    :param is_open:
    :return:
    """
    if parent_id == 0 or parent_id in org_dict.keys():
        return
    org = dbs.query(SysOrg.id, SysOrg.org_name, SysOrg.parent_id).filter(SysOrg.id == parent_id).first()
    branch = dict()
    branch['id'] = org[0]
    branch['name'] = org[1] + '(不可选)'
    branch['pId'] = org[2]
    branch['chkDisabled'] = True
    branch['open'] = is_open
    org_dict[parent_id] = branch
    if org[2] == 0:
        return
    find_parents(dbs, org[2], org_dict, is_open)
    return


def find_orgs(dbs, org_name=None, parent_id=None, address=None, org_id=None, page_no=1, show_child=True):
    """
    查询org列表
    :param dbs:
    :param org_name:
    :param parent_id:
    :param address:
    :param org_id:
    :param page_no:
    :param show_child:
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
                     SysOrg.create_time) \
        .outerjoin(SysUser, SysUser.id == SysOrg.create_user) \
        .outerjoin(sysorg1, SysOrg.parent_id == sysorg1.id)

    if org_id:
        if show_child:
            tmp = find_branch_json(dbs, org_id)
            child_org = list(map((lambda x: x['id']), tmp))
            orgs = orgs.filter(SysOrg.id.in_(child_org))
        else:
            orgs = orgs.filter(SysOrg.id == org_id)
    if org_name:
        orgs = orgs.filter(SysOrg.org_name.like('%' + org_name + '%'))
    if parent_id:
        orgs = orgs.filter(SysOrg.parent_id == parent_id)
    if address:
        orgs = orgs.filter(SysOrg.address.like('%' + address + '%'))

    orgs = orgs.order_by(SysOrg.create_time.desc())
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
    org = dbs.query(SysOrg).filter(SysOrg.id == org_id).first()
    if org:
        return org
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
        dbs.add(org)
        dbs.flush()
        sys_user_org = SysUserOrg(user_id=org.create_user, org_id=org.id, create_user=org.create_user,
                                  create_time=date_now())
        dbs.merge(sys_user_org)
        sys_user_org = SysUserOrg(user_id=1, org_id=org.id, create_user=org.create_user,
                                  create_time=date_now())
        dbs.merge(sys_user_org)
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
            dbs.query(SysUserOrg).filter(SysUserOrg.org_id == org_id).delete()
            dbs.flush()
        return ''
    except Exception as e:
        logger.error(e)
        return '删除机构失败，请重试！'


def find_org_ids(dbs, user_org_id):
    """
    获取当前用户所属机构及下属机构id
    :param dbs:
    :param user_org_id:
    :return:
    """
    branches = []  # 获取当前用户所属机构及下属机构id
    sql = 'WITH RECURSIVE r AS ( SELECT * FROM brms.sys_org '
    if user_org_id:
        sql += ' WHERE id = %s' % user_org_id
    else:
        sql += ' WHERE id = 1'
    sql += ' union ALL SELECT sys_org.* FROM brms.sys_org, r WHERE sys_org.parent_id = r.id ) ' \
           'SELECT id,org_name,parent_id FROM r ORDER BY id'
    orgs = dbs.execute(sql)
    for rec in orgs:
        branches.append(rec[0])
    return branches