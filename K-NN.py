import operator
import matplotlib.pyplot as plt
# import re
# 从文件中获取特征矩阵和标签列表
def fileToMatrix(fileName):
    fr = open(fileName)
    # 读文件内容
    allLines = fr.readlines()
    numberOfLines = len(allLines)
    # 构造numberOfLines行3列的0阵，用作之后存储特征矩阵
    returnMat = zeros((numberOfLines, 3))
    # 定义标签列表
    labelVector = []
    index = 0
    for line in allLines:
        # 左右截空
        line = line.strip()
        # \t分割
        listFromLine = line.split('\t')
        # 特征矩阵按行赋值
        returnMat[index, :] = listFromLine[0:3]
        # 离散化标签
        if listFromLine[-1] == 'largeDoses':
            label = 3
        elif listFromLine[-1] == 'smallDoses':
            label = 2
        else:
            label = 1
        labelVector.append(label)
        index += 1
    return returnMat, labelVector


# 特征矩阵归一化处理
def autoNorm(dataSet):
    # 取矩阵每列的最小值
    minVal = dataSet.min(0)
    # 同理，每列的最大值
    maxVal = dataSet.max(0)
    # 取每列的极差
    ranges = maxVal - minVal
    # 构造归一矩阵
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    # 每列原值减去每列最小值
    normDataSet = dataSet - tile(minVal, (m, 1))
    # 返回归一矩阵、极差矩阵、每列最小值矩阵
    return normDataSet, ranges, minVal


# 分类函数，之前有讲解（[传送门](https://zh1995.github.io/2017/03/22/K-%E8%BF%91%E9%82%BB%E7%AE%97%E6%B3%95Demo/) ）
def classify0(intX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(intX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(
        classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


# 测试分类器
def datingClassTest():
    # 选取10%数据用作测试
    ratio = 0.1
    datingDataMat, datingLabels = fileToMatrix('datingTestSet.txt')
    # 归一化
    normMat, ranges, minVal = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * ratio)
    errorCount = 0.0
    # 循环10%数据检验
    for i in range(numTestVecs):
        # 算法求结果
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs:m, :],
                                     datingLabels[numTestVecs:m], 3)
        print "the classifier came back with: %d, the real answer is %d" % (
            classifierResult, datingLabels[i])
        # 与已知不符错误计数器加1
        if (classifierResult != datingLabels[i]):
            errorCount += 1.0
    print "the total error rate is: %f" % (errorCount / float(numTestVecs))


# 输入用户信息，匹配好感度结果
def classifyPerson():
    # 好感度列表
    resultList = ['not at all', 'in small doses', 'in large doses']
    # 获取输入特征信息
    percentTats = float(input("percentage of time spent playing video games?"))
    ffMiles = float(input("frequent flier miles earned per year?"))
    iceCream = float(input("liters of ice cream consumed per year?"))
    # 获取特征矩阵、标签列表
    datingDataMat, datingLabels = fileToMatrix('datingTestSet.txt')
    # 特征矩阵归一化
    normMat, ranges, minVal = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    # 用户信息归一化后K-NN求解
    classifierResult = classify0((inArr - minVal) / ranges, normMat, datingLabels, 3)
    print "You will probably like this person:", resultList[classifierResult - 1]


datingDataMat, datingLabels = fileToMatrix('datingTestSet.txt')
# 创建画板
fig = plt.figure()
# 在1行1列1的位置添加子图
ax = fig.add_subplot(111)
# 以特征矩阵第2列和第3列的数据画散点图，后两个参数根据标签值的不同用于高亮坐标点
ax.scatter(datingDataMat[:, 1], datingDataMat[:, 2], 15.0*array(datingLabels), 15.0*array(datingLabels))
# 展示散点图
plt.show()
# 演示测试分类器
normMat, ranges, minVal = autoNorm(datingDataMat)
datingClassTest()
# 演示整个系统
classifyPerson()
