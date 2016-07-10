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
import time

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
		# self.footPosition = [0.0, 0.0, 0.0]
		# self.angles = [0.0, 0.0, 0.0]

		self.coxaLength = lengths['coxaLength']
		self.tibiaLength = lengths['tibiaLength']
		self.femurLength = lengths['femurLength']

		# initAngles = [-45, -20, -110]
		initAngles = [45, 0, 0]


		self.foot0 = self.fk(*initAngles)

		# Create each servo and move it to the initial position
		# servo arrange: coxa femur tibia
		for i in range(0, 3):
			# print('leg channels', channels)
			if limits: lim = limits[i]
			else: lim = None
			self.servos.append(Servo(channels[i], lim))
			self.servos[i].angle = initAngles[i]
			print('servo {} angle {}'.format(channels[i], initAngles[i]))
			# time.sleep(1)

		# self.servos[0].all_stop()

	def __del__(self):
		self.servos[0].all_stop()

	def fk(self, a, b, g):
		"""
		angle are all degrees
		"""
		Lc = self.coxaLength
		Lf = self.femurLength
		Lt = self.tibiaLength

		phi = a
		theta2 = b
		theta3 = g - 90.0  # fix tibia servo range

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
		and returns the joint angles[degrees]
		"""
		Lc = self.coxaLength
		Lf = self.femurLength
		Lt = self.tibiaLength
		a = atan2(y, x)  # <---
		# a = atan2(x, y)
		f = sqrt(x**2 + y**2) - Lc
		b1 = atan2(z, f)  # <---
		# b1 = atan2(f, z)
		d = sqrt(f**2 + z**2)  # <---
		b2 = acos((Lf**2 + d**2 - Lt**2) / (2.0 * Lf * d))
		b = b1 + b2
		g = acos((Lf**2 + Lt**2 - d**2) / (2.0 * Lf * Lt))

		#### FIXES ###################################
		g -= pi  # fix to align fk and ik frames
		g += pi/2.0  # fix tiba servo range
		##############################################

		# print('ik angles: {:.2f} {:.2f} {:.2f}'.format(r2d(a), r2d(b), r2d(g)))

		# return a, b, g  # coxaAngle, femurAngle, tibiaAngle
		return r2d(a), r2d(b), r2d(g)  # coxaAngle, femurAngle, tibiaAngle

	def move(self, x, y, z):
		"""
		Attempts to move it's foot to coordinates [x,y,z]
		"""
		try:
			a,b,c = self.ik(x, y, z)  # inverse kinematics
			angles = [a,b,c]
			# print('servos:', len(self.servos))
			# angles[0] *= -1
			angles[2] *= -1
			print('angles: {:.2f} {:.2f} {:.2f}'.format(*angles))
			for i, servo in enumerate(self.servos):
				# print('i, servo:', i, servo)
				# angle = angles[i]
				# if i == 2: angle += 90.0  # correct for tibia servo
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
	leg = Leg(length, channels)

	angles = [45, 0, 0]  # 0 is 45 angled from body

	pts = leg.fk(*angles)
	angles2 = leg.ik(*pts)
	pts2 = leg.fk(*angles2)
	# angles2 = [r2d(a), r2d(b), r2d(c)]
	print('angles (orig):', angles)
	print('pts from fk(orig): {:.2f} {:.2f} {:.2f}'.format(*pts))
	print('angles2 from ik(pts): {:.2f} {:.2f} {:.2f}'.format(*angles2))
	print('pts2 from fk(angle2): {:.2f} {:.2f} {:.2f}'.format(*pts2))
	# print('diff:', np.linalg.norm(np.array(angles) - np.array(angles2)))
	print('diff [mm]: {:.2f}'.format(np.linalg.norm(pts - pts2)))
	time.sleep(1)
	# assert(np.linalg.norm(np.array(angles) - np.array(angles2)) < 0.00001)

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


def check_range():
	length = {
		'coxaLength': 17,
		'femurLength': 45,
		'tibiaLength': 63
	}

	channels = [0, 1, 2]
	# limits = [[-45, 45], [-45, 45], [-90, 0]]

	leg = Leg(length, channels)
	time.sleep(1)
	for servo in range(0, 3):
		leg.servos[0].angle = -45; time.sleep(0.01)
		leg.servos[1].angle = -20; time.sleep(0.01)
		leg.servos[2].angle = -110; time.sleep(0.01)
		for angle in range(-45, 45, 20):
			if servo == 2: angle -= 90
			print('servo: {} angle: {}'.format(servo, angle))
			leg.servos[servo].angle = angle
			time.sleep(1)


if __name__ == "__main__":
	test_fk_ik()
	# check_range()
