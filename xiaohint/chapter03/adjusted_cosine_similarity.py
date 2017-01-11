#!/usr/bin/env python
# encoding: utf-8

"""
@description: 修正的余弦相似度

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: adjusted_cosine_similarity.py
@time: 2017/1/11 21:41
"""

from math import sqrt
from xiaohint.chapter03.users import users3


def computerSimilarity(band1, band2, userRatings):
    averages = {}
    for user, ratings in userRatings.items():
        averages[user] = (float(sum(ratings.values()) / len(ratings.values())))

    num = 0
    dem1 = 0
    dem2 = 0

    for user, ratings in userRatings.items():
        if band1 in ratings and band2 in ratings:
            avg = averages[user]
            num += (ratings[band1] - avg) * (ratings[band2] - avg)
            dem1 += (ratings[band1] - avg) ** 2
            dem2 += (ratings[band2] - avg) ** 2
    return num / (sqrt(dem1) * sqrt(dem2))


def main():
    print(computerSimilarity('Kacey Musgraves', 'Lorde', users3))
    print(computerSimilarity('Imagine Dragons', 'Lorde', users3))
    print(computerSimilarity('Daft Punk', 'Lorde', users3))


if __name__ == '__main__':
    main()
