# -*- coding=utf-8 -*-
# python2.7
import matplotlib.pyplot as plt
from images2gif import writeGif
import glob
from PIL import Image

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
            plt.savefig('%d%d' % (i, j))
            plt.show()
    return alist


images = [Image.open(image) for image in glob.glob('**.png')]
GifName = '1.gif'
writeGif(GifName, images, duration=0.1)

a = [5, 1, 4, 2, 8]
BubbleSortedList = BubbleSort(a)
print BubbleSortedList
