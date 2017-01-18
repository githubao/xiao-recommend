#!/usr/bin/env python
# encoding: utf-8

"""
@description: 数据分组

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: divide.py
@time: 2017/1/18 20:39
"""

import random


def buckets(filename, bucketname, separator, classColumn):
    numOfBuckets = 10
    data = {}

    with open(filename, encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if separator != '\t':
            line = line.replace(separator, '\t')
        category = line.split()[classColumn]
        data.setdefault(category, [])
        data[category].append(line)

    buckets = []
    for i in range(numOfBuckets):
        buckets.append([])

    for k in data.keys():
        random.shuffle(data[k])
        bNum = 0
        for item in data[k]:
            buckets[bNum].append(item)
            bNum = (bNum + 1) % numOfBuckets

    for bNum in range(numOfBuckets):
        with open('{}-{:02d}'.format(bucketname, bNum + 1), 'w', encoding='utf-8'):
            for item in buckets[bNum]:
                f.write(item)


def main():
    buckets('pimaSmall.txt', 'pimaSmall', ',', 8)


if __name__ == '__main__':
    main()
