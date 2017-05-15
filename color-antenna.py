# -*- coding=utf-8 -*-
# python2.7
import numpy as np
from numpy import sin, cos, pi, tan, arctan, arccos, log10, radians
import matplotlib.pyplot as plt


class relative_position:
    """
    求待测点相对于基站的坐标
    """
    def __init__(self, Point, antenna, horizontal_angle, vertical_angle):
        self.point = Point  # 待测点
        self.antenna = antenna  # 所符合要求的基站
        self.alpha = horizontal_angle  # 水平角
        self.beta = vertical_angle  # 下倾角

    def direction_down_angle(self):
        # 矩阵化
        mPoint = np.matrix(self.point)
        # n = len(self.antenna)
        # 循环每个基站
        # 旋转矩阵
        R = [[cos(self.alpha)*cos(self.beta), -sin(self.alpha), cos(self.alpha)*sin(self.beta), 0],
             [sin(self.alpha)*cos(self.beta), cos(self.alpha), sin(self.alpha)*sin(self.beta), 0],
             [-sin(self.beta), 0, cos(self.beta), 0],
             [0, 0, 0, 1]]
        # 平移矩阵
        T = [[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [-self.antenna[0], -self.antenna[1], -self.antenna[2], 1]]
        mR = np.matrix(R)
        mT = np.matrix(T)
        Point_after = np.round(mPoint*mT*mR, 5)
        # print Point_after
        return Point_after

class relative_angle:
    """
    求待测点相对于基站的水平角和下倾角
    """
    def __init__(self, Point_after):
        self.p_a = Point_after  # 待测点的新坐标

    def Angle(self):
        alpha = []
        beta = []
        m = np.sqrt(self.p_a[0][0]**2 + self.p_a[0][1]**2)
        n = np.sqrt(self.p_a[0][0]**2 + self.p_a[0][1]**2 + self.p_a[0][2]**2)
        if m != 0:
            a = np.arccos(self.p_a[0, 0]/m)*180./pi
            alpha = int(a)
        else:
            alpha = 0
        if n != 0:
            b =90 - np.arccos(abs(self.p_a[0, 2])/n)*180./pi
            beta = int(b)
        else:
            beta = 90
        # print 'The angle with new alpha axis is:', alpha, 'degree'
        # print ' The angle with new beta axis is:', beta, 'degree'
        return alpha, beta

class calculate:
    def __init__(self, Point_after, h_d_g, v_d_g, alpha, beta, Pt, f):
        self.p_a = Point_after  # 待测点的新坐标
        self.h_d_g = h_d_g  # 水平增益，供查询
        self.v_d_g = v_d_g  # 垂直增益，供查询
        self.alpha = alpha  # 相对于基站的新水平角
        self.beta = beta  # 相对于基站的新下倾角
        self.Pt = Pt  # 发射功率
        self.f = f  # 发射频率
    def Gain(self):
        """
        :return: 待测点相对于每个基站的增益
        """
        a = (pi - abs(self.alpha)/180.*pi)/pi*(self.h_d_g[0]-self.v_d_g[self.beta])
        b = abs(self.alpha)/180.*(self.h_d_g[180]-self.v_d_g[180-self.beta])
        Gain = self.h_d_g[self.alpha] - a - b
        # print 'The gain is:', np.round(Gain, 5), 'dBm'
        return Gain
    def dis(self, alist):
        dis = np.sqrt(alist[0][0]**2+alist[0][1]**2+alist[0][2]**2)
        # print dis
        return dis
    def Loss(self, C=3):
        """
        :param C: C=3 for metropolitan areas
        :return: 待测点相对于每个基站的损耗
        """
        hR = 3  # km
        hT = 3  # m
        a = (1.1*log10(self.f)-0.7)*hR-(1.56*log10(self.f)-0.8)
        Loss = 46.3+33.9*log10(self.f)-13.82*log10(hT)-a+(44.9-6.55*log10(hT))*log10(self.dis(self.p_a))+C
        # print 'The Loss is:', Loss, 'dB'
        return Loss

    def RSRP(self):
        """
        :return: 待测点相对于每个基站的信号强度RSRP
        """
        Gain = self.Gain()
        Loss = self.Loss()
        RSRP = self.Pt + Gain - Loss
        # print '                     The RSRP is:', min(RSRP), 'dBm', '--->', max(RSRP), 'dBm'
        print 'The RSRP is:', round(RSRP, 5), 'dBm'
        print '-----'
        return round(RSRP, 5)

def load_gain():
    """
    :return: 水平角下倾角及相对应的增益、以供查询待测点的增益
    """
    Gain_data = np.loadtxt("C:\Users\LIN\Desktop\message\GSM900-gain.txt")
    Gain_list = np.reshape(Gain_data, (720, 2))
    Gain_angle = []
    Gain = []
    for i in range(720):
        Gain_angle.append(Gain_list[i][0])
        Gain.append(Gain_list[i][1])
    horizontal_data_angle = vertical_data_angle = Gain_angle[0:360]
    horizontal_data_gain = Gain[0:360]
    vertical_data_gain = Gain[360:720]
    return horizontal_data_angle, horizontal_data_gain, \
           vertical_data_angle,vertical_data_gain

def main():
    # 取精度
    x = range(2000, 4000, 20)
    x = np.array(x)/1000.
    y = range(2000, 4000, 20)
    y = np.array(y)/1000.
    antenna = [3, 3, 3, 1]
    rsrp = [[0.0 for i in range(100)] for j in range(100)]
    rsrp = np.array(rsrp)
    for i in range(len(x)):
        for j in range(len(y)):
            point = [x[i], y[j], 3, 1]
            horizontal_angle = pi/2
            vertical_angle = 0
            r_p = relative_position(point, antenna, horizontal_angle, vertical_angle)
            point_after = r_p.direction_down_angle()
            r_a = relative_angle(point_after)
            alpha, beta = r_a.Angle()
            horizontal_data_angle, horizontal_data_gain, \
            vertical_data_angle, vertical_data_gain = load_gain()
            cal = calculate(point_after, horizontal_data_gain, vertical_data_gain, alpha, beta, 18.2, 900)
            rsrp[i][j] = cal.RSRP()
    # num = 0
    # for i in rsrp:
    #     if i >= -88:
    #         num += 1
    # print num
    # print len(x)
    image = plt.imshow(rsrp, cmap='jet')  # hot/jet等各种颜色
    plt.colorbar(image)
    plt.show()


if __name__ == '__main__':
    main()


