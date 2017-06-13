# -*- coding=utf-8 -*-
# python2.7
from __future__ import division
import numpy as np
from numpy import sin, cos, pi, log10
import xlrd
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
from copy import deepcopy


def data():
    """
    读取天线以及待测点的数据
    :return: 基站横纵坐标，水平角下倾角；待测点横纵坐标
    """
    A_P = xlrd.open_workbook('antenna_point.xlsx')
    A_P_table = A_P.sheets()[0]
    node_x = A_P_table.col_values(0)[:51]
    node_y = A_P_table.col_values(1)[:51]
    node_h = A_P_table.col_values(2)[:51]
    node_h_angle = A_P_table.col_values(3)[:51]
    node_v_angle = A_P_table.col_values(4)[:51]
    point_x = A_P_table.col_values(5)
    point_y = A_P_table.col_values(6)
    return node_x, node_y, node_h, node_h_angle, node_v_angle, point_x, point_y

def find_gain():
    """
    查找相对应角度的增益值
    :return: 分别对应于水平角和垂直角的增益
    """
    Gain = xlrd.open_workbook('angle_gain.xlsx')
    Gain_table = Gain.sheets()[0]
    horizontal_data_gain = Gain_table.col_values(1)
    vertical_data_gain = Gain_table.col_values(2)
    return horizontal_data_gain, vertical_data_gain


class relative_position:
    """
    求待测点相对于基站的坐标，以及待测点与基站的距离
    """
    def __init__(self, Point, needed_antenna, horizontal_angle, vertical_angle, needed_node_num):
        self.point = Point  # 待测点
        self.antenna = needed_antenna  # 基站
        self.alpha = np.array(horizontal_angle)/180.*pi  # 水平角，弧度
        self.beta = np.array(vertical_angle)/180.*pi  # 下倾角，弧度
        self.n = needed_node_num  # 基站数


    def direction_down_angle(self):
        """
        :return: 相对于基站的新坐标，以及和基站的距离
        """
        mPoint = np.matrix(self.point)  # 矩阵化
        Point_after = []
        dis = []
        # 循环每个基站
        for i in range(self.n):
            # 旋转矩阵
            R = [[cos(self.alpha[i])*cos(self.beta[i]), -sin(self.alpha[i]), cos(self.alpha[i])*sin(self.beta[i]), 0],
                 [sin(self.alpha[i])*cos(self.beta[i]), cos(self.alpha[i]), sin(self.alpha[i])*sin(self.beta[i]), 0],
                 [-sin(self.beta[i]), 0, cos(self.beta[i]), 0],
                 [0, 0, 0, 1]]
            # 平移矩阵
            T = [[1, 0, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 1, 0],
                 [-self.antenna[i][0], -self.antenna[i][1], -self.antenna[i][2], 1]]
            mR = np.matrix(R)
            mT = np.matrix(T)
            after = mPoint*mT*mR  # 计算公式
            Point_after.append(after)
        Point_after = np.round(Point_after, 100)
        # 计算待测点与基站的距离
        for i in range(len(Point_after)):
            d = np.sqrt((self.antenna[i][0] - self.point[0]) ** 2 +
                          (self.antenna[i][1] - self.point[1]) ** 2 +
                          (self.antenna[i][2] - self.point[2]) ** 2)
            dis.append(d)
        dis = np.round(dis, 5)
        # print Point_after
        # print dis
        return Point_after, dis


class relative_angle:
    """
    求待测点相对于基站的水平角和下倾角
    """
    def __init__(self, Point_after, needed_node_num):
        self.p_a = Point_after  # 待测点的新坐标
        self.n = needed_node_num  # 基站数


    def Angle(self):
        alpha = []
        beta = []
        for i in range(self.n):
            m = np.sqrt(self.p_a[i, 0, 0]**2 + self.p_a[i, 0, 1]**2)
            n = np.sqrt(self.p_a[i, 0, 0]**2 + self.p_a[i, 0, 1]**2 + self.p_a[i, 0, 2]**2)
            if m != 0:  # 投影到xOy平面上计算与x轴的夹角
                if self.p_a[i, 0, 1] < 0:  # 因为有方向，所以y>0时为0-180°
                    a = 360 - np.arccos(self.p_a[i, 0, 0]/m) * 180. / pi
                else:
                    a = np.arccos(self.p_a[i, 0, 0] / m) * 180. / pi
                alpha.append(int(a))
            else:
                alpha.append(0)
            if n != 0:  # 在整个空间里计算与z轴的夹角
                b = 90 - np.arccos(abs(self.p_a[i, 0, 2])/n)*180./pi
                beta.append(int(b))
            else:
                beta.append(90)
        # print 'The angle with new alpha axis is:', alpha, 'degree'
        # print ' The angle with new beta axis is:', beta, 'degree'
        return alpha, beta


class calculate:
    def __init__(self, point_after, Point, h_d_g, v_d_g,
                 node_h, index, alpha, beta, dis, Pt, f, needed_node_num):
        self.p_a = point_after  # 待测点的新坐标
        self.point = Point  # 待测点，后文只求了个挂高
        self.h_d_g = h_d_g  # 水平增益，供查询
        self.v_d_g = v_d_g  # 垂直增益，供查询
        self.n_h = node_h  # 挂高
        self.index = index
        self.alpha = alpha  # 相对于基站的新水平角
        self.beta = beta  # 相对于基站的新下倾角
        self.dis = np.array(dis)/1000.  # km
        self.Pt = Pt  # 发射功率
        self.f = f  # 发射频率
        self.n = needed_node_num  # 基站数

    def Gain(self):
        """
        :return: 待测点相对于每个基站的增益
        """
        Gain = []
        for i in range(self.n):
            a = (pi - abs(self.alpha[i])/180.*pi)/pi*(self.h_d_g[0]-self.v_d_g[self.beta[i]])
            b = abs(self.alpha[i])/180.*(self.h_d_g[179]-self.v_d_g[179-self.beta[i]])
            g = self.h_d_g[self.alpha[i]] - a - b
            Gain.append(g)
        # print '            The gain of point is:', np.round(Gain, 5), 'dBm'
        return Gain

    def Loss(self, C=3):
        """
        :param C: C=3 for metropolitan areas
        :return: 待测点相对于每个基站的损耗
        """
        Loss = []
        hR = self.point[2]  # m
        for i in range(self.n):
            hT = self.n_h[self.index[0][i]]  # m
            a = (1.1*log10(self.f)-0.7)*hR-(1.56*log10(self.f)-0.8)
            L = 46.3+33.9*log10(self.f)-13.82*log10(hT)-a+(44.9-6.55*log10(hT))*log10(self.dis[i])+C
            Loss.append(L)
        # print '                     The Loss is:', np.round(Loss, 5), 'dB'
        return Loss


    def Rsrp(self):
        """
        :return: 待测点相对于每个基站的信号强度RSRP
        """
        RSRP = []
        Gain = self.Gain()
        Loss = self.Loss()
        for i in range(self.n):
            r = self.Pt + Gain[i] - Loss[i]
            RSRP.append(r)
        max1 = max(RSRP)  #dBm
        max2 = 10**(max1/10)
        s = deepcopy(RSRP)
        s1 = np.array(s)
        s2 = sum(10**(s1/10)) - max2 #mW
        sinr = max2/s2
        SINR = 10*log10(sinr)  #dB
        # print '                     The RSRP is:', min(RSRP), 'dBm', '--->', max(RSRP), 'dBm'
        print 'The RSRP is:', round(max(RSRP), 5), 'dBm'
        print 'The SINR is:', SINR, 'dB'
        print '-----'
        return round(max(RSRP), 5), SINR


class kDTree:
    """
    找出符合距离要求的所有基站
    """
    def __init__(self, Antenna, Point, node_num):
        self.antenna = Antenna  # 基站坐标，km
        self.point = Point  # 待测点坐标，km
        self.n = node_num  # 符合要求的基站数


    def needed_antenna(self, d):
        """
        :param d: 定义的距离范围
        :return: 符合要求的基站坐标antenna以及在list中的索引，方便之后找挂高
        """
        point = [[self.point[0], self.point[1], self.point[2]]]
        antenna = []
        index = []
        a = []
        # b = []
        for i in range(self.n):
            a1 = [self.antenna[0][i], self.antenna[1][i], self.antenna[2][i]]
            a.append(a1)
        b = cKDTree(a)
        x = b.query_ball_point(point[0], d)
        index.append(x)
        for i in range(len(index[0])):
            antenna.append(a[index[0][i]])
        # print index
        # print antenna
        return antenna, index


def All():
    RSRP = []
    SINR = []
    unused_point = []
    L = len(point_x)
    for i in range(L):
        print i + 1
        a_p = kDTree(Antenna, Point[i], node_num)
        needed_antenna, index = a_p.needed_antenna(d=1000)
        needed_node_num = len(needed_antenna)
        if needed_antenna is not []:
            r_p = relative_position(Point[i], needed_antenna, node_h_angle, node_v_angle, needed_node_num)
            point_after, dis = r_p.direction_down_angle()
            r_a = relative_angle(point_after, needed_node_num)
            alpha, beta = r_a.Angle()
            horizontal_data_gain, vertical_data_gain = find_gain()
            cal = calculate(point_after, Point[i], horizontal_data_gain,
                            vertical_data_gain, node_h, index, alpha, beta, dis, Pt, f, needed_node_num)
            # gain = cal.Gain()
            # loss = cal.Loss()
            rsrp, sinr = cal.Rsrp()
            RSRP.append(rsrp)
            SINR.append(sinr)
        else:
            unused_point.append(Point[i])
    num = 0
    yes_index = []
    no_index = []
    for i in range(len(RSRP)):
        if RSRP[i] >= -88 and SINR[i] >= -3:
        # if RSRP[i] >= -88:
            num += 1
            yes_index.append(i)
        else:
            no_index.append(i)
    new_yes_x = []
    new_yes_y = []
    new_no_x = []
    new_no_y = []
    for i in yes_index:
        new_yes_x.append(point_x[i])
        new_yes_y.append(point_y[i])
    for i in no_index:
        new_no_x.append(point_x[i])
        new_no_y.append(point_y[i])
    print '           The unused point is:', unused_point
    print 'The number of >= -88dBm & -3dB:', num
    # print '       The number of >= -88dBm:', num
    print '      The number of test point:', len(RSRP)
    m = round(num / len(RSRP) * 100, 2)
    print '         The satisfaction rate:', m, '%'
    return RSRP, SINR, new_yes_x, new_yes_y, new_no_x, new_no_y, m, unused_point

def new_point(p, q, h):
    Point = []
    for i in range(len(p)):
        m = [p[i], q[i], h, 1]
        Point.append(m)
    # print Point
    return Point

Pt = 18.2  #dBm
f = 900  #MHz
node_x, node_y, node_h, node_h_angle, node_v_angle, point_x, point_y = data()
node_num = len(node_x)
Point = new_point(point_x, point_y, 1.7)
# Point = [3724.359, 2264.9, 12, 1]
Antenna = [node_x, node_y, node_h, 1]

def main():
    RSRP, SINR, new_yes_x, new_yes_y, new_no_x, new_no_y, m, unused_point = All()
    plt.scatter(new_yes_x, new_yes_y, c='g', alpha=0.2, lw=1, marker=".")
    plt.scatter(new_no_x, new_no_y, c='r', alpha=0.2, lw=1, marker=".")
    x = [0] * len(unused_point)
    y = [0] * len(unused_point)
    for i in range(len(unused_point)):
        x[i] = unused_point[i][0]
        y[i] = unused_point[i][1]
    plt.scatter(x, y, c='c', alpha=0.1, lw=1, marker=".")
    plt.scatter(node_x, node_y, c='k', alpha=1, lw=1, marker="^")
    plt.xlabel('x/m')
    plt.ylabel('y/m')
    plt.text(5000, 2500, str(m)+'%')
    plt.text(5000, 2600, 'RSRP & SINR')
    plt.savefig('RSRP & SINR.png')
    # plt.text(5000, 2600, 'RSRP')
    # plt.savefig('RSRP.png')
    plt.show()



if __name__ == '__main__':
    main()