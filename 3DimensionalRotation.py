# -*- coding=utf-8 -*-
# python2.7
import numpy as np
from numpy import sin, cos, pi


def Left_Right_Down(Antenna, Point, alpha, beta):
    """
    :param Antenna: antenna list 天线的坐标
    :param Point: the test antenna 测试点
    :param alpha: horizontal angle 水平方向角
    :param beta: down tilt angle 下倾角
    :return: new location of antenna 新坐标系下的天线位置
    """
    # 旋转矩阵，笛卡尔坐标系
    R = [[cos(alpha)*cos(beta), -sin(alpha), cos(alpha)*sin(beta), 0],
         [sin(alpha)*cos(beta), cos(alpha), sin(alpha)*sin(beta), 0],
         [-sin(beta), 0, cos(beta), 0],
         [0, 0, 0, 1]]
    # 平移矩阵
    T = [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 1],
         [-Antenna[0], -Antenna[1], -Antenna[2], 1]]
    mPoint = np.matrix(Point)
    mR = np.matrix(R)
    mT = np.matrix(T)
    Antenna_after = mPoint*mT*mR
    # 对矩阵保留精度为2
    Antenna_after = np.round(Antenna_after, 3)
    return Antenna_after


# 求夹角
def Angle(alist):
    """
    :param alist: a list
    :return: the angle with new axis
    """
    m = np.sqrt(alist[0]**2 + alist[1]**2 + alist[2]**2)
    alpha = np.arccos(alist[0]/m)
    beta = np.arccos(alist[2]/m)
    return alpha, beta


def main():
    # 水平方向角
    horizontal_angle = pi / 2
    # 下倾角
    down_tilt_angle = pi / 2
    # 齐次矩阵，Antenna[3]永远为1
    Antenna = [1, 1, 1, 1]
    # 测试点Point
    Point = [1, 0, 0, 1]
    Antenna_after = Left_Right_Down(Antenna, Point, horizontal_angle, down_tilt_angle)
    print Antenna_after
    alpha, beta = Angle(Antenna_after[0])
    print 'The angle with new x axis is', round(alpha, 6)
    print 'The angle with new y axis is', round(beta, 6)


if __name__ == '__main__':
    main()