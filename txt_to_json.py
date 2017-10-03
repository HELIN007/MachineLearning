# -*- coding=utf-8 -*-
# Python 2.7
"""
待测点的数据（经纬度、海拔、地形信息）预处理，
此代码还将经纬度换为 km ，以 lanzhou 为中心，
数据存储在 json 格式中。
"""
from __future__ import print_function, unicode_literals
import codecs
import simplejson as json
from coordconv import gcj02_to_wgs84

# lanzhou 经纬度
center_x = 103.75
center_y = 36.09

# 转为以 lanzhou 为中心的 km 坐标
def map(lon, lat):
    new_x = (lon - center_x) * 89.957
    new_y = (lat - center_y) * 110.574
    return new_x, new_y

def save_json():
    kind_set = set()
    bb = []
    with open("heightInfo.txt", "r") as f:
        for line in f:
            if len(line.strip()) == 0:
                continue
            records = line.split("\t")
            lon = float(records[0])
            lat = float(records[1])
            height = float(records[2])
            kind = records[3].strip()
            kind_set.add(kind)
            x1, y1 = gcj02_to_wgs84(lon, lat)
            xn, yn = map(x1, y1)
            sample = {
                "x": xn,
                "y": yn,
                "lon": x1,
                "lat": y1,
                "kind": kind,
                "height": height
            }
            bb.append(sample)
    with codecs.open('all_sample.json', 'w', "utf-8") as f:
        json.dump(bb, f, ensure_ascii=False, sort_keys=True, indent=4*' ')
    print(kind_set)
save_json()
