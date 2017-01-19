#!/usr/bin/env python
# encoding: utf-8

"""
@description: 贝叶斯情感

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: bayesSentiment.py
@time: 2017/1/19 19:59
"""

import os, math


class BayesText():
    def __init__(self, trainingdir, stopwordlist, ignoreBucket):
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
            self.prob[category], self.totals[category] = self.train(trainingdir, category, ignoreBucket)
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

    def train(self, trainingdir, category, bucketNumberToIgnore):
        ignore = '{}'.format(bucketNumberToIgnore)
        currentdir = trainingdir + category
        directories = os.listdir(currentdir)
        counts = {}
        total = 0
        for directory in directories:
            if directory == ignore:
                continue

            currentBucket = currentdir + '/' + directory
            files = os.listdir(currentBucket)
            for file in files:
                with open(currentBucket + '/' + file, 'r', encoding='iso8859-1') as f:
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

    def testCategory(self, direc, category, bucketNumber):
        results = {}

        directory = '{}{}/'.format(direc, bucketNumber)
        files = os.listdir(directory)
        total = 0
        correct = 0
        for file in files:
            total += 1
            result = self.classify(directory + file)
            results.setdefault(result, 0)
            results[result] += 1

        return results

    def test(self, testdir, bucketNumber):
        results = {}

        categories = os.listdir(testdir)
        categories = [filename for filename in categories if os.path.isdir(testdir + filename)]

        for category in categories:
            print('.', end='')
            results[category] = self.testCategory(testdir + category + '/', category, bucketNumber)
        return results


def tenfold(dataPrefix, stoplist):
    results = {}
    for i in range(0, 10):
        bT = BayesText(dataPrefix, stoplist, i)
        r = bT.test(dataPrefix, i)
        for key, value in r.items():
            results.setdefault(key, {})
            for ck, cv in value.items:
                results[key].setdefault(ck, 0)
                results[key][ck] += cv

    categories = list(results.keys())
    categories.sort()
    print("\n       Classified as: ")
    header = "          "
    subheader = "        +"
    for category in categories:
        header += '{:2s    }'.format(category)
        subheader += '-----+'
    print(header)
    print(subheader)
    total = 0.0
    correct = 0.0
    for category in categories:
        row = ' {}    |'.format(category)
        for c2 in categories:
            if c2 in results[category]:
                count = results[category][c2]
            else:
                count = 0
            row += ' {:03d} |'.format(count)
            total += count
            if c2 == category:
                correct += count
        print(row)
    print(subheader)
    print('\n\nAccuracy is {}% ({} test instances)'.format(correct / total * 100, total))


def main():
    print("do sth")


if __name__ == '__main__':
    main()
