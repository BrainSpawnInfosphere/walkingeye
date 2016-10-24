#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import numpy as np
from math import sin, cos
from math import radians as d2r

"""
This file is needed by gait Trot class
"""

# FIXME: 20160625 add euler -> quaternion transform and reverse
# FIXME 2016-10-09 look at using pip's quaternion package

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


# def rot(a, alpha, S, theta):
# 	"""
# 	Creates a DH rotation matrix for forward kinematics.
# 	"""
# 	return np.array([  # eqn 3.7 pg 36
# 		[cos(theta), -sin(theta), 0, a],
# 		[sin(theta) * cos(alpha), cos(theta) * cos(alpha), -sin(alpha), -sin(alpha) * S],
# 		[sin(theta) * sin(alpha), cos(theta) * sin(alpha), cos(alpha), cos(alpha) * S],
# 		[0, 0, 0, 1]
# 	])
#
# 	# return np.array([  # inverse of above ??
# 	# 	[cos(theta), sin(theta) * cos(alpha), sin(theta) * sin(alpha), -cos(theta) * a],
# 	# 	[-sin(theta), cos(theta) * cos(alpha), cos(theta) * sin(alpha), sin(theta) * a],
# 	# 	[0, -sin(alpha), cos(alpha), -S],
# 	# 	[0, 0, 0, 1]
# 	# ])
#
#
# def T(params, phi):
# 	"""
# 	T -> dh ??
#
# 	Creates a transform from the leg frame to the foot.
#
# 	params = [[a, alpha, S, theta],[a, alpha, S, theta],...]
# 	"""
# 	# handle the base frame, eqn 3.9, p36
# 	t = np.array([
# 		[cos(phi), -sin(phi), 0, 0],
# 		[sin(phi), cos(phi), 0, 0],
# 		[0, 0, 1, 0],
# 		[0, 0, 0, 1]
# 	])
# 	for i, p in enumerate(params):
# 		t = t.dot(rot(*p))
# 	return t

class DH(object):
	def __init__(self):
		pass

	def fk(self, params):
		t = np.eye(4)
		for p in params:
			t = t.dot(self.makeT(*p))
		return t

	def makeT(self, a, alpha, d, theta):
		alpha = d2r(alpha)
		theta = d2r(theta)
		return np.array([  # classic DH
			[cos(theta), -sin(theta) * cos(alpha),  sin(theta) * sin(alpha), cos(theta) * a],
			[sin(theta),  cos(theta) * cos(alpha), -cos(theta) * sin(alpha), sin(theta) * a],
			[0, sin(alpha), cos(alpha), d],
			[0, 0, 0, 1]
		])


if __name__ == "__main__":
	pass
