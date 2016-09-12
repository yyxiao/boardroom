# encoding: utf-8
'''
Created on 2016年3月2日

@author: shaoxw
'''
import datetime

date_pattern = '%Y%m%d'  # 日期格式
date_pattern1 = '%Y-%m-%d'  # 日期格式
time_pattern = '%H%M%S'  # 时间模式
datetime_pattern = '%Y%m%d %H%M%S'  # 日期时间模式
datetime_format = '%Y-%m-%d %H:%M:%S' # 标准时间格式

START_QUARTER = '2012-1'


def get_now_quarter():
    '''返回当前季度'''
    dnow = datetime.datetime.now()
    syear = str(dnow.year)
    if (dnow.month >= 1) and (dnow.month <= 3):
        return syear + '-1'
    elif (dnow.month >= 4) and (dnow.month <= 6):
        return syear + '-2'
    elif (dnow.month >= 7) and (dnow.month <= 9):
        return syear + '-3'
    else:
        return syear + '-4'


def get_pre_data_date_quarter(data_date):
    '''返回当前数据日期前一季度'''
    syear = str(data_date[0:4])
    smonth = int(data_date[5:6])
    smonth = smonth - 3
    if (smonth >= 1) and (smonth <= 3):
        return syear + '-1'
    elif (smonth >= 4) and (smonth <= 6):
        return syear + '-2'
    elif (smonth >= 7) and (smonth <= 9):
        return syear + '-3'
    else:
        syear = str(int(syear) - 1)
        return syear + '-4'


def get_welcome():
    ''''''
    dnow = datetime.datetime.now()
    stime = dnow.strftime('%H%M%S')
    if (stime >= '080000') and stime < '120000':
        return '上午好！'
    elif (stime >= '120000') and stime < '140000':
        return '中午好！'
    elif (stime >= '140000') and stime < '180000':
        return '下午好！'
    elif (stime >= '180000') and stime < '240000':
        return '晚上好！'
    else:
        return ''


def date_to_cn(d):
    '''将yyyyMMdd格式的日期转换为"yyyy年MM月dd日"'''
    if d and len(d) == 8:
        return d[0:4] + '年' + d[4:6] + '月' + d[6:] + '日'
    else:
        return ''


def date_now():
    """
    获取当前时间——用于创建时间
    :return:
    """
    dnow = datetime.datetime.now().strftime(datetime_format)
    return dnow


# 获取下一天, 日期格式为:yyyyMMdd
def get_next_date(sdate):
    ddate = datetime.datetime.strptime(sdate, date_pattern1)
    rdate = ddate + datetime.timedelta(days=1)
    return rdate.strftime(date_pattern1)


# 获取前一天, 日期格式为:yyyyMMdd
def get_pre_date(sdate):
    ddate = datetime.datetime.strptime(sdate, date_pattern1)
    ddate.weekday()
    rdate = ddate + datetime.timedelta(days=-1)
    return rdate.strftime(date_pattern)


def get_pre_month_end(sdate):
    '''前一个月最后一天'''
    ddate = datetime.datetime.strptime(sdate[0:6] + '01', date_pattern)
    rdate = ddate + datetime.timedelta(days=-1)
    return rdate.strftime(date_pattern)


def get_month_range():
    '''月范围: 2012-01~2030-12'''
    return ['2012-01', '2012-02', '2012-03', '2012-04', '2012-05', '2012-06', '2012-07', '2012-08', '2012-09',
            '2012-10', '2012-11', '2012-12',
            '2013-01', '2013-02', '2013-03', '2013-04', '2013-05', '2013-06', '2013-07', '2013-08', '2013-09',
            '2013-10', '2013-11', '2013-12',
            '2014-01', '2014-02', '2014-03', '2014-04', '2014-05', '2014-06', '2014-07', '2014-08', '2014-09',
            '2014-10', '2014-11', '2014-12',
            '2015-01', '2015-02', '2015-03', '2015-04', '2015-05', '2015-06', '2015-07', '2015-08', '2015-09',
            '2015-10', '2015-11', '2015-12',
            '2016-01', '2016-02', '2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09',
            '2016-10', '2016-11', '2016-12',
            '2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', '2017-08', '2017-09',
            '2017-10', '2017-11', '2017-12',
            '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09',
            '2018-10', '2018-11', '2018-12',
            '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07', '2019-08', '2019-09',
            '2019-10', '2019-11', '2019-12',
            '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09',
            '2020-10', '2020-11', '2020-12',
            '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09',
            '2021-10', '2021-11', '2021-12',
            '2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06', '2022-07', '2022-08', '2022-09',
            '2022-10', '2022-11', '2022-12',
            '2023-01', '2023-02', '2023-03', '2023-04', '2023-05', '2023-06', '2023-07', '2023-08', '2023-09',
            '2023-10', '2023-11', '2023-12',
            '2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', '2024-07', '2024-08', '2024-09',
            '2024-10', '2024-11', '2024-12',
            '2025-01', '2025-02', '2025-03', '2025-04', '2025-05', '2025-06', '2025-07', '2025-08', '2025-09',
            '2025-10', '2025-11', '2025-12',
            '2026-01', '2026-02', '2026-03', '2026-04', '2026-05', '2026-06', '2026-07', '2026-08', '2026-09',
            '2026-10', '2026-11', '2026-12',
            '2027-01', '2027-02', '2027-03', '2027-04', '2027-05', '2027-06', '2027-07', '2027-08', '2027-09',
            '2027-10', '2027-11', '2027-12',
            '2028-01', '2028-02', '2028-03', '2028-04', '2028-05', '2028-06', '2028-07', '2028-08', '2028-09',
            '2028-10', '2028-11', '2028-12',
            '2029-01', '2029-02', '2029-03', '2029-04', '2029-05', '2029-06', '2029-07', '2029-08', '2029-09',
            '2029-10', '2029-11', '2029-12',
            '2030-01', '2030-02', '2030-03', '2030-04', '2030-05', '2030-06', '2030-07', '2030-08', '2030-09',
            '2030-10', '2030-11', '2030-12', ]


def get_weekday(start_date, end_date, weekday_nums, repeat=None):
    """
    获取一段时间范围内每个周天对应的日期
    :param start_date:
    :param end_date:
    :param weekday_nums: list, 星期对应数字 0 ～ 6
    :param repeat:
    :return:
    """

    sdate = datetime.datetime.strptime(start_date, date_pattern1)
    edate = datetime.datetime.strptime(end_date, date_pattern1)

    if not repeat:
        edate += datetime.timedelta(days=1)

    weekdays = []
    day_delta = 0
    if len(weekday_nums) == 1:
        day_delta = 7
    while sdate < edate:
        for weekday_num in weekday_nums:
            if sdate <= edate:
                now_weekday = sdate.weekday()
                sdate += datetime.timedelta(days=(((int(weekday_num)+6) % 7 - now_weekday + 7) % 7))
                if sdate < edate:
                    weekdays.append(sdate.strftime(date_pattern1))
                    sdate += datetime.timedelta(days=day_delta)
                else:
                    break
    return weekdays


def add_date(max_period):
    """
    计算用户预定范围使用：日期增加、删除
    :param max_period:
    :return:
    """
    u = datetime.datetime.now().strptime(datetime.datetime.now().strftime(date_pattern1),date_pattern1)
    d = datetime.timedelta(days=max_period)
    t = u + d
    return str(t)
