# -*- coding=utf-8 -*-
# Python2.7
import matplotlib.pyplot as plt
import numpy as np

# 发射功率
Pt = 20
# 天线增益
Gt = 1.0
Gr = 1.0
# 给定基站坐标位置
A = (1, 1, 1)
# 取整个平面
points = np.arange(0, 10, 0.01)
xs, ys = np.meshgrid(points, points)
zs = 5
# 上下倾角设置，随机生成另一定点确定天线朝向
# x = random.randint(2, 10)
# y = random.randint(2, 10)
# x, y = (np.random.random(2)-0.5)*10
# print x, y
x = 2
y = 1
alpha = np.pi / 3
# 天线正中间轴线的向量
Sl = (x - A[0], y - A[1], np.tan(alpha) * np.sqrt(x - A[0]**2 + (y - A[1])**2))
# 判断接收机是否在接受范围内
St = (xs - A[0], ys - A[1], zs - A[2])
beta = np.pi / 6
distant = np.sqrt((xs - A[0])**2 + (ys - A[1])**2 + (zs - A[2])**2)
a = Sl[0] * St[0] + Sl[1] * St[1] + Sl[2] * St[2]
b = np.sqrt(Sl[0]**2 + Sl[1]**2 + Sl[2]**2) * np.sqrt(
    St[0]**2 + St[1]**2 + St[2]**2)
c = np.arccos(a/b)
Pr = [[0.0 for i in range(1000)] for j in range(1000)]
Pr = np.array(Pr)
# 判断是否存在于辐射范围内并计算该点功率
for i, row in enumerate(c):
    for j, col in enumerate(row):
        if 0 <= col <= beta:
            Pr[i][j] = (Pt * Gt * Gr * (A[2]**2) *
                        (zs**2)) / (distant[i][j]**4)
print '所接收到的功率最小值：', np.amin(Pr)
print '所接收到的功率最大值：', np.amax(Pr)
# 画图
image = plt.imshow(Pr, cmap='jet')
plt.colorbar(image)
plt.show()
