#!/usr/bin/env python
# encoding: utf-8

"""
@description: 分类

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: classifyTemplate.py
@time: 2017/1/18 19:29
"""


class Classifier():
    def __init__(self, filename):
        self.medianAndDeviation = []

        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        self.format = lines[0].strip().split('\t')
        self.data = []

        for line in lines[1:]:
            fields = line.strip().split('\t')
            ignore = []
            vector = []
            classification = ''
            for i in range(len(fields)):
                if self.format[i] == 'num':
                    vector.append(int(fields[i]))
                elif self.format[i] == 'comment':
                    ignore.append(fields[i])
                elif self.format[i] == 'class':
                    classification = fields[i]
            self.data.append((classification, vector, ignore))
        self.rawData = list(self.data)

        self.vlen = len(self.data[0][1])
        for i in range(self.vlen):
            self.normalizeColumn(i)

    def getMedian(self, alist):
        if alist == []:
            return []
        blist = sorted(alist)
        length = len(alist)
        if length % 2 == 1:
            return blist[int(((length + 1) / 2) - 1)]
        else:
            v1 = blist[int(length / 2)]
            v2 = blist[int(length / 2) - 1]
            return (v1 + v2) / 2

    def getAbsoluteStandardDeviation(self, alist, median):
        sum = 0
        for item in alist:
            sum += abs(item - median)
        return sum / len(alist)

    def normalizeColumn(self, columnNumber):
        col = [v[1][columnNumber] for v in self.data]
        median = self.getMedian(col)
        asd = self.getAbsoluteStandardDeviation(col, median)
        self.medianAndDeviation.append((median, asd))
        for v in self.data:
            v[1][columnNumber] = (v[1][columnNumber] - median) / asd

    def normalizeVector(self, v):
        vector = list(v)
        for i in range(len(vector)):
            (median, asd) = self.medianAndDeviation[i]
            vector[i] = (vector[i] - median) / asd
        return vector

    def mahattan(self, vector1, vector2):
        return sum(map(lambda v1, v2: abs(v1 - v2), vector1, vector2))

    def nearestNeighbor(self, itemVector):
        # min = -1
        # minVector = None
        # for vector in self.data:
        #     nowmin = self.mahattan(vector[1], itemVector)
        #     if min == -1:
        #         min = nowmin
        #
        #     if nowmin != 0 and nowmin < min:
        #         min = nowmin
        #         minVector = vector
        #
        # return (itemVector,minVector,)

        return min([(self.mahattan(itemVector, item[1]), item) for item in self.data])

        # return ((0, ('replace this line with correct return', [0], [])))

    def classify(self, itemVector):
        return self.nearestNeighbor(self.normalizeVector(itemVector))[1][0]


def unittest():
    classifier = Classifier('athletesTrainingSet.txt')

    br = ('Basketball', [72, 162], ['Brittainey Raven'])
    n1 = ('Gymnastics', [61, 76], ['Viktoria Komova'])
    c1 = ('Basketball', [74, 190], ['Crystal Langhorne'])

    brNorm = classifier.normalizeVector(br[1])
    n1Norm = classifier.normalizeVector(n1[1])
    c1Norm = classifier.normalizeVector(c1[1])

    assert (brNorm == classifier.data[1][1])
    assert (n1Norm == classifier.data[-1][1])
    print('normalizeVector fn ok')

    assert (round(classifier.mahattan(c1Norm, classifier.data[1][1]), 5) == 1.16823)
    assert (classifier.mahattan(brNorm, classifier.data[1][1]) == 0)
    assert (classifier.mahattan(n1Norm, classifier.data[-1][1]) == 0)
    print('mahattan fn ok')

    result = classifier.nearestNeighbor(brNorm)
    assert (result[1][2] == br[2])
    result = classifier.nearestNeighbor(n1Norm)
    assert (result[1][2] == n1[2])
    assert (classifier.nearestNeighbor(c1Norm)[1][2][0] == 'Jennifer Lacy')
    print('nearest Neighbor fn ok')

    assert (classifier.classify(br[1]) == 'Basketball')
    assert (classifier.classify(c1[1]) == 'Basketball')
    assert (classifier.classify(n1[1]) == 'Gymnastics')
    print('classify fn ok')


def test(training_filename, test_filename):
    classifier = Classifier(training_filename)
    with open(test_filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    numCorrect = 0.0
    for line in lines:
        data = line.strip().split('\t')
        vector = []
        classInColumn = -1
        for i in range(len(classifier.format)):
            if classifier.format[i] == 'num':
                vector.append(float(data[i]))
            elif classifier.format[i] == 'class':
                classInColumn = i
        theClass = classifier.classify(vector)
        prefix = '-'
        if theClass == data[classInColumn]:
            numCorrect += 1
            prefix = '+'
        print('{}{:12s}{}'.format(prefix, theClass, line), end='')
    print('{:4.2f}% correct'.format(numCorrect * 100 / len(lines)))


def main():
    # unittest()
    test('athletesTrainingSet.txt', 'athletesTestSet.txt')


if __name__ == '__main__':
    main()
