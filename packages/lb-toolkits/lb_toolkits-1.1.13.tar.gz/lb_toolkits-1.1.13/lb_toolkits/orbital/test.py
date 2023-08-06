# coding:utf-8
'''
@Project  : CalOrbit
@File     : test.py
@Modify Time      @Author    @Version    @Desciption
--------------    -------    --------    -----------
2022/1/21 18:01      Lee       1.0         
 
'''

import itertools

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def data_gen():
    for cnt in itertools.count():
        t = cnt / 10
        yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)


def init():
    ax.set_ylim(-1.1, 1.1)
    ax.set_xlim(0, 10)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)
    return line,

import datetime
import time
from pyorbital import orbital
from orbital import Orbital

if __name__ == "__main__":
    obs_lon, obs_lat = 12.4143, 55.9065
    obs_alt = 0.02
    o = Orbital(satellite="FY-3D")

    # t_start = datetime.datetime.now()
    # t_stop = t_start + timedelta(minutes=20)
    # t = t_start
    while True:
        # t += timedelta(seconds=15)

        t = datetime.datetime.utcnow()
        lon, lat, alt = o.get_lonlatalt(t)
        # lon, lat = np.rad2deg((lon, lat))
        az, el = o.get_observer_look(t, obs_lon, obs_lat, obs_alt)
        ob = o.get_orbit_number(t, tbus_style=True)
        print(lon, lat, az, el, ob)
        time.sleep(5)




# fig, ax = plt.subplots()
# line, = ax.plot([], [], lw=2)
# ax.grid()
# xdata, ydata = [], []
#
#
# def run(data):
#     # update the data
#     t, y = data
#     xdata.append(t)
#     ydata.append(y)
#     xmin, xmax = ax.get_xlim()
#
#     if t >= xmax:
#         ax.set_xlim(xmin, 2*xmax)
#         ax.figure.canvas.draw()
#     line.set_data(xdata, ydata)
#
#     return line,
#
# ani = animation.FuncAnimation(fig, run, data_gen, interval=10, init_func=init)
# plt.show()

