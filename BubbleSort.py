# -*- coding=utf-8 -*-
# python2.7


a = [5, 1, 4, 2, 8]
def BubbleSort(alist):
    """
    :param alist: a given list
    :return: a sorted list
    """
    for i in range(len(alist)-1):
        for j in range(len(alist)-1):
            if alist[j] > alist[j+1]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]
                print alist
    return alist

print BubbleSort(a)