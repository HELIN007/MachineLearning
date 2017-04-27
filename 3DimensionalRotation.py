# -*- coding=utf-8 -*-
import numpy as np
from numpy import sin, cos, pi, round

def Left_Right_Down(Antenna, One, alpha, beta):
    """
    @param Antenna: antenna list 天线的坐标
    @param One: the test antenna 测试点
    @param alpha: horizontal angle 水平方向角
    @param beta: down tilt angle 下倾角 
    @return: new location of antenna 新坐标系下的天线位置
    """
    # 旋转矩阵
    R = [[cos(alpha)*cos(beta), -sin(alpha), cos(alpha)*sin(beta), 0],
         [sin(alpha)*cos(beta), cos(alpha), sin(alpha)*sin(beta), 0],
         [-sin(beta), 0, cos(beta), 0],
         [0, 0, 0, 1]]
    # 平移矩阵
    T = [[1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 1],
         [-Antenna[0], -Antenna[1], -Antenna[2], 1]]
    mOne = np.matrix(One)
    mR = np.matrix(R)
    mT = np.matrix(T)
    Antenna_after = mOne*mT*mR
    # 对矩阵保留精度为2
    Antenna_after = np.round(Antenna_after, 2)
    return Antenna_after


# 齐次矩阵，Antenna[3]永远为1
Antenna = [1, 1, 1, 1]
# 测试点One
One = [1, 0, 0, 1]
Antenna_after = Left_Right_Down(Antenna, One, pi/2, pi/2)
print Antenna_after