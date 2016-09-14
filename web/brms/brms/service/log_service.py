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
        HyLog.operator_logger.info('[login] ip:'+ip+' \"'+user_account+'\" login '+msg+'.')

    @staticmethod
    def log_out(ip, user_account):
        HyLog.operator_logger.info(('[logout] ip:'+ip+' \"'+user_account+'\" logout.'))

    @staticmethod
    def log_access(ip, user_account, url):
        HyLog.operator_logger.info('[access] ip:'+ip+' \"'+user_account+'\" accessed '+url)

    @staticmethod
    def log_query(ip, user_account, msg='', research_type=''):
        HyLog.operator_logger.info('[research]['+research_type+'] ip:'+ip+' \"'+user_account+'\"'+msg)

    @staticmethod
    def log_add(ip, user_account, msg='', add_type=''):
        HyLog.operator_logger.info('[add]['+add_type+'] ip:'+ip+' \"'+user_account+'\"'+msg)

    @staticmethod
    def log_update(ip, user_account, msg='', update_type=''):
        HyLog.operator_logger.info('[update]['+update_type+'] ip:'+ip+' \"'+user_account+'\"'+msg)

    @staticmethod
    def log_delete(ip, user_account, msg='', delete_type=''):
        HyLog.operator_logger.info('[delete][' + delete_type + '] ip:' + ip + ' \"' + user_account + '\"' + msg)

