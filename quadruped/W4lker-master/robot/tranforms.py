__author__ = 'will'
import numpy as np
import math


def get_axis(axis):
    if axis == "x":
        return [1, 0, 0]
    elif axis == "y":
        return [0, 1, 0]
    elif axis == "z":
        return [0, 0, 1]
    else:
        return axis

def distance(a, b):
    return math.sqrt((b[0]-a[0])**2 +(b[1]-a[1])**2 +(b[2]-a[2])**2)

def rotateAroundCenter(matrix, axis, theta):
    axis = get_axis(axis)
    axis = np.asarray(axis)
    theta = np.asarray(theta)
    axis = axis/math.sqrt(np.dot(axis, axis))
    a = math.cos(theta/2)
    b, c, d = -axis*math.sin(theta/2)
    aa, bb, cc, dd = a*a, b*b, c*c, d*d
    bc, ad, ac, ab, bd, cd = b*c, a*d, a*c, a*b, b*d, c*d
    rot = np.array([[aa+bb-cc-dd, 2*(bc+ad), 2*(bd-ac)],
                     [2*(bc-ad), aa+cc-bb-dd, 2*(cd+ab)],
                     [2*(bd+ac), 2*(cd-ab), aa+dd-bb-cc]])
    return np.dot(rot, matrix)

def rotate(matrix, axis, theta, center=None):
    if not center:
        center = np.matrix([[0],[0],[0]])
    else:
        center = np.matrix(center)
    matrix = np.matrix(matrix)
    if matrix.shape[0] ==1:
        matrix = np.transpose(matrix)

    if center.shape[0] ==1:
        center = np.transpose(center)
    # print center
    # print matrix

    dislocated = np.subtract(matrix, center)
    # print dislocated
    rotated = rotateAroundCenter(dislocated, axis, theta)
    # print rotated
    relocated = np.add(rotated, center)
    return relocated

test = [[1], [0], [0]]

print (rotate(test, 'y', math.pi, [0, 1, 0]))

