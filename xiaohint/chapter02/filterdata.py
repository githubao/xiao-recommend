#!/usr/bin/env python
# encoding: utf-8

"""
@description: 曼哈顿距离
适用于数据量完全且比较维度一致的情况

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: filterdata.py
@time: 2017/1/11 20:37
"""

from xiaohint.chapter02.users import users

def manhanttan(rating1, rating2):
    distance = 0
    commonRatings = False
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key])
            commonRatings = True

    return distance if commonRatings else -1


def computerNearestNeighbor(username, users):
    distances = []
    for user in users:
        if user != username:
            distance = manhanttan(users[user], users[username])
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
    return sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse=True)


def main():
    print(recommend('Hailey', users))
    # [('Phoenix', 4.0), ('Blues Traveler', 3.0), ('Slightly Stoopid', 2.5)]

if __name__ == '__main__':
    main()
