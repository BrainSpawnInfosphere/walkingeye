#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import numpy as np
# import math
from math import sin, cos, acos, atan2, sqrt, pi
from math import radians as d2r
from math import degrees as r2d

"""
This file is needed by gait Trot class
"""

# FIXME: 20160625 add euler -> quaternion transform and reverse


def distance(a, b):
	"""
	Calculate the distance between pt a and pt b.
	in: vector a, vector b
	out: magnitude(b-a)
	"""
	return sqrt((b[0] - a[0])**2.0 + (b[1] - a[1])**2.0 + (b[2] - a[2])**2.0)
	# c = b-a
	# return sqrt(np.dot(c, c))


def rotateAroundCenter(matrix, axis, theta):
	"""
	not sure what this does

	in:
		matrix - ????
		axis of rotation - 'x', 'y', or 'z'
		theta - angle of rotation (rads)
	out: ???
	"""
	# axis = get_axis(axis)
	aa = [0, 0, 1]
	if axis == "x": aa = [1, 0, 0]
	elif axis == "y": aa = [0, 1, 0]
	# elif axis == "z": ret = [0, 0, 1]

	axis = np.asarray(aa)
	# theta = np.asarray(theta)
	axis = axis / sqrt(np.dot(axis, axis))  # normalizing axis
	a = cos(theta / 2.0)
	b, c, d = -axis * sin(theta / 2.0)
	aa, bb, cc, dd = a * a, b * b, c * c, d * d
	bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
	rot = np.array([
		[aa+bb-cc-dd, 2.0*(bc+ad), 2.0*(bd-ac)],
		[2.0*(bc-ad), aa+cc-bb-dd, 2.0*(cd+ab)],
		[2.0*(bd+ac), 2.0*(cd-ab), aa+dd-bb-cc]
	])

	return np.dot(rot, matrix)


# def rotate(matrix, axis, theta, center=None):
# 	"""
# 	how is this different???
# 	in:
# 		matix - ??
# 		axis - axis of rotation??
# 		theta - angle of rotation (rads)
# 	out: ???
# 	"""
# 	if not center:
# 		center = np.matrix([[0], [0], [0]])
# 	else:
# 		center = np.matrix(center)
# 	matrix = np.matrix(matrix)
# 	if matrix.shape[0] == 1:
# 		matrix = np.transpose(matrix)
#
# 	if center.shape[0] == 1:
# 		center = np.transpose(center)
# 	# print center
# 	# print matrix
#
# 	dislocated = np.subtract(matrix, center)
# 	# print dislocated
# 	rotated = rotateAroundCenter(dislocated, axis, theta)
# 	# print rotated
# 	relocated = np.add(rotated, center)
# 	return relocated


def rot(a, alpha, S, theta):
	"""
	Creates a DH rotation matrix for forward kinematics.
	"""
	return np.array([  # eqn 3.7 pg 36
		[cos(theta), -sin(theta), 0, a],
		[sin(theta) * cos(alpha), cos(theta) * cos(alpha), -sin(alpha), -sin(alpha) * S],
		[sin(theta) * sin(alpha), cos(theta) * sin(alpha), cos(alpha), cos(alpha) * S],
		[0, 0, 0, 1]
	])
	# return np.array([  # inverse of above ??
	# 	[cos(theta), sin(theta) * cos(alpha), sin(theta) * sin(alpha), -cos(theta) * a],
	# 	[-sin(theta), cos(theta) * cos(alpha), cos(theta) * sin(alpha), sin(theta) * a],
	# 	[0, -sin(alpha), cos(alpha), -S],
	# 	[0, 0, 0, 1]
	# ])


def T(params, phi):
	"""
	Creates a transform from the leg frame to the foot.

	params = [[a, alpha, S, theta],[a, alpha, S, theta],...]
	"""
	# handle the base frame, eqn 3.9, p36
	t = np.array([
		[cos(phi), -sin(phi), 0, 0],
		[sin(phi), cos(phi), 0, 0],
		[0, 0, 1, 0],
		[0, 0, 0, 1]
	])
	for i, p in enumerate(params):
		t = t.dot(rot(*p))
	return t


def test_t_r():
	# works for Crane's Book, p 41
	ans = np.array([24.11197183, 20.11256511, 18.16670832, 1.])
	params = [
		# a_ij alpha_ij  S_j  theta_j
		[0,    d2r(90),  5.9, 5*pi/6],  # frame 12
		[17,    d2r(0),    0,  -pi/3],  # 23
		[0.8, d2r(270),   17,   pi/4],  # 34
		[0,    d2r(90),    0,   pi/3],  # 45
		[0,    d2r(90),    4,  -pi/6]   # 56
	]

	r = T(params, 5*pi/4)
	# print(r)
	pos = r.dot(np.array([5, 3, 7, 1]))
	res = np.linalg.norm(ans - pos)
	# print('res:', res)
	assert(res < 0.000001)


# def test2():
# 	Lc = 10.0
# 	Lf = 43.0
# 	Lt = 63.0
# 	phi = 45
# 	theta2 = 0
# 	theta3 = -90
# 	params = [
# 		# a_ij alpha_ij  S_j  theta_j
# 		[Lc,   d2r(90),   0,   d2r(theta2)],  # frame 12
# 		[Lf,    d2r(0),   0,   d2r(theta3)]   # 23
# 	]
# 	r = T(params, d2r(phi))
# 	foot = r.dot(np.array([Lt, 0, 0, 1]))  # ok [ 37.4766594  37.4766594 -63. 1.]
# 	# print(r)
# 	print('foot loc:', foot)  # ok [ 37.4766594  37.4766594 -63. 1.]
#
# 	d = foot - np.array([37.4766594, 37.4766594, -63., 1.])
# 	diff = np.inner(d, d)
# 	print('diff:', diff)




if __name__ == "__main__":
	testt_t_r()
