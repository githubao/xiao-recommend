#!/usr/bin/env python
# encoding: utf-8

"""
@description: 贝叶斯文本

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: bayesText.py
@time: 2017/1/19 20:00
"""

import os, math


class BayesText():
    def __init__(self, trainingdir, stopwordlist):
        self.vocabulary = {}
        self.prob = {}
        self.totals = {}
        self.stopwords = {}

        with open(stopwordlist, encoding='utf-8') as f:
            for line in f:
                self.stopwords[line.strip()] = 1
        categories = os.listdir(trainingdir)
        self.categories = [filename for filename in categories if os.path.isdir(trainingdir + filename)]
        print('Counting...')
        for category in self.categories:
            print(' ' * 4 + category)
            self.prob[category], self.totals[category] = self.train(trainingdir, category)
        toDelete = []
        for word in self.vocabulary:
            if self.vocabulary[word] < 3:
                toDelete.append(word)

        for word in toDelete:
            del self.vocabulary[word]

        vocabLength = len(self.vocabulary)
        print('Computing probabilities: ')
        for category in self.categories:
            print(' ' * 4 + category)
            denominator = self.totals[category] + vocabLength
            for word in self.vocabulary:
                if word in self.prob[category]:
                    count = self.prob[category][word]
                else:
                    count = 1
                self.prob[category][word] = (float(count + 1) / denominator)

        print('DONE TRAINING\n\n')

    def train(self, trainingdir, category):
        currentdir = trainingdir + category
        files = os.listdir(currentdir)
        counts = {}
        total = 0
        for file in files:
            with open(currentdir + '/' + file, 'r', encoding='iso8859-1') as f:
                for line in f:
                    tokens = line.split()
                    for token in tokens:
                        token = token.strip('\'".,?:-')
                        token = token.lower()
                        if token and token not in self.stopwords:
                            self.vocabulary.setdefault(token, 0)
                            self.vocabulary[token] += 1
                            counts.setdefault(token, 0)
                            counts[token] += 1
                            total += 1
        return counts, total

    def classify(self, filename):
        results = {}
        for category in self.categories:
            results[category] = 0

        with open(filename, 'r', encoding='iso8859-1') as f:
            for line in f:
                tokens = line.split()
                for token in tokens:
                    token = token.strip('\'".,?:-')
                    token = token.lower()
                    if token in self.vocabulary:
                        for category in self.categories:
                            if self.prob[category][token] == 0:
                                print('{} {}'.format(category, token))
                            results[category] += math.log(self.prob[category][token])

        results = list(results.items())
        results.sort(key=lambda x: x[1], reverse=True)
        return results[0][0]

    def testCategory(self, directory, category):
        files = os.listdir(directory)
        total = 0
        correct = 0
        for file in files:
            total += 1
            result = self.classify(directory + file)
            if result == category:
                correct += 1
        return (correct, total)

    def test(self, testdir):
        categories = os.listdir(testdir)
        categories = [filename for filename in categories if os.path.isdir(testdir + filename)]

        correct = 0
        total = 0
        for category in categories:
            print('.', end='')
            catCorrect, catTotal = self.testCategory(testdir + category + '/', category)
            correct += catCorrect
            total += catCorrect
        print('\n\nAccuracy is {}% ({} test instances)'.format(correct / total * 100, total))


def main():
    print("do sth")


if __name__ == '__main__':
    main()
