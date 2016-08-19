#!/usr/bin/env python3.4
# -*- coding: utf-8 -*-
"""
__author__ = cuizc
__mtime__ = 2016-08-18
"""

from functools import reduce
from ..models.model import HasBoardroom, HasMeeting, HasMeetBdr


def compare_bin(mt_bin, br_bin):
    '''
    比较二进制判断是否有重复
    :param mt_bin: 会议时间范围对应二进制数
    :param br_bin: 会议室已占用时间范围二进制数
    :return: result: 0 有冲突, 此时flag才有意义;
                     other 新的二进制数;
             flag:   -1 开始时间冲突;
                     0 全部时间冲突;
                     1 结束时间冲突;
    '''
    if isinstance(mt_bin, str):
        mt_bin = int(mt_bin)
    if isinstance(br_bin, str):
        br_bin = int(br_bin)

    flag = mt_bin & br_bin
    result = 0
    if mt_bin == br_bin or flag == mt_bin or flag == br_bin:
        flag = 0
    elif flag:
        if flag < mt_bin < br_bin:
            flag = 1
        elif flag < br_bin < mt_bin:
            flag = -1
    else:
        result = mt_bin | br_bin
    return result, flag


def delete_bin(mt_bin, br_bin):
    '''
    删除会议时,清除此会议的占用值
    :param mt_bin:
    :param br_bin:
    :return:
    '''

    result, flag = compare_bin(mt_bin, br_bin)
    return (mt_bin ^ br_bin) if flag == 0 else br_bin


def get_binary(start_time, end_time, start=7, hours=14):
    '''
    根据时间范围生成梳型二进制数对应整形数
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param start: 允许预订的最早时间
    :param hours: 允许预订的时间长度
    :return: -1: 超出时间范围, other int:
    '''

    s_h, s_m = start_time.split(':')
    e_h, e_m = end_time.split(':')

    left = (int(s_h) - start) * 2 + (int(s_m) // 30)
    right = (int(e_h) - start) * 2 + (int(e_m) // 30)

    if left < 0 or (right > hours * 2):
        return -1

    binary = reduce((lambda x, y: x + 2 ** y), range(left, right), 0)
    return binary
