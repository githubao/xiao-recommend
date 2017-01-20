#!/usr/bin/env python
# encoding: utf-8

"""
@description: 姓名挖掘

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: namemining.py
@time: 2017/1/20 18:12
"""

import json
import os
import re

from xiaohint.pth import *
from collections import defaultdict

chinese = re.compile('^[\u4e00-\u9fa5]')

root_path = '{}/renren'.format(FILE_PATH)

fuxing = None


def name_cnt():
    '''
    统计人名和姓名的个数
    '''

    first_cnt = defaultdict(int)
    last_dic = defaultdict(dict)

    for file in os.listdir(root_path):
        full_path = os.path.join(root_path, file)
        with open(full_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                json_data = json.loads(line)
                name = json_data['name']

                if not name or len(name) < 2 or len(name) > 4:
                    continue

                m = chinese.search(name)
                if not m:
                    continue

                if len(name) > 2:
                    fu_name = ''.join(name[:2])
                    if fu_name in fuxing:
                        first_name = ''.join(name[:2])
                        last_name = ''.join(name[2:])
                    else:
                        first_name = name[0]
                        last_name = ''.join(name[1:])

                if first_name and last_name:
                    first_cnt[first_name] += 1
                    last_dic[first_name].setdefault(last_name, 0)
                    last_dic[first_name][last_name] += 1

    # last_dic = {key: list(value) for key, value in last_dic.items()}
    #
    # sorted_first = sorted(first_cnt.items(), key=lambda x: x[1], reverse=True)
    # sorted_last = sorted(last_dic.items(), key=lambda x: x[1][1], reverse=True)
    #
    # print(sorted_first)
    # print(sorted_last)

    sort_name(first_cnt, last_dic)


def sort_name(first_cnt, last_dic):
    sorted_first = sorted(first_cnt.items(), key=lambda x: x[1], reverse=True)
    for k, v in sorted_first:
        print('{}\t{}'.format(k, v))
        name_dic = last_dic.get(k)
        sorted_last = sorted(name_dic.items(), key=lambda x: x[1], reverse=True)
        for ck, cv in sorted_last:
            print('\t{}\t{}'.format(ck, cv))
        print('*' * 20)


def load_fuxing():
    global fuxing
    with open('{}/fuxing.txt'.format(FILE_PATH), 'r', encoding='utf-8') as f:
        line = f.readline()
        fuxing = line.strip().split('|')


if not fuxing:
    load_fuxing()


def main():
    name_cnt()


if __name__ == '__main__':
    main()
