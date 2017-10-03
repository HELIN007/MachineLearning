#coding=utf-8
from __future__ import division
import cython
cimport cython

import numpy as np
cimport numpy as np

from libc.math cimport sin, cos, sqrt, fabs

cdef double x_pi = 3.14159265358979324 * 3000.0 / 180.0
cdef double pi = 3.1415926535897932384626  # π
cdef double a = 6378245.0  # 长半轴
cdef double ee = 0.00669342162296594323  # 扁率

cdef double _transformlng(double lng, double lat):
    cdef double ret
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * sqrt(fabs(lng))
    ret += (20.0 * sin(6.0 * lng * pi) + 20.0 *
            sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(lng * pi) + 40.0 *
            sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * sin(lng / 12.0 * pi) + 300.0 *
            sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret

@cython.cdivision(True)
cdef double _transformlat(double lng, double lat):
    cdef double ret
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * sqrt(fabs(lng))
    ret += (20.0 * sin(6.0 * lng * pi) + 20.0 *
            sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(lat * pi) + 40.0 *
            sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * sin(lat / 12.0 * pi) + 320 *
            sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret
    
cdef void _wgs84_to_gcj02(double lng, double lat, double *mglng, double *mglat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    cdef double dlat = _transformlat(lng - 105.0, lat - 35.0)
    cdef double dlng = _transformlng(lng - 105.0, lat - 35.0)
    cdef double radlat = lat / 180.0 * pi
    cdef double magic = sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * cos(radlat) * pi)
    mglat[0] = lat + dlat
    mglng[0] = lng + dlng
    return

def wgs84_to_gcj02(lng, lat):
    cdef double mglng
    cdef double mglat
    _wgs84_to_gcj02(lng, lat, &mglng, &mglat)
    return [mglng, mglat]
    

@cython.cdivision(True)
cdef void _gcj02_to_wgs84(double lng, double lat, double *mglng, double *mglat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    cdef double dlat = _transformlat(lng - 105.0, lat - 35.0)
    cdef double dlng = _transformlng(lng - 105.0, lat - 35.0)
    cdef double radlat = lat / 180.0 * pi
    cdef double magic = sin(radlat)
    magic = 1 - ee * magic * magic
    cdef double sqrtmagic = sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * cos(radlat) * pi)
    mglat[0] = lat + dlat
    mglng[0] = lng + dlng
    mglng[0] = lng * 2 - mglng[0]
    mglat[0] = lat * 2 - mglat[0]
    return

def gcj02_to_wgs84(lng, lat):
    cdef double mglng
    cdef double mglat
    _gcj02_to_wgs84(lng, lat, &mglng, &mglat)
    return [mglng, mglat]
    
DTYPE = np.float64
ctypedef np.float64_t DTYPE_t

#in-place
@cython.boundscheck(False)
@cython.wraparound(False)
def np_gcj02_to_wgs84(np.ndarray[DTYPE_t, ndim=2] f):
    cdef int imax = f.shape[0]
    cdef int i
    cdef DTYPE_t xo, yo
    for i in range(imax):
        x = f[i,0]
        y = f[i,1]
        _gcj02_to_wgs84(x, y, &xo, &yo)
        f[i, 0] = xo
        f[i, 1] = yo

        
#in-place
@cython.boundscheck(False)
@cython.wraparound(False)
def np_wgs84_to_gcj02(np.ndarray[DTYPE_t, ndim=2] f):
    cdef int imax = f.shape[0]
    cdef int i
    cdef DTYPE_t xo, yo
    for i in range(imax):
        x = f[i,0]
        y = f[i,1]
        _wgs84_to_gcj02(x, y, &xo, &yo)
        f[i, 0] = xo
        f[i, 1] = yo
