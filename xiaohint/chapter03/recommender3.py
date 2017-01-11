#!/usr/bin/env python
# encoding: utf-8

"""
@description: 基于slot one 的评分推荐系统

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: recommender3.py
@time: 2017/1/11 21:52
"""

from xiaohint.chapter02.recommender import Recommender, FILE_PATH


class Recommender3(Recommender):
    def __init__(self, data, k=1, metric='pearson', n=5):
        super().__init__(data, k, metric, n)

        self.frequencies = {}
        self.deviations = {}

    def showUserTopItems(self, user, n):
        items = list(self.data[user].items())
        items.sort(key=lambda x: x[1], reverse=True)
        for i in range(n):
            print('{]\t{}'.format(self.convertProductId2Name(items[i][0]), items[i][1]))

    def loadMovieLens(self, path=FILE_PATH):
        pass

    def computerDeviations(self):
        for ratings in self.data.values():
            for item, rating in ratings.items():
                self.frequencies.setdefault(item, {})
                self.deviations.setdefault(item, {})

                for item2, rating2 in ratings.items():
                    if item != item2:
                        self.frequencies[item].setdefault(item2, 0)
                        self.deviations[item].setdefault(item2, 0.0)
                        self.frequencies[item][item2] += 1
                        self.deviations[item][item2] += rating - rating2

        for item, ratings in self.deviations.items():
            for item2 in ratings:
                ratings[item2] /= self.frequencies[item][item2]

    def slopeOneRecommendations(self, userRatings):
        recommendations = {}
        frequencies = {}

        for userItem, userRating in userRatings.items():
            for diffItem, diffRating in self.deviations.items():
                if diffItem not in userRatings and userItem in self.deviations[diffItem]:
                    freq = self.frequencies[diffItem][userItem]

                    recommendations.setdefault(diffItem, 0.0)
                    frequencies.setdefault(diffItem, 0)

                    recommendations[diffItem] += (diffItem[userItem] + userRating) * freq
                    frequencies[diffItem] += freq

        recommendations = [(self.convertProductId2Name(k), v) for k, v in recommendations.items()]
        recommendations.sort(key=lambda x: x[1], reverse=True)
        return recommendations[:self.n]


def main():
    print("do sth")


if __name__ == '__main__':
    main()
