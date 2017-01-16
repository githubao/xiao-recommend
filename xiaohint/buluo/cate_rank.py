#!/usr/bin/env python
# encoding: utf-8

"""
@description: 根据关注数和话题数按照类别的排序

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: cate_rank.py
@time: 2017/1/16 19:41
"""

from collections import namedtuple
from xiaohint.pth import *
from itertools import chain

# Item = namedtuple('Item', ['id', 'name','alias', 'cate', 'follownum', 'topicnum', 'intro', 'score'])
type_list = [int, str, str, str, int, int, str, float]

input_file = '{}/buluo.txt'.format(FILE_PATH)
out_file = '{}/buluo-score.txt'.format(FILE_PATH)

datas = []


def recommend(name):
    global datas
    if not datas:
        datas = load_datas(out_file)

    cate = ''
    for item in datas:
        if match_name(name, item):
            cate = item.cate
            break

    if not cate:
        return

    cates = [item for item in datas if item.cate == cate]
    cates.sort(key=lambda x: x.score, reverse=True)

    results = []
    this = -1
    for idx, item in enumerate(cates):
        if match_name(name, item):
            this = idx
        if this > -1 and idx <= this + 3:
            results.append((item.name, item.intro))

    return results


def match_name(name, item):
    return item.name == name or name in item.alias.split('|')


def load_datas(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        items = []
        for line in f:
            line = line.strip()
            item = Item(*[type(item) for type, item in zip(type_list, line.split('\t'))])
            items.append(item)

        return items


def score_data():
    items = load_datas(input_file)

    cates = (item.cate for item in items)

    clusters = []

    for cate in cates:
        cluster = [item for item in items if item.cate == cate]
        clusters.append(cluster)

    for cluster in clusters:
        all_follow = 0.0
        all_topic = 0.0
        for item in cluster:
            all_follow += item.follownum
            all_topic += item.topicnum

        for item in cluster:
            score = 0.6 * item.follownum / all_follow + 0.4 * item.topicnum / all_topic
            item.score = score

        max_score = max([item.score for item in cluster])
        min_score = min([item.score for item in cluster])
        for item in cluster:
            score = float('{:.5f}'.format((item.score - min_score) / (max_score - min_score))) * 100
            item.score = score

    with open(out_file, 'w', encoding='utf-8') as fw:
        for item in items:
            fw.write('{}\n'.format(item))


class Item:
    def __init__(self, *args):
        self.id, self.name, self.alias, self.cate, self.follownum, self.topicnum, self.intro, self.score = args
        self.__orderlist__ = ['id', 'name', 'alias', 'cate', 'follownum', 'topicnum', 'intro', 'score']

    def __str__(self):
        ordered_list = [self.__dict__[name] for name in self.__orderlist__]
        return '\t'.join('{:.3f}'.format(v) if isinstance(v, float) else str(v) for v in ordered_list)
        # return '\t'.join('{:.5f}'.format(v) if isinstance(v, float) else str(v)
        #                  for k, v in self.__dict__.items() if not k.startswith('__'))


def test_recommend():
    items = ['大学生', '华中科技大学', '北京']
    items2 = ['阴阳师', '网易阴阳师', '阴阳师手游']

    for item in chain(items, items2):
        print(recommend(item))


def main():
    # score_data()
    test_recommend()


if __name__ == '__main__':
    main()
