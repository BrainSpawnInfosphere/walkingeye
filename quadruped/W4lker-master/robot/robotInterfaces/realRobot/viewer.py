from matplotlib import pyplot as plt

import time
from pylab import ion
import pylab
# plt.show()

#NOT USED ANYMORE, KEPT FOR POSTERITY
###



leg_index = {"front_left": 0,
        "front_right": 1,
        "rear_right": 2,
        "rear_left": 3}


def create():
    global fig
    fig = plt.figure(0)
    ax1 = fig.add_subplot(211)
    ax1.set_aspect("equal")
    pylab.ylim([-100, 100])
    pylab.xlim([-100, 100])
    # ax1.plot([(1, 2), (3, 4)], [(4, 3), (2, 3)])
    ax2 = fig.add_subplot(212)

    ax2.set_aspect("equal")
    # ax2.plot([(7, 2), (5, 3)], [(1, 6), (9, 5)])

    ion()
    global patch
    patch = plt.Polygon([[0, 0],
                         [0, 3],
                         [3, 0]], fc='y')
    ax1.add_patch(patch)
    pylab.ylim([-200, 200])
    pylab.xlim([-200, 200])

    global body
    body = plt.Polygon([[-50, 75],
                        [50, 75],
                        [50, -75],
                        [-50, -75],], fc='y')
    global legs
    legs = []
    for i in range(4):
        l = plt.Polygon([[0, 0]], fc='g')
        legs.append(l)
        ax2.add_patch(l)

    ax2.add_patch(body)



def update_lines(lines):
    patch.set_xy(lines)
    fig.canvas.draw()
    plt.pause(0.0001)


def update_body(body,legs_coords):
    body.set_xy(body)
    fig.canvas.draw()
    plt.pause(0.0001)

def update_leg(leg,polygon):
    legs[leg_index[leg]].set_xy(polygon)
    fig.canvas.draw()
    # print "legs:", legs
    plt.pause(0.0001)