# -*- coding:utf-8 -*-
'''
@Project     : lb_toolkits

@File        : basic.py

@Modify Time :  2022/10/31 15:52   

@Author      : Lee    

@Version     : 1.0   

@Description :

'''
import os
import sys
import numpy as np
import datetime

Deg2Rad = 180.0/np.pi
Rad2Deg = np.pi/180.0

def calc_earth_distance(lat1, lon1, lat2, lon2) :
    '''  计算球面两点之间距离（KM） '''
    lon11 = lon1 * Deg2Rad
    lat11 = lat1 * Deg2Rad
    lon21 = lon2 * Deg2Rad
    lat21 = lat2 * Deg2Rad

    dlon = lon21 - lon11
    dlat = lat21 - lat11
    h = np.sin(dlat/2)**2 + np.cos(lat11) * np.cos(lat21) * np.sin(dlon/2)**2
    distance = 2 * 6371.009 * np.arcsin(np.sqrt( h )) # 地球平均半径，6371km

    return distance

def planck_t2r(bt, wn):
    '''
    普朗克函数：将亮温（K）转成辐射值

    Parameters
    ----------
    bt : numpy.narray
        bright temperature, units: K
    wn : float or numpy.narray
        wave number(cm^-1)

    Returns
    -------
        numpy.narray
        卫星观测辐射值，mW/(m2.cm-1.sr)

    '''
    Radiation_C1 = 1.191042953E-5
    Radiation_C2 = 1.4387774
    a = Radiation_C1 * wn * wn * wn
    b = (Radiation_C2 * wn) / bt
    c = np.exp(b) - 1.0
    radi = a / c

    return radi


def planck_r2t(rad, wn):
    '''
    普朗克函数：将辐射值转成亮温（K）

    Parameters
    ----------
    rad : numpy.narray
        mW/(m2.cm-1.sr)
    wn : float or numpy.narray
        wave number(cm^-1)

    Returns
    -------
        numpy.narray
        bright temperature
        units: K
    '''

    Radiation_C1 = 1.191042953E-5
    Radiation_C2 = 1.4387774
    vs = wn
    bt = (Radiation_C2*vs/np.log(Radiation_C1*vs*vs*vs/(rad)+1.0))

    return bt
