#!/usr/bin/env python
# encoding: utf-8

"""
@description: 计算二分类的曼哈顿方法

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: filteringdata.py
@time: 2017/1/18 19:18
"""

from xiaohint.chapter02.users import users, music


def mahattan(rating1, rating2):
    distance = 0
    total = 0
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key])
            total += 1
    return distance


def computeNearestNeighbor(username, users):
    distances = []
    for user in users:
        if user != username:
            distance = mahattan(users[user], users[username])
            distances.append((distance, user))
    distances.sort()
    return distances


def recommend(username, users):
    nearest = computeNearestNeighbor(username, users)[0][1]

    recommendations = []
    neighborRatings = users[nearest]
    userRatings = users[username]

    for artist in neighborRatings:
        if not artist in userRatings:
            recommendations.append((artist, neighborRatings[artist]))
    return sorted(recommendations, key=lambda x: x[1], reverse=True)


def main():
    print(recommend('Hailey', users))


if __name__ == '__main__':
    main()
