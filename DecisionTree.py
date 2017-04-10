# -*- coding=utf-8 -*-
# python2.7
from math import log
import operator

# 创建简单的数据集
def creatDataset():
    dataSet = [[1, 1, 0, 'fight'], [1, 0, 1, 'fight'],
               [1, 0, 1,'fight'], [1, 0, 1, 'fight'],
               [0, 0, 1, 'run'], [0, 1, 0, 'fight'], [0, 1, 1, 'run']]
    labels = ['weapon', 'bullet', 'blood']
    return dataSet, labels

# 计算香农熵
def Shannon(dataSet):
    numEntries = len(dataSet)  # 数据集的条数
    labelCounts = {}
    for featVec in dataSet:
        currentLabel = featVec[-1]  # 现在所处的状态
        # 累计状态出现的次数
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
            # print labelCounts
        labelCounts[currentLabel] += 1
    # print labelCounts
    shannon = 0
    for key in labelCounts:
        # key即为run和fight
        prob = float(labelCounts[key])/numEntries  # key出现的概率
        shannon -= prob * log(prob, 2)  # 香农熵公式
    return shannon

# 打印出数据集
def printData(myDat):
    for item in myDat:
        print '%s' % (item)

# 按照给定特征划分数据集
def splitDataset(dataSet, axis, value):
    retDataset = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducefeatVec = featVec[:axis]
            reducefeatVec.extend(featVec[axis+1:])
            retDataset.append(reducefeatVec)
    return retDataset

# 选择最佳
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    bestShannon = Shannon(dataSet)
    # print bestShannon
    bestInfoGain = 0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newShannon = 0
        for value in uniqueVals:
            subDataSet = splitDataset(dataSet,i,value)
            prob = len(subDataSet)/float(len(dataSet))
            newShannon += prob * Shannon(subDataSet)
        infoGain = bestShannon - newShannon
        print infoGain
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            # print bestInfoGain
            bestFeature = i
    return bestFeature
myDat, labels = creatDataset()
# printData(myDat)
# print Shannon(myDat)
# print splitDataset(myDat, 1, 1)
print chooseBestFeatureToSplit(myDat)