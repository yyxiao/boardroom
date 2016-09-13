#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'cuizc'
__mtime__ = ''
"""
import logging
from datetime import datetime
from pyramid.response import Response
from ..common.dateutils import datetime_format

logger = logging.getLogger('operator')


def request_login(func):
    def _request_login(request):
        try:
            user_name = request.session['userAccount']
            logger.info('[access] \"' + user_name + '\" accessed '+request.path)
        except:
            return Response(status=404)
        return func(request)

    return _request_login


class UserTools(object):

    @staticmethod
    def count_err(user):
        if (0 < user.err_count < 5) and compare_date(user.unlock_time):
            user.err_count = 1
            user.unlock_time = datetime.today().date()
            return
        user.err_count += 1
        if user.err_count >= 5:
            user.unlock_time = get_unlock_time()
            logger.info('[login] \"' + user.user_account + '\" locked. unlock time: ' + user.unlock_time.strftime(
                datetime_format))

    @staticmethod
    def unlock(user):
        if compare_date(user.unlock_time):
            user.err_count = 0
            logger.info('[login] \"' + user.user_account + '\" unlocked.')
            return True
        return False


def get_unlock_time():
    today = datetime.today().date()
    day = today.day
    return datetime.today().date().replace(day=day + 1)


def compare_date(date1, date2=datetime.today().date()):
    print(type(date1))
    if isinstance(date1, datetime):
        return str(date2) >= str(date1.date())
    elif isinstance(date1, datetime.date):
        return str(date2) >= str(date1)