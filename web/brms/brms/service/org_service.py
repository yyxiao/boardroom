#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-09
"""

from ..models.model import SysOrg


def find_branch(dbs):
    branches = []
    curs = dbs.query(SysOrg.id, SysOrg.org_name)
    for rec in curs:
        branch = {}
        branch['org_id'] = rec[0]
        branch['org_name'] = rec[1]
        branches.append(branch)
    return branches

