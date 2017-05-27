# -*- coding=utf-8 -*-
from __future__ import division
import cairo
import numpy as np
# import matplotlib.pyplot as plt
from numpy import pi, log10
import xlrd
from copy import deepcopy


class Antenna:
    def __init__(self, x, y, h, h_angle, v_angle):
        self.x = x*10  # 天线的横坐标
        self.y = y*10  # 天线的纵坐标
        self.h = h  # 天线的高度
        self.h_a = h_angle  # 水平角
        self.v_a = v_angle  # 下倾角

    def draw(self, cr, n):
        """
        :param cr: 
        :param n: 画一竖，一竖有n个高度
        :return: 
        """
        cr.move_to(self.x, self.y + 200*n)  # 移到基站坐标处
        # 画圆arc(起始横坐标，起始纵坐标，起始角度【x轴正方向为起始方向，逆时针为正角度】，终止角度)
        cr.arc(self.x, self.y + 200*n, 20,
               degree_to_rad(self.h_a - 30),
               degree_to_rad(self.h_a + 30))
        cr.line_to(self.x, self.y + 200*n)  # 开始画
        cr.stroke()
        pass


class Region(object):
    def __init__(self, antennas):
        self.antennas = antennas

    def draw(self, cr, Pr, n):
        r = 0  # 红色个数
        y = 0  # 黄色个数
        g = 0  # 绿色个数
        for i in range(len(Pr)):
            for j in range(len(Pr[0])):
                if Pr[i][j] > 20:
                    cr.set_source_rgba(1, 0, 0, 0.5)
                    r += 1
                elif Pr[i][j] > 17:
                    cr.set_source_rgba(1, 1, 0, 0.5)
                    y += 1
                elif Pr[i][j] > 0:
                    cr.set_source_rgba(0, 1, 0, 0.5)
                    g += 1
                # 给每个点填充颜色
                cr.rectangle(i * 10, j * 10 + 200 * n, 9.5, 9.5)
                cr.fill()
        # 画整个图的框
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(0, 0 + 200 * n, W * 10 - 2, H * 10 + 200 * n)
        cr.set_line_width(1)
        cr.stroke()
        for a in self.antennas:
            a.draw(cr, n)
        return r, y, g



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


def cal_P(get_gain, dis):
    a = 300./f  # 波长
    p = Pt  # W
    # gain = 10**(np.array(get_gain)/10.)
    gain = get_gain
    PR = []
    # # Pr = []
    for i in range(len(get_gain)):
        b = p*gain[i]*a**2
        c = 4*(pi*dis[i])**2
        d = b/c
        PR.append(d)
    s = deepcopy(PR)
    s1 = np.array(s)  # W
    s2 = sum(s1)
    Pr = 10*log10(s2*1000)  #dBm

    # print s2
    print 'The Pr of point is:', np.round(Pr, 5), 'dBm'
    print '-----'
    # print min(PR), max(PR), len(PR)
    return Pr

def cal_dis(Antanna_x, Antanna_y, Antanna_h, Point, n):
    dis = []
    for i in range(n):
        d = np.sqrt((Antanna_x[i] - Point[0]) ** 2 +
                    (Antanna_y[i] - Point[1]) ** 2 +
                    (Antanna_h[i] - Point[2]) ** 2)
        dis.append(d)
    return  dis


W = 50  # m
H = 20  # m
Pt = 20  # W
f = 900  # MHz

def main():
    n = 12
    h = [1.7, 2.0, 2.4, 3.0]  # 待测点的高度
    antennas, Antanna_x, Antanna_y, Antanna_h, h_angle, v_angle = data()
    # h_d_g, v_d_g = gain()
    point_x = range(0, 50, 1)
    point_y = range(0, 20, 1)
    Pr1 = []
    Pr = []
    get_Gain = [10] * 12
    for i in range(len(h)):
        Point = new_point(point_x, point_y, h[i])
        for j in range(len(Point)):
            dis = cal_dis(Antanna_x, Antanna_y, Antanna_h, Point[j], n)
            pr = cal_P(get_Gain, dis)
            Pr1.append(pr)
        Pr.append(Pr1)
        Pr1 = []
    # print min(Pr), max(Pr)

    pixel_per_m = 2
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W*10*pixel_per_m), int(len(h)*H*10*pixel_per_m))
    cr = cairo.Context(surface)
    cr.scale(pixel_per_m, pixel_per_m)
    cr.translate(1, 1)
    text = ['China Mobile', 'China Mobile', 'China Mobile',
            'China Unicom', 'China Unicom', 'China Unicom',
            'China Telecom', 'China Telecom', 'China Telecom',
            'China Mi', 'China Mi', 'China Mi']
    # text = ['China Mobile', 'China Unicom', 'China Telecom', 'China Mi']
    for i in range(len(h)):
        PR = np.reshape(Pr[i], (50, 20))
        r = Region(antennas)
        red, yellow, green = r.draw(cr, PR, i)
        colors = 'Red: %d, Yellow: %d, Green: %d' % (red, yellow, green)
        total = '   All: %d' % 1000
        cr.move_to(10, 10 + 200 * i)
        cr.set_font_size(10)
        # cr.set_source_rgb(0, 0, 0)
        cr.show_text(str(h[i]))
        cr.move_to(10, 20 + 200 * i)
        cr.show_text(total)
        cr.move_to(10, 30 + 200 * i)
        cr.show_text(str(colors))
        for j in range(0, len(Antanna_x), 3):
            cr.move_to(Antanna_x[j] * 10, Antanna_y[j] * 10 + 200 * i)
            cr.set_font_size(7)
            # cr.set_source_rgb(0, 0, 0)
            cr.show_text(text[j])
    surface.write_to_png(u'信号强度.png')


if __name__ == '__main__':
    main()