# -*- utfcoding=utf-8 -*-
# python 2.7
from numpy import array, tile


class KNN:
    # 定义四个点,前两个点代表A类，后两个点代表B类
    def createDataset(self):
        group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
        labels = ['A', 'A', 'B', 'B']
        return group, labels

    def KnnClassify(self, testX, trainX, labels, K):
        [N, M] = trainX.shape  # N为行数，M为列数
        # calculate the distance between testX and other training samples
        # tile使得textX变成了N行1列，- trainXtile里面是减去trainX里相应的数
        difference = tile(testX, (N, 1)) - trainX
        # print difference
        difference = difference**2  # take pow(difference,2)
        # print difference
        distance = difference.sum(axis=1)  # 按行求和（axis=1）take the sum of difference from all dimensions
        # print distance
        distance = distance**0.5
        # print distance
        sortdiffidx = distance.argsort()  # 从小到大排列数组，返回序列值
        # find the k nearest neighbours
        vote = {}  # create the dictionary
        for i in range(K):
            ith_label = labels[sortdiffidx[i]]
            # print ith_label
            vote[ith_label] = vote.get(ith_label, 0) + 1
            # print vote[ith_label]
            # print vote
            # get(ith_label,0) : if dictionary 'vote' exist key 'ith_label',return vote[ith_label]; else return 0
        # print sorted(vote.iteritems())
        sortedvote = sorted(vote.iteritems(), key=lambda x: x[1], reverse=True)
        # print sortedvote
        # 'key = lambda x: x[1]' can be substituted by operator.itemgetter(1)
        return sortedvote[0][0]


k = KNN()  # create KNN object
group, labels = k.createDataset()
cls = k.KnnClassify([0, 0], group, labels, 3)
print cls
