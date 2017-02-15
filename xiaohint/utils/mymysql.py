#!/usr/bin/env python
# encoding: utf-8

"""
@description: mysql 的操作接口

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: mymysql.py
@time: 2017/2/14 18:29
"""

import pymysql


class MyMysql():
    url = 'mysql://root:00@127.0.0.1:3306'

    def __init__(self):
        self.client = pymysql.connect('127.0.0.1', 'root', 'Full77', 'nlp_xiao', charset='utf8')

    def get_one(self, sql):
        cursor = self.client.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        return data

    def get_many(self, sql):
        cursor = self.client.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        return data

    def close(self):
        self.client.close()


def test_mysql():
    mysql = MyMysql()
    sql = 'SELECT sid from interests_item where tag = "篮球" ORDER BY RAND() limit 1'
    print(mysql.get_one(sql))


def main():
    test_mysql()


if __name__ == '__main__':
    main()
