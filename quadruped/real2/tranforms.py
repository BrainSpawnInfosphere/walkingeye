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
# from math import degrees as r2d

"""
This file is needed by gait Trot class
"""

# FIXME: 20160625 add euler -> quaternion transform and reverse

def axis_angle(vec, axis, theta):
	"""
	https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation#Conversion_to_and_from_the_matrix_representation
	Quaternion (axis/angle) to rotation matrix

	in:
		vec - point to rotate
		axis - axis of rotation
		theta - angle of rotation (degrees)
	out: rotated vector/point
	"""
	theta = d2r(theta)
	axis = np.array([0, 0, 1])
	# axis = axis / sqrt(np.dot(axis, axis))  # normalizing axis
	a = cos(theta / 2.0)
	b, c, d = axis * sin(theta / 2.0)
	aa, bb, cc, dd = a * a, b * b, c * c, d * d
	bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
	rot = np.array([
		[aa+bb-cc-dd, 2.0*(bc-ad), 2.0*(bd+ac)],
		[2.0*(bc+ad), aa-bb+cc-dd, 2.0*(cd-ab)],
		[2.0*(bd-ac), 2.0*(cd+ab), aa-bb-cc+dd]
	])
	# print('rotateAroundCenter', np.dot(rot, vec))

	return np.dot(rot, vec)


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


def test_t():
	R = rot(0.0, 0.0, 0.0, 0.0)  # should be eye(4,4)
	a = np.array([1., 2., 3., 1.])
	b = np.dot(R, a)
	# print(R)
	# print(a,b)
	assert(np.linalg.norm(a-b) == 0.0)


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


if __name__ == "__main__":
	# test_t_r()
	test_t()
