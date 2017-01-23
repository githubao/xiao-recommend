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

chinese = re.compile('[\u4e00-\u9fa5]')

root_path = '{}/renren'.format(FILE_PATH)
out_path = '{}/name.txt'.format(root_path)
err_path = '{}/err.txt'.format(root_path)

fuxing = None
firstnames = None

MIN_ALLOW = 5


def name_cnt():
    '''
    统计人名和姓名的个数
    '''

    first_cnt = defaultdict(int)
    last_cnt = defaultdict(int)
    last_dic = defaultdict(dict)

    for file_name in os.listdir(root_path):
        full_path = os.path.join(root_path, file_name)

        if not file_name.endswith('json'):
            continue

        logging.info('process file: {}'.format(full_path))
        cnt = 0
        with open(full_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                json_data = json.loads(line)
                name = json_data['name']

                if not name or len(name) < 2 or len(name) > 4:
                    continue

                m = chinese.match(name)
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
                    last_cnt[last_name] += 1

                    last_dic[first_name].setdefault(last_name, 0)
                    last_dic[first_name][last_name] += 1

                cnt += 1
                if cnt % 1000 == 0:
                    logging.info('process cnt: {}'.format(cnt))

    # last_dic = {key: list(value) for key, value in last_dic.items()}
    #
    # sorted_first = sorted(first_cnt.items(), key=lambda x: x[1], reverse=True)
    # sorted_last = sorted(last_dic.items(), key=lambda x: x[1][1], reverse=True)
    #
    # print(sorted_first)
    # print(sorted_last)

    name_sorted = sort_name(first_cnt, last_cnt, last_dic)
    with open(out_path, 'w', encoding='utf-8') as fw, open(err_path, 'w', encoding='utf-8') as ferr:
        for item in name_sorted:
            # if not item['first'] in firstnames:
            if is_not_name(item):
                ferr.write('{}\n'.format(json.dumps(item,ensure_ascii=False,sort_keys=True)))
            else:
                fw.write('{}\n'.format(json.dumps(item,ensure_ascii=False,sort_keys=True)))


def sort_name(first_cnt, last_cnt, last_dic):
    name_list = []
    for k, v in first_cnt.items():
        for ck, cv in last_dic[k].items():
            dic = {}
            dic['first'] = k
            dic['first_cnt'] = v
            dic['last'] = ck
            dic['last_total_cnt'] = last_cnt[ck]
            dic['last_this_cnt'] = cv
            dic['name'] = '{}{}'.format(k, ck)
            name_list.append(dic)

    # 低于某个阈值的数据不要
    # name_list.sort(key=lambda x: x['first_cnt'], reverse=True)
    # first_threshold = name_list[int(9 / 10 * len(name_list))]['first_cnt']
    # name_list.sort(key=lambda x: x['last_cnt'], reverse=True)
    # last_threshold = name_list[int(9 / 10 * len(name_list))]['last_cnt']
    # name_list = list(filter(lambda x: x['first_cnt'] >= first_threshold and x['last_cnt'] >= last_threshold, name_list))

    # 数据归一化
    # first_sum = sum(name['first_cnt'] for name in name_list)
    # last_sum = sum(name['last_cnt'] for name in name_list)
    # for item in name_list:
    #     item['score'] = 0.2 * item['first_cnt'] / first_sum + 0.8 * item['last_cnt'] / last_sum
    #     # item['score'] = item['last_cnt'] / last_sum
    #
    # # 分值表示成0-100
    # score_max = max(name['score'] for name in name_list)
    # score_min = min(name['score'] for name in name_list)
    #
    # for item in name_list:
    #     item['score'] = float('{:.5f}'.format(100 * (item['score'] - score_min) / (score_max - score_min)))

    # 按照分值排序
    # name_list.sort(key=lambda x: x['score'], reverse=True)

    first_set = defaultdict(set)
    last_set = defaultdict(set)
    for item in name_list:
        first_set[item['first']].add(item['last'])
        last_set[item['last']].add(item['first'])

    for item in name_list:
        item['first_ref'] = len(first_set[item['first']])
        item['last_ref'] = len(last_set[item['last']])

    # 多少个姓都用了这个名字
    name_list.sort(key=lambda x: x['last_ref'], reverse=True)

    return name_list


def sort_name_2(first_cnt, last_dic):
    sorted_first = sorted(first_cnt.items(), key=lambda x: x[1], reverse=True)
    for k, v in sorted_first:
        print('{}\t{}'.format(k, v))
        name_dic = last_dic.get(k)
        sorted_last = sorted(name_dic.items(), key=lambda x: x[1], reverse=True)
        for ck, cv in sorted_last:
            print('\t{}\t{}'.format(ck, cv))
        print('*' * 20)


def is_not_name(item):
    return less_than_min(item['last_total_cnt']) or less_than_min(item['last_ref']) or less_than_min(item['first_ref'])


def less_than_min(num):
    return MIN_ALLOW >= num


def load_firstnames():
    global firstnames
    with open('{}/firstnames.txt'.format(RESOURCE_PATH), 'r', encoding='utf-8') as f:
        line = f.readline()
        firstnames = line.strip().split('|')


def load_fuxing():
    global fuxing
    with open('{}/fuxing.txt'.format(RESOURCE_PATH), 'r', encoding='utf-8') as f:
        line = f.readline()
        fuxing = line.strip().split('|')


if not firstnames:
    load_firstnames()
if not fuxing:
    load_fuxing()


def test():
    name = '|小包'
    # name = 'xc包'
    print(chinese.match(name))


def main():
    name_cnt()
    # test()


if __name__ == '__main__':
    main()
