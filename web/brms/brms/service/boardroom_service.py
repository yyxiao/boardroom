#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-10
"""
from ..models.model import SysOrg, HasBoardroom
from ..common.paginator import Paginator


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
            'picture': picture,
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


