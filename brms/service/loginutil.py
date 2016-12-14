#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'cuizc'
__mtime__ = ''
"""

import string
from datetime import datetime
from pyramid.response import Response
from ..common.dateutils import datetime_format
from ..service.log_service import HyLog


def request_login1(event):
    try:
        if event.request.path.find('/static/') == -1:
            user_name = event.request.session['userAccount']
            print(event.request.path)
            print(user_name)
    except:
        print("not login")


def request_login(func):
    def _request_login(request):
        try:
            user_name = request.session['userAccount']
            HyLog.log_access(request.client_addr, user_name, request.path)
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
            HyLog.log_in('', user.user_account,
                         'failed, user locked, unlock time: ' + user.unlock_time.strftime(datetime_format))

    @staticmethod
    def unlock(user):
        if compare_date(user.unlock_time):
            user.err_count = 0
            HyLog.log_in('', user.user_account, 'success, user unlocked')
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