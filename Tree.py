# -*- coding: utf-8 -*-
# Python2.7
# KD树

import numpy as np


class node:
    def __init__(self, point=None, split=None, left=None, right=None):
        self.point = point  # 坐标点
        self.split = split  # 分割方式
        self.left = left  # 左儿子
        self.right = right  # 右儿子


# 中位数
def getMedian(x):
    lenth = x.shape[0]
    if lenth % 2 == 1:
        return np.median(x)
    return x[np.argsort(x)[lenth / 2]]


# 传入的data是numpy_array类型
def createKdTree(data):
    row = data.shape[0]
    if row == 0:
        return
    col = data.shape[1]  # 表示维数
    var = 0  # 方差
    split = 0  # 划分的索引
    for i in range(col):
        tmp_col = data[:, i]  # i=0时读取所有的横坐标，i=1时读取所有的纵坐标
        tmp_var = np.var(tmp_col)
        if tmp_var > var:
            var = tmp_var
            split = i
    # 进行划分的点的坐标
    data_point = getMedian(data[:, split])  # split=0时读取所有的横坐标，split=1时读取所有的纵坐标

    # 划分的具体的点的值是data[point_tmp, split]
    point = data[np.where(data[:, split] == data_point)]

    # 查看如何划分
    root = node(point, split)
    # print root.point, root.split
    root.left = createKdTree(data[np.where(data[:, split] < data_point)])
    root.right = createKdTree(data[np.where(data[:, split] > data_point)])
    return root


# 两点间的距离
def distant(s1, s2):
    sum = 0.0
    for i in range(len(s1)):
        sum = sum + (s1[i]-s2[0][i])**2
    return np.sqrt(sum)


# 树的查询
def findPoint(root, query):
    Point = root.point  # Point为树的开头
    # print Point
    minDist = distant(query, Point)  # 点与Point的距离
    nodeList = []
    tempRoot = root
    # 确定了query所在的区域
    while tempRoot:  # tempRoot为空跳出循环
        nodeList.append(tempRoot)
        Dist = distant(query, tempRoot.point)
        # print Dist
        if minDist >= Dist:
            Point = tempRoot.point
            minDist = Dist
        Split = tempRoot.split
        # print Split
        if query[Split] <= tempRoot.point[0][Split]:
            tempRoot = tempRoot.left
        else:
            tempRoot = tempRoot.right
    # 回溯查找
    while nodeList:
        backPoint = nodeList.pop()  # 移除最后一个元素，并赋值给backPoint
        # print backPoint
        Split = backPoint.split
        # print Split, minDist
        # print 'back.point = ', backPoint.point
        # 判断是否需要进入父亲节点的子空间进行搜索
        if abs(query[Split]-backPoint.point[0][Split]) <= minDist:
            if query[Split] <= backPoint.point[0][Split]:
                # print query[Split], backPoint.point[0][Split]
                tempRoot = backPoint.right
                # print tempRoot
            else:
                tempRoot = backPoint.left
                # print tempRoot
            if tempRoot:
                nodeList.append(tempRoot)
                # print nodeList, tempRoot.point
                curDist = distant(query, tempRoot.point)
                # print curDist
                if minDist > curDist:
                    minDist = curDist
                    Point = tempRoot.point
    return Point, minDist


if __name__ == '__main__':
    input = np.array([[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]])
    # print createKdTree(input).point
    print findPoint(createKdTree(input), [2.1, 3.1])
