# -*- coding=utf-8 -*-
# Python 2.7
import re
import sys

# 测试匹配中文信息
def TestReChinese():
    source = u"    机器学习----MachingLearning非常难[支持向量机&&贝叶斯分类器](Python语言实现)"
    temp = source.decode('utf8')
    print "同时匹配中文英文"
    print "--------------------------"
    xx = u"[\w\W\u4e00-\u9fff]+"
    pattern = re.compile(xx)
    results = pattern.findall(temp)
    for result in results:
        print result
    print "--------------------------"
    print
    print
    print "只匹配中文"
    print "--------------------------"
    xx = u"([\u4e00-\u9fff]+)"
    pattern = re.compile(xx)
    results = pattern.findall(temp)

    for result in results:
        print result
    print "--------------------------"


if __name__ == "__main__":
    # 测试正则表达式
    # Python3不需要sys模块转换编码方式
    reload(sys)
    sys.setdefaultencoding("utf-8")
    TestReChinese()
