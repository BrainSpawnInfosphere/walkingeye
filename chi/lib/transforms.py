#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
from math import cos, sin, atan2, asin, sqrt, pi
from math import radians as d2r
from math import degrees as r2d
import numpy as np


class ChiMathError(Exception):
	pass


def axis_angle(vec, axis, theta):
	"""
	https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation#Conversion_to_and_from_the_matrix_representation
	https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
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


def euler2Quaternion():
	"""
	tbd
	"""
	pass


def quaternion2Euler(w, x, y, z):
	"""
	Convert quaterion (w,x,y,z) into a euler angle (r,p,y)

	https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
	"""
	roll = atan2(2.0*(w*x+y*z), 1.0-2.0*(x**2+y**2))
	pitch = asin(2.0*(w*y-z*x))
	yaw = atan2(2.0*(w*z+x*y), 1.0-2.0*(y**2+z**2))
	# print('r {:.2f} p {:.2f} y {:.2f}'.format(r2d(roll), r2d(pitch), r2d(yaw)))
	return roll, pitch, yaw


def aa2Quaternion(axis, angle):
	"""
	Axis/angle to quaternion
	"""
	w = cos(angle/2)
	s = sin(angle/2)

	# normalize if necessary
	d = 0.0001
	m = sqrt(axis[0]**2 + axis[1]**2 + axis[2]**2)
	if m > (1.0 + d) or m < (1.0-d):
		if m > 0.0:
			for i in range(0, 3):
				axis[i] /= m
		else:
			raise ChiMathError('aa2Quaternion: div by 0')

	x = axis[0]*s
	y = axis[1]*s
	z = axis[2]*s

	return w, x, y, z


def main():
	w, x, y, z = aa2Quaternion([1,0,0], pi)
	print(w,x,y,z)
	r, p, y = quaternion2Euler(w,x,y,z)
	print(r,p,y)


if __name__ == '__main__':
	main()
