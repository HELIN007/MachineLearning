# -*- coding=utf-8 -*-
# python2.7
import matplotlib.pyplot as plt
import images2gif


def BubbleSort(alist):
    """
    :param alist: The given list
    :return: The sorted list
    """
    k = 0
    for i in range(len(alist)):
        k += 1
        for j in range(len(alist)-k):
            if alist[j] > alist[j+1]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]
            plt.plot(range(len(alist)), alist)
            plt.xlabel(u'x轴')
            plt.ylabel(u'y轴')
            # plt.savefig('Picture-%d%d' % (i, j))
            plt.show()
    return alist


a = [5, 1, 4, 2, 8]
BubbleSortedList = BubbleSort(a)
print BubbleSortedList
