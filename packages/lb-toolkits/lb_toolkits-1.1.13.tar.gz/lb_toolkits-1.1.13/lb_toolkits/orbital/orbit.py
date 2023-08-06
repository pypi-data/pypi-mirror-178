# coding:utf-8
'''
@Project: WordUtil.py
-------------------------------------
@File   : orbital.py
-------------------------------------
@Modify Time      @Author    @Version    
--------------    -------    --------
2022/1/7 15:15     Lee        1.0         
-------------------------------------
@Desciption
-------------------------------------

'''

import time

from orbital import Orbital
import datetime

import itertools

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def data_gen():
    # for cnt in itertools.count():
    #     t = cnt / 10
    #
    #     yield t, np.sin(2*np.pi*t) * np.exp(-t/10.)
    now =  datetime.datetime.utcnow()
    print(now)
    for i in range(1000):
        x = now + datetime.timedelta(seconds=i)
        lon, lat, alt = orb.get_lonlatalt(x)
        # print(lon, lat)
        # print(orb.get_observer_look(now, lon, lat, alt))
        # time.sleep(1)
        yield lon, lat
    # Get normalized position and velocity of the satellite:
    # print(orb.get_position(now))

    # Get longitude, latitude and altitude of the satellite:
    # print(orb.get_lonlatalt(now))



def init():
    ax.set_ylim(-90, 90)
    ax.set_xlim(-180, 180)
    del xdata[:]
    del ydata[:]
    line.set_data(xdata, ydata)

    return line,




def run(data):
    # update the data
    t, y = data

    xdata.append(t)
    ydata.append(y)
    print(xdata, ydata)
    # xmin, xmax = ax.get_xlim()

    # if t >= xmax:
    #     ax.set_xlim(xmin, 2*xmax)
    #     ax.figure.canvas.draw()
    line.set_data(xdata, ydata)

    return line,



def test1():
    fig, ax = plt.subplots()

    x = np.arange(0, 2*np.pi, 0.01)
    line, = ax.plot(x, np.sin(x))


    def animate(i):
        line.set_ydata(np.sin(x + i / 50))  # update the data.
        return line


    ani = animation.FuncAnimation(
        fig, animate, interval=20, blit=True, save_count=50)

    plt.show()




if __name__ == '__main__':

    # Use current TLEs from the internet:
    # test1()

    orb = Orbital("FY-3D")

    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    ax.grid()
    xdata, ydata = [], []
    ani = animation.FuncAnimation(fig, run, data_gen, interval=10, init_func=init)
    plt.show()



