#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import numpy as np
from math import sin, cos, acos, atan2, sqrt, pi
from math import radians as d2r
from math import degrees as r2d
from tranforms import rot, T
# from Interfaces import PCA9685
import logging
from Servo import Servo
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.ERROR)


class Leg(object):
	"""
	"""

	def __init__(self, lengths, channels, limits=None):
		"""
		"""
		if not len(channels) == 3: raise Exception('len(channels) = 3')

		self.servos = []
		self.footPosition = [0.0, 0.0, 0.0]
		self.angles = [0.0, 0.0, 0.0]

		self.coxaLength = lengths['coxaLength']
		self.tibiaLength = lengths['tibiaLength']
		self.femurLength = lengths['femurLength']

		self.foot0 = self.fk(0, 0, -90)

		# Create each servo and move it to the initial position
		# servo arrange: coxa femur tibia
		for i in range(0, 3):
			# print('leg channels', channels)
			if limits: lim = limits[i]
			else: lim = None
			self.servos.append(Servo(channels[i], lim))
			self.servos[i].angle = self.foot0[i]

	def __del__(self):
		self.servos[0].all_stop()

	def fk(self, a, b, g):
		"""
		"""
		Lc = self.coxaLength
		Lf = self.femurLength
		Lt = self.tibiaLength

		phi = a
		theta2 = b
		theta3 = g

		params = [
			# a_ij alpha_ij  S_j  theta_j
			[Lc,   d2r(90),   0,   d2r(theta2)],  # frame 12
			[Lf,    d2r(0),   0,   d2r(theta3)]   # 23
		]

		r = T(params, d2r(phi))
		foot = r.dot(np.array([Lt, 0, 0, 1]))  # ok [ 37.4766594  37.4766594 -63. 1.]

		return foot[0:-1]  # DH return vector size 4, only grabe first 3 (x,y,z)

	def ik(self, x, y, z):
		"""
		Calculates the inverse kinematics from a given foot coordinate (x,y,z)[mm]
		and returns the joint angles
		"""
		Lc = self.coxaLength
		Lf = self.femurLength
		Lt = self.tibiaLength
		a = atan2(y, x)
		f = sqrt(x**2 + y**2) - Lc
		b1 = atan2(z, f)
		d = sqrt(f**2 + z**2)
		b2 = acos((Lf**2 + d**2 - Lt**2) / (2.0 * Lf * d))
		b = b1 + b2
		g = acos((Lf**2 + Lt**2 - d**2) / (2.0 * Lf * Lt))

		g -= pi  # fix to align fk and ik

		print('ik angles:', r2d(a), r2d(b), r2d(g))

		# return a, b, g  # coxaAngle, femurAngle, tibiaAngle
		return r2d(a), r2d(b), -r2d(g)  # coxaAngle, femurAngle, tibiaAngle

	def move(self, x, y, z):
		"""
		Attempts to move it's foot to coordinates [x,y,z]
		"""
		try:
			angles = self.ik(x, y, z)  # inverse kinematics
			# print('move:', angles)
			# print('servos:', len(self.servos))
			for i, servo in enumerate(self.servos):
				# print('i, servo:', i, servo)
				servo.angle = angles[i]

		except Exception as e:
			print (e)
			raise

	def reset(self):
		self.angles = self.resting_position

################################################################


def test_fk_ik():
	length = {
		'coxaLength': 10,
		'tibiaLength': 43,
		'femurLength': 63
	}

	channels = [0, 1, 2]
	limits = [[-45, 45], [-45, 45], [-90, 0]]

	leg = Leg(length, channels, limits)
	angles = [-45, -10, 0]
	print('angles:', angles)
	pts = leg.fk(*angles)
	print('pts:', pts)
	a, b, c = leg.ik(*pts)
	angles2 = [r2d(a), r2d(b), r2d(c)]
	print('angles2:', angles2)
	print('diff:', np.linalg.norm(np.array(angles) - np.array(angles2)))
	assert(np.linalg.norm(np.array(angles) - np.array(angles2)) < 0.00001)

	# Lc = 10.0
	# Lf = 43.0
	# Lt = 63.0
	# phi = -45
	# theta2 = -10
	# theta3 = 0
	#
	# print('input angles:', phi, theta2, theta3)
	#
	# params = [
	# 	# a_ij alpha_ij  S_j  theta_j
	# 	[Lc,   d2r(90),   0,   d2r(theta2)],  # frame 12
	# 	[Lf,    d2r(0),   0,   d2r(theta3)]   # 23
	# ]
	# r = T(params, d2r(phi))
	# foot = r.dot(np.array([Lt, 0, 0, 1]))  # ok [ 37.4766594  37.4766594 -63. 1.]
	# # print(r)
	# print('foot loc:', foot)  # ok [ 37.4766594  37.4766594 -63. 1.]
	#
	# a, b, g = ik_to(foot[0], foot[1], foot[2], Lc, Lf, Lt)
	# print('ik angles:', r2d(a), r2d(b), r2d(g))


################################################################


if __name__ == "__main__":
	test_fk_ik()
