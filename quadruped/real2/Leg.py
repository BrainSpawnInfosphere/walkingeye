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
		if not len(channels) == 3: raise Exception('len(channels) != 3')

		self.servos = []
		# self.footPosition = [0.0, 0.0, 0.0]
		# self.angles = [0.0, 0.0, 0.0]

		self.coxaLength = lengths['coxaLength']
		self.tibiaLength = lengths['tibiaLength']
		self.femurLength = lengths['femurLength']

		# Create each servo and move it to the initial position
		# servo arrange: coxa femur tibia
		for i in range(0, 3):
			# print('leg channels', channels)
			if limits: lim = limits[i]
			else: lim = None
			self.servos.append(Servo(channels[i], lim))
			# self.servos[i].angle = initAngles[i]
			# print('servo {} angle {}'.format(channels[i], initAngles[i]))
			# time.sleep(1)

		# initAngles = [-45, -20, -110]
		initAngles = [0, 0, -90]
		self.foot0 = self.fk(*initAngles)
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

		if 0:
			phi = a
			theta2 = b
			theta3 = g

			params = [
				# a_ij alpha_ij  S_j  theta_j
				[Lc,   d2r(90.0),   0.0,   d2r(theta2)],  # frame 12
				[Lf,    d2r(0.0),   0.0,   d2r(theta3)]   # frame 23
			]

			r = T(params, d2r(phi))
			foot = r.dot(np.array([Lt, 0.0, 0.0, 1.0]))

			return foot[0:-1]  # DH return vector size 4, only grab (x,y,z) which are the 1st 3 elements
		else:
			a = d2r(a)
			b = d2r(b)
			g = d2r(g)
			foot = [
				Lc*cos(a) + Lf*cos(a)*cos(b) + Lt*(-sin(b)*sin(g)*cos(a) + cos(a)*cos(b)*cos(g)),
				Lc*sin(a) + Lf*sin(a)*cos(b) + Lt*(-sin(a)*sin(b)*sin(g) + sin(a)*cos(b)*cos(g)),
				Lf*sin(b) + Lt*(sin(b)*cos(g) + sin(g)*cos(b))
			]

			return np.array(foot)

	def ik(self, x, y, z):
		"""
		Calculates the inverse kinematics from a given foot coordinate (x,y,z)[mm]
		and returns the joint angles[degrees]

		Reference (there are typos)
		https://tote.readthedocs.io/en/latest/ik.html
		"""
		try:
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
			##############################################

			# print('ik angles: {:.2f} {:.2f} {:.2f}'.format(r2d(a), r2d(b), r2d(g)))

			# return a, b, g  # coxaAngle, femurAngle, tibiaAngle
			return r2d(a), r2d(b), r2d(g)  # coxaAngle, femurAngle, tibiaAngle
		except Exception as e:
			print('ik error:', e)
			raise e

	def move(self, x, y, z):
		"""
		Attempts to move it's foot to coordinates [x,y,z]
		"""
		try:
			a, b, c = self.ik(x, y, z)  # inverse kinematics
			angles = [a, b, c]
			# print('angles: {:.2f} {:.2f} {:.2f}'.format(*angles))
			for i, servo in enumerate(self.servos):
				# print('i, servo:', i, servo)
				angle = angles[i]
				if i == 2: angle = -1*angle - 180   # correct for tibia servo backwards
				# print('servo {} angle {}'.format(i, angle))
				servo.angle = angle

		except Exception as e:
			print (e)
			raise

	def reset(self):
		self.angles = self.resting_position

################################################################


def test_fk_ik():
	length = {
		'coxaLength': 26,
		'femurLength': 42,
		'tibiaLength': 63
	}
	channels = [0, 1, 2]
	leg = Leg(length, channels)

	angles = [0, -70, -90]

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


def printError(pts, pts2, angles, angles2):
	print('angles (orig):', angles)
	print('angles2 from ik(pts): {:.2f} {:.2f} {:.2f}'.format(*angles2))
	print('pts from fk(orig): {:.2f} {:.2f} {:.2f}'.format(*pts))
	print('pts2 from fk(angle2): {:.2f} {:.2f} {:.2f}'.format(*pts2))
	# print('diff:', np.linalg.norm(np.array(angles) - np.array(angles2)))
	print('diff [mm]: {:.2f}'.format(np.linalg.norm(pts - pts2)))


def test_full_fk_ik(c=[0, 1, 2]):
	length = {
		'coxaLength': 26,
		'femurLength': 42,
		'tibiaLength': 63
	}
	channels = c
	leg = Leg(length, channels)

	servorange = [[-90, 90], [-90, 90], [-180, 0]]
	for s in range(0, 3):
		leg.servos[s].setServoRangeAngle(*servorange[s])

	for i in range(1, 3):
		for a in range(-70, 70, 10):
			angles = [0, 0, -10]
			if i == 2: a -= 90
			angles[i] = a
			pts = leg.fk(*angles)
			angles2 = leg.ik(*pts)
			pts2 = leg.fk(*angles2)

			angle_error = np.linalg.norm(np.array(angles) - np.array(angles2))
			pos_error = np.linalg.norm(pts - pts2)
			# print(angle_error, pos_error)

			if angle_error > 0.0001:
				print('Angle Error')
				printError(pts, pts2, angles, angles2)
				exit()

			elif pos_error > 0.0001:
				print('Position Error')
				printError(pts, pts2, angles, angles2)
				exit()

			else:
				print('Good: {} {} {}  error(deg,mm): {} {}'.format(angles[0], angles[1], angles[2], angle_error, pos_error))
				leg.move(*pts)
				time.sleep(0.1)

	Servo.all_stop()


def check_range():
	length = {
		'coxaLength': 26,
		'femurLength': 42,
		'tibiaLength': 63
	}

	channels = [0, 1, 2]
	# limits = [[-45, 45], [-45, 45], [-90, 0]]

	leg = Leg(length, channels)
	time.sleep(1)
	for servo in range(0, 3):
		leg.servos[0].angle = 45; time.sleep(0.01)
		leg.servos[1].angle = 0; time.sleep(0.01)
		leg.servos[2].angle = -90; time.sleep(0.01)
		for angle in range(-45, 45, 20):
			# if servo == 2: angle -= 90
			print('servo: {} angle: {}'.format(servo, angle))
			leg.servos[servo].angle = angle
			time.sleep(1)


if __name__ == "__main__":
	# test_fk_ik()
	# test_full_fk_ik([0,1,2])
	# test_full_fk_ik([4,5,6])
	test_full_fk_ik([8,9,10])
	# test_full_fk_ik([12,13,14])
	# check_range()
