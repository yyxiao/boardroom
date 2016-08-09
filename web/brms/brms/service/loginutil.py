#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'cuizc'
__mtime__ = ''
"""
from datetime import datetime
from pyramid.httpexceptions import HTTPFound


def request_login(func):
    def _request_login(request):
        try:
            user_name = request.session['userAccount']
        except:
            return HTTPFound(request.route_url('login'))
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

    @staticmethod
    def unlock(user):
        if compare_date(user.unlock_time):
            user.err_count = 0
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