#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-09-14
"""

import logging


class HyLog(object):
    operator_logger = logging.getLogger(__name__)

    @staticmethod
    def log_in(ip, user_account, msg=''):
        HyLog.log_info('[login] ip:' + ip + ' \"' + user_account + '\" login ' + msg + '.')

    @staticmethod
    def log_out(ip, user_account):
        HyLog.log_info(('[logout] ip:' + ip + ' \"' + user_account + '\" logout.'))

    @staticmethod
    def log_access(ip, user_account, url):
        HyLog.log_info('[access] ip:' + ip + ' \"' + user_account + '\" accessed ' + url)

    @staticmethod
    def log_research(ip, user_account, msg='', research_type=''):
        HyLog.log_info('[research][' + research_type + '] ip:' + ip + ' \"' + user_account + '\"' + msg)

    @staticmethod
    def log_add(ip, user_account, msg='', add_type=''):
        HyLog.log_info('[add][' + add_type + '] ip:' + ip + ' \"' + user_account + '\"' + msg)

    @staticmethod
    def log_update(ip, user_account, msg='', update_type=''):
        HyLog.log_info('[update][' + update_type + '] ip:' + ip + ' \"' + user_account + '\"' + msg)

    @staticmethod
    def log_delete(ip, user_account, msg='', delete_type=''):
        HyLog.log_info('[delete][' + delete_type + '] ip:' + ip + ' \"' + user_account + '\"' + msg)

    @staticmethod
    def log_auth(ip, user_account, authed_user, authority, auth_type):
        HyLog.log_info('[auth][' + auth_type + '] ip:' + ip + ' \"' + user_account + '\" licensed to \"' + authed_user + '\" with authority:' + authority)

    @staticmethod
    def log_error(msg):
        HyLog.operator_logger.error(msg)

    @staticmethod
    def log_warn(msg):
        HyLog.operator_logger.warn(msg)

    @staticmethod
    def log_info(msg):
        HyLog.operator_logger.info(msg)
