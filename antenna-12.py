# -*- coding=utf-8 -*-
import cairo
# import matplotlib.pyplot as plt
from numpy import pi
import xlrd


class Antenna:
    def __init__(self, x, y, h, h_angle, v_angle):
        self.x = x
        self.y = y
        self.h = h
        self.h_a = h_angle
        self.v_a = v_angle

    def draw(self, cr):
        cr.move_to(self.x, self.y)
        cr.arc(self.x, self.y, 50, degree_to_rad(self.h_a - 30), degree_to_rad(self.h_a + 30))
        cr.line_to(self.x, self.y)
        cr.stroke()
        pass


class Region(object):
    def __init__(self, antennas):
        self.antennas = antennas

    def draw(self, cr):
        cr.rectangle(1, 1, W-4, H-4)
        cr.set_line_width(1)
        cr.stroke()
        for a in self.antennas:
            a.draw(cr)


def degree_to_rad(d):
    return d*pi/180.

W = 500  # m
H = 200  # m


def main():
    Antanna = xlrd.open_workbook('antenna12.xlsx')
    Antanna_table = Antanna.sheets()[0]
    Antanna_x = Antanna_table.col_values(0)
    Antanna_y = Antanna_table.col_values(1)
    Antanna_h = Antanna_table.col_values(2)
    Antanna_hangle = Antanna_table.col_values(3)
    Antanna_vangle = Antanna_table.col_values(4)
    antennas = []
    point_x = range(0, 500, 10)
    point_y = range(0, 200, 10)
    for i in range(len(Antanna_hangle)):
        A = Antenna(Antanna_x[i], Antanna_y[i], Antanna_h[i], Antanna_hangle[i], Antanna_vangle[i])
        antennas.append(A)
    pixel_per_m = 2
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W*pixel_per_m), int(H*pixel_per_m))
    cr = cairo.Context(surface)
    cr.scale(pixel_per_m, pixel_per_m)
    cr.translate(1, 1)
    r = Region(antennas)
    for i in range(0, len(Antanna_x), 3):
        cr.move_to(Antanna_x[i], Antanna_y[i])
        cr.set_font_size(10)
        cr.set_source_rgb(0, 0, 0)
        cr.show_text('node%d->%d' % (i+1, i+3))
    r.draw(cr)
    surface.write_to_png('antennas.png')

if __name__ == '__main__':
    main()