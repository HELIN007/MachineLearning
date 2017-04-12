# -*- coding=utf-8 -*-
# python2.7
from math import log


# 创建简单的数据集
def creatDataset():
    dataSet = [[1, 1, 0, 'fight'], [1, 0, 1, 'fight'],
               [1, 0, 1, 'fight'], [1, 0, 1, 'fight'],
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
def printData(dataSet):
    for item in dataSet:
        print '%s' % item


# 按照给定特征划分数据集，axis是某一属性的序列号，value是属性值
def splitDataset(dataSet, axis, value):
    retDataset = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducefeatVec = featVec[:axis]
            reducefeatVec.extend(featVec[axis+1:])  # 这两行为了去除该属性axis列
            retDataset.append(reducefeatVec)
    return retDataset  # 返回原数据集中符合所给定属性值的数据集


# 选择最佳
def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    bestShannon = Shannon(dataSet)  # 先计算整个数据集的香农熵
    bestInfoGain = 0
    bestFeature = -1
    for i in range(numFeatures):  # 分别遍历所有的属性
        featList = [example[i] for example in dataSet]  # 分别取出每一列的值，存为列表
        # print featList
        uniqueVals = set(featList)  # 去重，保留的该类型属性的数量
        # print uniqueVals
        newShannon = 0
        for value in uniqueVals:
            # print value
            subDataSet = splitDataset(dataSet, i, value)
            # print subDataSet
            prob = len(subDataSet)/float(len(dataSet))
            newShannon += prob * Shannon(subDataSet)
        infoGain = bestShannon - newShannon  # 信息熵
        # print infoGain
        if infoGain > bestInfoGain:  # 选出信息熵最大的属性的序列号
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


'''
# 选出出现次数最多的分类名称
def majorityCnt(classList):
    classCount = 0
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedclassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedclassCount[0][0]
'''


# 递归创建决策树
def creatTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]  # 取出最后一列属性
    # 判断属性是否都是一样的，若是一样则返回该属性
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    # if len(dataSet[0]) == 1:
    #     return majorityCnt(classList)
    bestFeature = chooseBestFeatureToSplit(dataSet)  # 得出以哪个属性(序号）进行决策
    # print bestFeature
    bestFeatureLable = labels[bestFeature]  # 得出属性
    # print bestFeatureLable
    myTree = {bestFeatureLable: {}}
    # print myTree
    del(labels[bestFeature])  # 删除labels中的该属性避免重复
    featValues = [example[bestFeature] for example in dataSet]  # 分别取出第bestFeature列的值，存为列表
    # print featValues
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLables = labels[:]  # 复制labels的值，且subLables变化时不影响labels
        # print subLables
        myTree[bestFeatureLable][value] = creatTree(splitDataset(dataSet, bestFeature, value), subLables)
        # print myTree
    return myTree


myDat, labels = creatDataset()
print creatTree(myDat, labels)
