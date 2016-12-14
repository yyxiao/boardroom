#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/8
"""

import random
import base64

_letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper()  # 大写字母
_numbers = ''.join(map(str, range(3, 10)))  # 数字
_special_character = "!@#$%^&*"
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))   # 拼接字符串
length = 8
DEFAULT_PASSWORD = '000000'


def init_password():
    password = random.sample(init_chars, length)
    return ''.join(password)


def get_password(passwd):
    """加密处理"""
    '''password_md5 = crypt.crypt("hycfdps1234",passwd)'''
    password_md5 = base64.encodestring(passwd.encode()).decode('utf-8').replace('\n', '')
    return password_md5