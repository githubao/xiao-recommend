#!/usr/bin/env python
# encoding: utf-8

"""
@description: 皮尔森相关系数距离
平均的曼哈顿距离: 适用于一些数据量缺失且比较维度一致的情况
皮尔森相关系数： 每个人的评分的标准不同 一个人的2分相当于另一个人的4分

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: filterdataPearson.py
@time: 2017/1/11 20:47
"""
from xiaohint.chapter02.users import users
from math import sqrt


def mahattan(rating1, rating2):
    distance = 0
    total = 0
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key])
            total += 1
    return distance / total if total > 0 else -1


def pearson(rating1, rating2):
    sum_xy = 0
    sum_x = 0
    sum_y = 0
    sum_x2 = 0
    sum_y2 = 0
    n = 0

    for key in rating1:
        if key in rating2:
            n += 1
            x = rating1[key]
            y = rating2[key]
            sum_xy += x * y
            sum_x += x
            sum_y += y
            sum_x2 += pow(x, 2)
            sum_y2 += pow(y, 2)

    denominator = sqrt(sum_x2 - pow(sum_x, 2) / n) * sqrt(sum_y2 - pow(sum_y, 2) / n)
    return (sum_xy - (sum_x * sum_y) / n) / denominator if denominator != 0 else 0


def computerNearestNeighbor(username, users):
    distances = []
    for user in users:
        if user != username:
            distance = pearson(users[user], users[username])
            distances.append((distance, user))
    distances.sort()
    return distances


def recommend(username, users):
    nearest = computerNearestNeighbor(username, users)[0][1]
    recommendations = []
    neighborRatings = users[nearest]
    userRatings = users[username]
    for artist in neighborRatings:
        if not artist in userRatings:
            recommendations.append((artist, neighborRatings[artist]))
    return sorted(recommendations, key=lambda x: x[1], reverse=True)


def main():
    print(recommend('Hailey', users))
    # [('Slightly Stoopid', 3.5), ('Blues Traveler', 2.0), ('Phoenix', 2.0)]


if __name__ == '__main__':
    main()
