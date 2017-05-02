# -*- coding=utf-8 -*-
# python2.7
import matplotlib.pyplot as plt
# from images2gif import writeGif
# import glob
# from PIL import Image


def BubbleSort(alist):
    """
    :param alist: The given list
    :return: The sorted list and the number of picture
    """
    k = 0
    time = 1
    for i in range(len(alist)):
        k += 1
        for j in range(len(alist)-k):
            if alist[j] > alist[j+1]:
                alist[j], alist[j + 1] = alist[j + 1], alist[j]
            drawFig(alist, i, j, time)
            time += 1
    return alist, time - 1


def drawFig(alist, x, y, k):
    """
    :param alist: The given list
    """
    plt.plot(range(len(alist)), alist, 'o-')
    # 给每个点写注释
    for i in range(0, len(alist)):
        # plt.text(i, alist[i], str((i, alist[i])),
        #          family='serif', style='italic', ha='right', wrap=True)
        plt.text(i, alist[i], alist[i], fontsize=15)
        plt.text(2, 6, 'The %d change!' % k)
    plt.xlabel('x AXIS')
    plt.ylabel('y AXIS')
    plt.savefig('No.%d-%d%d.png' % (k, x, y))
    plt.show()


"""
# 无法存储
def drawGif():
    images = [Image.open(image) for image in glob.glob('F:\MachineLearning\*.png')]
    GifName = 'BubbleSort.gif'
    writeGif(GifName, images, duration=0.1)
"""


a = [5, 1, 4, 2, 8]
BubbleSortedList = BubbleSort(a)
print BubbleSortedList

