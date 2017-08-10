# -*- coding=utf-8 -*-
# Python 2.7
from numpy import sin, cos, tan, arccos, arctan, radians


class change_axis:
    def __init__(self, x, y, n):
        self.x = x  # 经度
        self.y = y  # 维度
        self.n = n  # 待转换点的数量

    def axis(self):
        """
        :return: 以node_0为参考点，返回每个基站的新坐标（距离单位为km）
        """
        node_0 = [103.588810, 36.023888]
        new_x = []
        new_y = []
        for i in range(self.n):
            xx = self.calcDistance(node_0[0], node_0[1], self.x[i], node_0[1])
            new_x.append(xx)
            yy = self.calcDistance(node_0[0], node_0[1], node_0[0], self.y[i])
            new_y.append(yy)
        return new_x, new_y

    def calcDistance(self, Lng_A, Lat_A, Lng_B, Lat_B):
        ra = 6378.140  # 赤道半径 (km)
        rb = 6356.755  # 极半径 (km)
        flatten = (ra - rb) / ra  # 地球扁率
        rad_lat_A = radians(Lat_A)
        rad_lng_A = radians(Lng_A)
        rad_lat_B = radians(Lat_B)
        rad_lng_B = radians(Lng_B)
        pA = arctan(rb / ra * tan(rad_lat_A))
        pB = arctan(rb / ra * tan(rad_lat_B))
        xx = arccos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(rad_lng_A - rad_lng_B))
        c1 = (sin(xx) - xx) * (sin(pA) + sin(pB)) ** 2 / cos(xx / 2) ** 2
        c2 = (sin(xx) + xx) * (sin(pA) - sin(pB)) ** 2 / sin(xx / 2) ** 2
        dr = flatten / 8 * (c1 - c2)
        distance = ra * (xx + dr)
        return distance


def main():
    LonLat_To_XY = change_axis([103.588810], [37.023888], 1)
    x, y = LonLat_To_XY.axis()
    print x, y


if __name__ == '__main__':
    main()
