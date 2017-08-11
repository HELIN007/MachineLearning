# -*- coding=utf-8 -*-
# Python 2.7
from numpy import sin, cos, tan, arccos, arctan, radians
import xlrd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def data():
    """
    读取数据
    :return: 经度、维度、海拔、地形地貌类型
    """
    A_P = xlrd.open_workbook('DiXingDiMao.xlsx')
    A_P_table = A_P.sheets()[0]
    Lon = A_P_table.col_values(0)  # 待测点精度
    Lat = A_P_table.col_values(1)  # 待测点纬度
    Hight = A_P_table.col_values(2)  # 待测点海拔
    Type = A_P_table.col_values(3)  # 待测点地形地貌类型
    return Lon, Lat, Hight, Type


class change_axis:
    """
    将经纬度坐标转换为笛卡尔坐标，参考点自己设置
    """
    def __init__(self, x, y, n):
        self.x = x  # 经度
        self.y = y  # 维度
        self.n = n  # 待转换点的数量

    def axis(self):
        """
        :return: 以node_0为参考点，返回每个基站的新坐标（距离单位为km）
        """
        node_0 = [103.8, 36.0]
        new_x = []
        new_y = []
        for i in range(self.n):
            xx = self.calcDistance(node_0[0], node_0[1], self.x[i], node_0[1])
            new_x.append(xx)
            yy = self.calcDistance(node_0[0], node_0[1], node_0[0], self.y[i])
            new_y.append(yy)
        # print '转换后x坐标：', new_x
        # print '转换后y坐标：', new_y
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

def Color(Type):
    """
    给每个地形地貌赋一个值、每个类型赋一个颜色
    :param Type: 地形地貌类型
    :return: 所有点的地形地貌颜色
    """
    C = []
    for h in Type:
        if h == 1:
            C.append('r')
        elif h == 2:
            C.append('salmon')
        elif h == 3:
            C.append('peru')
        elif h == 4:
            C.append('lime')
        elif h == 5:
            C.append('yellow')
        elif h == 6:
            C.append('grey')
        elif h == 7:
            C.append('pink')
        elif h == 8:
            C.append('blue')
        elif h == 9:
            C.append('darkred')
        elif h == 10:
            C.append('darkblue')
        elif h == 11:
            C.append('g')
    return C


def main():
    """
    经度范围：103.804532 -> 103.939891
    纬度范围：36.019794 -> 36.085647
    """
    Lon, Lat, Hight, Type = data()
    C = Color(Type)
    n = len(Lon)
    # 开始画图
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    LonLat_To_XY = change_axis(Lon, Lat, n)
    x, y = LonLat_To_XY.axis()
    ax.scatter(x, y, Hight, c=C, alpha=1)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_zlabel('Hight')
    plt.show()


if __name__ == '__main__':
    main()
