#!/usr/bin/env python
# encoding: utf-8

"""
@description: 朴素贝叶斯分类

@version: 1.0
@author: BaoQiang
@license: Apache Licence 
@contact: mailbaoqiang@gmail.com
@site: http://www.github.com/githubao
@software: PyCharm
@file: naiveBayes.py
@time: 2017/1/19 18:22
"""


class Classifier():
    def __init__(self, bucketPrefix, testBucketNumber, dataFormat):
        total = 0
        classes = {}
        counts = {}

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
                for i in range(len(fields)):
                    if self.format[i] == 'num':
                        vector.append(float(fields[i]))
                    elif self.format[i] == 'attr':
                        vector.append(fields[i])
                    elif self.format[i] == 'comment':
                        ignore.append(fields[i])
                    elif self.format[i] == 'class':
                        category = fields[i]

                total += 1
                classes.setdefault(category, 0)
                counts.setdefault(category, {})
                classes[category] += 1

                col = 0
                for columnValue in vector:
                    col += 1
                    counts[category].setdefault(col, {})
                    counts[category][col].setdefault(columnValue, 0)
                    counts[category][col][columnValue] += 1

        for category, count in classes.items():
            self.prior[category] = count / total

        for category, columns in counts.items():
            self.conditional.setdefault(category, {})
            for col, valueCounts in columns.items():
                self.conditional[category].setdefault(col, {})
                for attrValue, count in valueCounts.items():
                    self.conditional[category][col][attrValue] = count / classes[category]

        self.tmp = counts

    def classify(self, itemVector):
        results = []
        for category, prior in self.prior.items():
            prob = prior
            col = 1
            for attrValue in itemVector:
                if not attrValue in self.conditional[category][col]:
                    prob = 0
                else:
                    prob = prob * self.conditional[category][col][attrValue]
                col += 1
            results.append((prob, category))
        return max(results)[1]

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
            classInColumn = -1
            for i in range(len(self.format)):
                if self.format[i] == 'num':
                    vector.append(float(data[i]))
                elif self.format[i] == 'attr':
                    vector.append(data[i])
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
    testfold('house-votes/hv',
             'class\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr\tattr')


if __name__ == '__main__':
    main()
