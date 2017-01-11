#!/usr/bin/env python
# encoding: utf-8

"""
@description: 推荐系统的实现

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: recommender.py
@time: 2017/1/11 21:07
"""

from math import sqrt
from xiaohint.chapter02.filterdataPearson import pearson
from xiaohint.chapter02.users import users
from xiaohint.pth import *


class Recommender():
    def __init__(self, data, k=1, metric='pearson', n=5):
        """
        :param data:
        :param k: nearest neighbor cnt
        :param metric: witch distance formula to use
        :param n: how many recommend to make
        :return:
        """
        self.k = k
        self.n = n
        self.username2id = {}
        self.userid2name = {}
        self.productid2name = {}
        self.metric = metric
        if self.metric == 'pearson':
            self.fn = pearson

        if isinstance(data, dict):
            self.data = data

    def convertProductId2Name(self, id):
        return self.productid2name[id] if id in self.productid2name else id

    def userRatings(self, id, n):
        print('Ratings for {}'.format(self.userid2name[id]))
        ratings = self.data[id]
        print('data len : {}'.format(len(ratings)))
        ratings = list(ratings.items())
        ratings = [(self.convertProductId2Name(k), v) for (k, v) in ratings]

        ratings.sort(key=lambda x: x[1], reverse=True)
        ratings = ratings[:n]
        for rating in ratings:
            print('{}\t{}'.format(rating[0], rating[1]))

    def loadBookDb(self, path=FILE_PATH):
        self.data = {}
        i = 0

        with open(path + 'Bx-Book-Ratings.csv', 'r', encoding='utf-8') as f:
            for line in f:
                i += 1
                fields = line.split(';')
                user = fields[0].strip('"')
                book = fields[1].strip('"')
                rating = int(fields[2].strip().strip('"'))
                if user in self.data:
                    currentRatings = self.data[user]
                else:
                    currentRatings = {}
                currentRatings[book] = rating
                self.data[users] = currentRatings

        print('load db total size: {}'.format(i))

    def computerNearestNeighbor(self, username):
        distances = []
        for user in self.data:
            if user != username:
                distance = self.fn(users[user], users[username])
                distances.append((user, distance))
        distances.sort(key=lambda x: x[1], reverse=True)
        return distances

    def recommend(self, user):
        recommendations = {}

        nearest = self.computerNearestNeighbor(user)

        userRatings = self.data[user]
        totalDistance = 0.0
        for i in range(self.k):
            totalDistance += nearest[i][1]
        for i in range(self.k):
            weight = nearest[i][1] / totalDistance
            name = nearest[i][0]
            neighborRatings = self.data[name]

            for artist in neighborRatings:
                if artist not in userRatings:
                    if artist not in recommendations:
                        recommendations[artist] = neighborRatings[artist] * weight
                    else:
                        recommendations[artist] += neighborRatings[artist] * weight

        recommendations = list(recommendations.items())
        recommendations = [(self.convertProductId2Name(k), v) for (k, v) in recommendations]
        recommendations.sort(key=lambda x: x[1], reverse=True)

        return recommendations[:self.n]


def main():
    r = Recommender(users)
    print(r.recommend('Jordyn'))
    print(r.recommend('Hailey'))
    # [('Blues Traveler', 5.0)]
    # [('Phoenix', 5.0), ('Slightly Stoopid', 4.5)]

if __name__ == '__main__':
    main()
