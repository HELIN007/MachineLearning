# -*- coding=utf-8 -*-
from __future__ import division
import cairo
import numpy as np
# import matplotlib.pyplot as plt
from numpy import pi, cos, sin, log10, sqrt
import xlrd
from copy import deepcopy


class Antenna:
    def __init__(self, x, y, h, h_angle, v_angle):
        self.x = x*10
        self.y = y*10
        self.h = h
        self.h_a = h_angle
        self.v_a = v_angle

    def draw(self, cr):
        cr.move_to(self.x, self.y)
        cr.arc(self.x, self.y, 20, degree_to_rad(self.h_a - 30), degree_to_rad(self.h_a + 30))
        cr.line_to(self.x, self.y)
        cr.stroke()
        pass


class Region(object):
    def __init__(self, antennas):
        self.antennas = antennas

    def draw(self, cr, Pr):
        # cr.rectangle(1, 1, W*10-4, H*10-4)
        cr.rectangle(0, 0, W * 10-2, H * 10-2)
        cr.set_line_width(1)
        # cr.fill()
        cr.stroke()
        for a in self.antennas:
            a.draw(cr)
        for i in range(len(Pr)):
            for j in range(len(Pr[0])):
                cr.set_source_rgba(0.2, 0.3, Pr[i][j]/10-1, 0.5)
                # cr.set_source_rgba(1, 0, 0, 0.5)
                cr.rectangle(i*10, j*10, 9.9, 9.9)
                cr.fill()


class relative_position:
    """
    求待测点相对于基站的坐标
    """
    def __init__(self, Point, Antanna_x, Antanna_y, Antanna_h, horizontal_angle, vertical_angle, n):
        self.point = Point  # 待测点
        self.x = Antanna_x
        self.y = Antanna_y
        self.h = Antanna_h  # 所符合要求的基站
        self.alpha = -np.array(horizontal_angle)/180.*pi  # 水平角
        self.beta = np.array(vertical_angle)/180.*pi  # 下倾角
        self.n = n  # 基站数


    def direction_down_angle(self):
        # 矩阵化
        mPoint = np.matrix(self.point)
        # n = len(self.antenna)
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
                 [-self.x[i], -self.y[i], -self.h[i], 1]]
            mR = np.matrix(R)
            mT = np.matrix(T)
            after = mPoint*mT*mR
            Point_after.append(after)
        Point_after = np.round(Point_after, 5)
        for i in range(len(Point_after)):
            d = np.sqrt((self.x[i] - self.point[0]) ** 2 +
                          (self.y[i] - self.point[1]) ** 2 +
                          (self.h[i] - self.point[2]) ** 2)
            dis.append(d)
        # dis = np.round(dis, 5)
        # print '              The point_after is:', Point_after
        # print '                  The distant is:', dis, 'm'
        return Point_after, dis


class relative_angle:
    """
    求待测点相对于基站的水平角和下倾角
    """
    def __init__(self, point_after, n):
        self.p_a = point_after  # 待测点的新坐标
        self.n = n  # 符合要求的基站数


    def Angle(self):
        alpha = []
        beta = []
        for i in range(self.n):
            m = np.sqrt(self.p_a[i, 0, 0]**2 + self.p_a[i, 0, 1]**2)
            n = np.sqrt(self.p_a[i, 0, 0]**2 + self.p_a[i, 0, 1]**2 + self.p_a[i, 0, 2]**2)
            if m != 0:
                if self.p_a[i, 0, 1] < 0:
                    a = 360 - np.arccos(self.p_a[i, 0, 0]/m)*180./pi
                else:
                    a = np.arccos(self.p_a[i, 0, 0] / m) * 180. / pi
                alpha.append(int(a))
            else:
                alpha.append(0)
            if n != 0:
                b =90 - np.arccos(abs(self.p_a[i, 0, 2])/n)*180./pi
                beta.append(int(b))
            else:
                beta.append(90)
        # print 'The angle with new alpha axis is:', alpha, 'degree'
        # print ' The angle with new beta axis is:', beta, 'degree'
        return alpha, beta


def degree_to_rad(d):
    return d*pi/180.

def new_point(p, q, h):
    Point = []
    for i in range(len(p)):
        for j in range(len(q)):
            m = [p[i], q[j], h, 1]
            Point.append(m)
    return Point

def data():
    Antanna = xlrd.open_workbook('antenna12.xlsx')
    Antanna_table = Antanna.sheets()[0]
    Antanna_x = Antanna_table.col_values(0)
    Antanna_y = Antanna_table.col_values(1)
    Antanna_h = Antanna_table.col_values(2)
    Antanna_hangle = Antanna_table.col_values(3)
    Antanna_vangle = Antanna_table.col_values(4)
    antennas = []
    for i in range(len(Antanna_hangle)):
        A = Antenna(Antanna_x[i], Antanna_y[i], Antanna_h[i], Antanna_hangle[i], Antanna_vangle[i])
        antennas.append(A)
    return antennas, Antanna_x, Antanna_y, Antanna_h, Antanna_hangle, Antanna_vangle


def gain():
    Gain = xlrd.open_workbook('angle.xlsx')
    Gain_table = Gain.sheets()[0]
    horizontal_data_angle = Gain_table.col_values(1)
    vertical_data_angle = Gain_table.col_values(2)
    return horizontal_data_angle, vertical_data_angle

def Gain(n, alpha, beta, h_d_g, v_d_g):
    """
    :return: 待测点相对于每个基站的增益
    """
    Gain = []
    for i in range(n):
        a = (pi - abs(alpha[i])/180.*pi)/pi*(h_d_g[0]-v_d_g[beta[i]])
        b = abs(alpha[i])/180.*(h_d_g[179]-v_d_g[179-beta[i]])
        g = h_d_g[alpha[i]] - a - b
        Gain.append(g)
    # print '            The gain of point is:', np.round(Gain, 5), 'dB'
    return Gain



def cal_P(get_gain, dis):
    a = 300./f  # 波长
    p = 10**(Pt/10)*1000  # W
    gain = 10**(np.array(get_gain)/10.)
    PR = []
    # Pr = []
    for i in range(len(get_gain)):
        b = p*(a**2)*gain[i]
        # b = p*get_gain[i]
        c = 4*(pi*dis[i])**2
        pr = b/c  # W
        PR.append(pr)
    s = deepcopy(PR)
    s1 = np.array(s)  # W
    s2 = sum(s1)
    Pr = 10*log10(s2)  #dBw
    # print '              The Pr of point is:', np.round(Pr, 5), 'dBm'
    print 'The Pr of point is:', np.round(Pr, 5), 'dBw'
    print '-----'
    print min(PR), max(PR)
    return Pr




W = 50  # m
H = 20  # m
Pt = 18.2  #dBm
f = 900  #MHz

def main():
    n = 12
    h = 1.7
    antennas, Antanna_x, Antanna_y, Antanna_h, h_angle, v_angle = data()
    h_d_g, v_d_g = gain()
    point_x = range(0, 50, 1)
    point_y = range(0, 20, 1)
    Point = new_point(point_x, point_y, h)
    Pr = []
    for i in range(len(Point)):
        r_p = relative_position(Point[i], Antanna_x, Antanna_y, Antanna_h, h_angle, v_angle, n)
        point_after, dis = r_p.direction_down_angle()
        ra = relative_angle(point_after, n)
        alpha, beta = ra.Angle()
        get_Gain = Gain(n, alpha, beta, h_d_g, v_d_g)
        pr = cal_P(get_Gain, dis)
        Pr.append(pr)
    Pr = np.reshape(Pr, (50, 20))



    pixel_per_m = 2
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W*10*pixel_per_m), int(H*10*pixel_per_m))
    cr = cairo.Context(surface)
    cr.scale(pixel_per_m, pixel_per_m)
    cr.translate(1, 1)
    r = Region(antennas)
    for i in range(0, len(Antanna_x), 3):
        cr.move_to(Antanna_x[i]*10, Antanna_y[i]*10)
        cr.set_font_size(5)
        cr.set_source_rgb(0, 0, 0)
        cr.show_text('node%d->%d' % (i+1, i+3))
    r.draw(cr, Pr)
    surface.write_to_png(u'信号强度.png')

if __name__ == '__main__':
    main()