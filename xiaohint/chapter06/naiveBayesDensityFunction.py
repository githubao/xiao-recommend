#!/usr/bin/env python
# encoding: utf-8

"""
@description: 朴素贝叶斯 条件概率

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: naiveBayesDensityFunction.py
@time: 2017/1/19 19:24
"""
import math


class Classifier():
    def __init__(self, bucketPrefix, testBucketNumber, dataFormat):
        total = 0
        classes = {}
        counts = {}

        totals = {}
        numericValues = {}

        self.format = dataFormat.strip().split('\t')
        self.prior = {}
        self.conditional = {}

        for i in range(1, 11):
            if i == testBucketNumber:
                continue

            filename = '{}-{:02d}'.format(bucketPrefix, i)
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line in lines:
                fields = line.strip().split('\t')
                ignore = []
                vector = []
                category = ''
                nums = []
                for i in range(len(fields)):
                    if self.format[i] == 'num':
                        nums.append(float(fields[i]))
                    elif self.format[i] == 'attr':
                        vector.append(fields[i])
                    elif self.format[i] == 'comment':
                        ignore.append(fields[i])
                    elif self.format[i] == 'class':
                        category = fields[i]

                total += 1
                classes.setdefault(category, 0)
                counts.setdefault(category, {})
                totals.setdefault(category, {})
                numericValues.setdefault(category, {})
                classes[category] += 1

                col = 0
                for columnValue in vector:
                    col += 1
                    counts[category].setdefault(col, {})
                    counts[category][col].setdefault(columnValue, 0)
                    counts[category][col][columnValue] += 1

                col = 0
                for columnValue in nums:
                    col += 1
                    totals[category].setdefault(col, 0)
                    totals[category][col] += columnValue
                    numericValues[category].setdefault(col, [])
                    numericValues[category][col].append(columnValue)

        for category, count in classes.items():
            self.prior[category] = count / total

        for category, columns in counts.items():
            self.conditional.setdefault(category, {})
            for col, valueCounts in columns.items():
                self.conditional[category].setdefault(col, {})
                for attrValue, count in valueCounts.items():
                    self.conditional[category][col][attrValue] = count / classes[category]

        self.tmp = counts

        self.means = {}
        self.totals = totals
        for category, columns in totals.items():
            self.means.setdefault(category, {})
            for col, cTotal in columns.items():
                self.means[category][col] = cTotal / classes[category]

        self.ssd = {}
        for category, columns in numericValues.items():
            self.ssd.setdefault(category, {})
            for col, values in columns.items():
                SumOfSquareDifferences = 0
                theMean = self.means[category][col]
                for value in values:
                    SumOfSquareDifferences += (value - theMean) ** 2
                columns[col] = 0
                self.ssd[category][col] = math.sqrt(SumOfSquareDifferences / (classes[category] - 1))

    def testBucket(self, bucketPrefix, bucketNumber):
        totals = {}
        loc = 1

        filename = '{}-{:02d}'.format(bucketPrefix, bucketNumber)
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            loc += 1

            data = line.strip().split('\t')
            vector = []
            numV = []
            classInColumn = -1
            for i in range(len(self.format)):
                if self.format[i] == 'num':
                    numV.append(float(data[i]))
                elif self.format[i] == 'attr':
                    vector.append(data[i])
                elif self.format[i] == 'class':
                    classInColumn = i
            theRealClass = data[classInColumn]
            classifiedAs = self.classify(vector, numV)
            totals.setdefault(theRealClass, {})
            totals[theRealClass].setdefault(classifiedAs, 0)
            totals[theRealClass][classifiedAs] += 1
        return totals

    def classify(self, itemVector, numVector):
        results = []
        sqrt2pi = math.sqrt(2 * math.pi)

        for category, prior in self.prior.items():
            prob = prior
            col = 1
            for attrValue in itemVector:
                if not attrValue in self.conditional[category][col]:
                    prob = 0
                else:
                    prob = prob * self.conditional[category][col][attrValue]
                col += 1

            col = 1
            for x in numVector:
                mean = self.means[category][col]
                ssd = self.ssd[category][col]
                ePart = math.pow(math.e, -(x - mean) ** 2 / (2 * ssd ** 2))
                prob = prob * ((1.0 / (sqrt2pi * ssd)) * ePart)
                col += 1

            results.append((prob, category))
        return max(results)[1]


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
    subheader = '{}+'.format(' ' * 4)
    for cate in categories:
        header += cate + ' ' * 3
        subheader += '{}+'.format('-' * 4)
    print(header)
    print(subheader)

    total = 0.0
    correct = 0.0

    for cate in categories:
        row = '{}{}|'.format(cate, ' ' * 2)
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
    print('\n{:5.3f} percent correct'.format((correct * 100) / total))
    print('total of {} instances'.format(total))


def main():
    testfold("pimaSmall/pimaSmall", "num	num	num	num	num	num	num	num	class")


if __name__ == '__main__':
    main()
