#!/usr/bin/env python
# encoding: utf-8

"""
@description: 兴趣推荐

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: interests_recommend.py
@time: 2017/2/14 18:48
"""

from xiaohint.pth import *
from xiaohint.utils.mymysql import MyMysql

mysql = MyMysql()


def recommend(word):
    sql = 'SELECT sid from interests_item where tag = "{}" ORDER BY RAND() limit 1'.format(word)
    sid = mysql.get_one(sql)
    if not sid:
        return None

    logging.info('{} process sid is:{}'.format(word, sid[0]))
    sql2 = 'SELECT tag from interests_item where sid = {} ORDER BY RAND() limit 5;'.format(sid[0])

    return [item[0] for item in mysql.get_many(sql2)]


def main():
    word = '游泳'
    results = recommend(word)
    print(results)


if __name__ == '__main__':
    main()
