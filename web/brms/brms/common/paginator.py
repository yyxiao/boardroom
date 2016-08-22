#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
__author__ = xyy
__mtime__ = 2016/8/8
"""

import math

PAGESIZE = 10              # 每页显示记录数
PAGINATORSIZE = 5          # 分页插件最多显示页数


class Paginator(object):

    def __init__(self, dbquery, page_no, page_size=PAGESIZE):
        self.page_no = page_no
        self.page_size = page_size
        self.lst, self.page_list, self.pages, self.previous_page, self.next_page = self.paginator(dbquery, page_no)

    def paginator(self, dbquery, page_no):
        """
        分页器，输入为当前页数
        输出结果集，分页插件上显示的页码(list)，上一页页码，下一页页码
        :param dbquery: sqlalchemy查询对象
        :param page_no: 当前页数
        :type page_no: int
        :return: 分页查询结果集,分页插件上显示的页码(list),上一页页码,下一页页码
        """
        (lst, pages) = self.page_search(dbquery, page_no)
        if page_no > pages:
            page_no = pages
        elif page_no <= 0:
            page_no = 1

        if pages <= PAGINATORSIZE:              # 计算分页插件上要显示的页码
            page_list = list(range(1, pages+1))
        elif page_no == 1:
            page_list = list(range(1, PAGINATORSIZE+1))
        elif page_no == pages:
            page_list = list(range(1, pages+1)[pages-PAGINATORSIZE:])
        else:
            page_list = list(range(page_no-1, page_no-1+PAGINATORSIZE))

        if page_no == 1:                        # 计算当前页的下一页与上一页页码
            previous_page = 1
        else:
            previous_page = page_no - 1
        if page_no == pages:
            next_page = pages
        else:
            next_page = page_no + 1
        return lst, page_list, pages, previous_page, next_page

    def page_search(self, dbquery, page_no):
        """
        分页查询
        :param dbquery:
        :param page_no:
        :return:tuple(查询结果集, 总页数)
        """
        total_num = dbquery.count()
        pages = math.ceil(total_num / self.page_size)  # 分页数，向上取整
        pages = 1 if pages == 0 else pages
        if page_no > pages:
            page_no = pages
        elif page_no <= 0:
            page_no = 1
        limit = self.page_size
        offset = (page_no - 1) * self.page_size
        lst = dbquery.limit(limit).offset(offset).all()
        return lst, pages

    def to_dict(self):
        """
        将分页器对象以dict形式返回
        :return:
        """
        paginator = {
            'page_list': self.page_list,
            'page_no': self.page_no,
            'pages': self.pages,
            'previous_page': self.previous_page,
            'next_page': self.next_page,
        }
        return self.lst, paginator
