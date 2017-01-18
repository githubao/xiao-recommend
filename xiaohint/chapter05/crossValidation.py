#!/usr/bin/env python
# encoding: utf-8

"""
@description: 交叉验证

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: crossValidation.py
@time: 2017/1/18 20:49
"""


class Classifier():
    def __init__(self, bucketPrefix, testBucketNumber, dataFormat):
        self.medianAndDeviation = []

        self.format = dataFormat.strip().split('\t')
        self.data = []

        for i in range(1, 11):
            if i == testBucketNumber:
                continue

            filename = '{}-{:02d}'.format(bucketPrefix, i)
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line in lines[1:]:
                fields = line.strip().split('\t')
                ignore = []
                vector = []
                classification = ''
                for i in range(len(fields)):
                    if self.format[i] == 'num':
                        vector.append(float(fields[i]))
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

    def testBucket(self, bucketPrefix, bucketNumber):
        totals = {}

        filename = '{}-{:02d}'.format(bucketPrefix, bucketNumber)
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            data = line.strip().split('\t')
            vector = []
            classInColumn = -1
            for i in range(len(self.format)):
                if self.format[i] == 'num':
                    vector.append(float(data[i]))
                elif self.format[i] == 'class':
                    classInColumn = i
            theRealClass = data[classInColumn]
            classifiedAs = self.classify(vector)
            totals.setdefault(theRealClass, {})
            totals[theRealClass].setdefault(classifiedAs, 0)
            totals[theRealClass][classifiedAs] += 1
        return totals


def testfold(bucketPrefix, dataFormat):
    results = {}
    for i in range(1, 11):
        c = Classifier(bucketPrefix, i, dataFormat)
        t = c.testBucket(bucketPrefix, i)
        for k, v in t.items():
            results.setdefault(k, {})
            for ck, cv in v.items():
                results[k].setdefault(ck, 0)
                results[k][ck] += cv

    categories = list(results.keys())
    categories.sort()
    print('\n{}Classified as: '.format(' ' * 8))
    header = ' ' * 6
    subheader ='{}+'.format(' ' * 4)
    for cate in categories:
        header += cate + ' ' * 3
        subheader += '{}+'.format('-' * 4)
    print(header)
    print(subheader)

    total = 0.0
    correct = 0.0

    for cate in categories:
        row = '{}{}|'.format(cate,' '* 2)
        for c2 in categories:
            if c2 in results[cate]:
                count = results[cate][c2]
            else:
                count = 0
            row += ' {:2d} |'.format(count)
            total += count
            if c2 == cate:
                correct += count
        print(row)
    print(subheader)
    print('\n{:5.3f} percent correct'.format((correct * 100)/total))
    print('total of {} instances'.format(total))


def main():
    testfold('mpgData/mpgData','class\tnum\tnum\tnum\tnum\tnum\tcomment')


if __name__ == '__main__':
    main()
