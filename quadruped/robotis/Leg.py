#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import numpy as np
from math import sin, cos, acos, atan2, sqrt, pi, fabs
from math import radians as d2r
from math import degrees as r2d
# from kinematics import T
import logging
from Servo import Servo

# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.ERROR)

"""
 \      /           ^ y
  \    /            |
   ----             |
  |    |     <------+
   ----      x
  /    \
 /      \

+x forward
-x reverse


  /\     /\
 /  -----  \
/           \

"""

class Leg(object):
	"""
	"""
	def __init__(self, lengths, channels, ser, limits, offsets):
		"""
		Each leg has 3 servos/channels
		"""
		if not len(channels) == 3:
			raise Exception('len(channels) != 3')

		self.servos = []

		self.coxaLength = lengths['coxaLength']
		self.tibiaLength = lengths['tibiaLength']
		self.femurLength = lengths['femurLength']

		# Create each servo and move it to the initial position
		# servo arrange: coxa femur tibia
		for i in range(0, 3):
			self.servos.append(Servo(channels[i], ser))
			# self.servos[i].offset = offsets[i]
			self.servos[i].setServoLimits(offsets[i], *limits[i])

		initAngles = [0, 45, -90-45]
		self.foot0 = self.fk(*initAngles)

	def __del__(self):
		pass

	def fk(self, a, b, g):
		"""
		angle are all degrees
		"""
		Lc = self.coxaLength
		Lf = self.femurLength
		Lt = self.tibiaLength

		# if 0:
		# 	phi = a
		# 	theta2 = b
		# 	theta3 = g
		#
		# 	params = [
		# 		# a_ij alpha_ij  S_j  theta_j
		# 		[Lc,   d2r(90.0),   0.0,   d2r(theta2)],  # frame 12
		# 		[Lf,   d2r(0.0),    0.0,   d2r(theta3)]   # frame 23
		# 	]
		#
		# 	r = T(params, d2r(phi))
		# 	foot = r.dot(np.array([Lt, 0.0, 0.0, 1.0]))
		#
		# 	return foot[0:-1]  # DH return vector size 4, only grab (x,y,z) which are the 1st 3 elements
		# else:
		a = d2r(a)
		b = d2r(b)
		g = d2r(g)
		# foot = [
		# 	Lc*cos(a) + Lf*cos(a)*cos(b) + Lt*(-sin(b)*sin(g)*cos(a) + cos(a)*cos(b)*cos(g)),
		# 	Lc*sin(a) + Lf*sin(a)*cos(b) + Lt*(-sin(a)*sin(b)*sin(g) + sin(a)*cos(b)*cos(g)),
		# 	Lf*sin(b) + Lt*(sin(b)*cos(g) + sin(g)*cos(b))
		# ]

		foot = [
			(Lc + Lf*cos(b) + Lt*cos(b + g))*cos(a),
			(Lc + Lf*cos(b) + Lt*cos(b + g))*sin(a),
			Lf*sin(b) + Lt*sin(b + g)
		]

		return np.array(foot)

	def ik(self, x, y, z):
		"""
		Calculates the inverse kinematics from a given foot coordinate (x,y,z)[mm]
		and returns the joint angles[degrees]

		Reference (there are typos)
		https://tote.readthedocs.io/en/latest/ik.html
		"""
		# try:
		Lc = self.coxaLength
		Lf = self.femurLength
		Lt = self.tibiaLength

		if sqrt(x**2 + y**2) < Lc:
			print('too short')
			return None
		# elif z > 0.0:
		# 	return None

		a = atan2(y, x)
		f = sqrt(x**2 + y**2) - Lc
		# b1 = atan2(z, f)  # takes into account quadrent, z is neg

		# you have different conditions depending if z is pos or neg
		if z < 0.0:
			b1 = atan2(f, fabs(z))
		else:
			b1 = atan2(z, f)

		d = sqrt(f**2 + z**2)  # <---

		# print('pos: {} {} {}'.format(x,y,z))
		# print('d: {:.3f}  f: {:.3f}'.format(d,f))
		# print('Lc Lf Lt: {} {} {}'.format(Lc,Lf,Lt))
		# print('num: {:.3f}'.format(Lf**2 + d**2 - Lt**2))
		# print('den: {:.3f}'.format(2.0 * Lf * d))
		# print('acos: {:.2f}'.format((Lf**2 + d**2 - Lt**2) / (2.0 * Lf * d)))

		guts = ((Lf**2 + d**2 - Lt**2) / (2.0 * Lf * d))
		if 1.0 < guts or guts < -1.0:
			print('acos crap!: {:.3f} {:.3f} {:.3f}'.format(x,y,z))
			return None
		b2 = acos((Lf**2 + d**2 - Lt**2) / (2.0 * Lf * d))  # issues?
		b = b1 + b2
		g = acos((Lf**2 + Lt**2 - d**2) / (2.0 * Lf * Lt))

		#### FIXES ###################################
		g -= pi  # fix to align fk and ik frames

		if z < 0.0:
			b -= pi/2  #
		##############################################
		# print('b1 b2: {:.2f} {:.2f}'.format(r2d(b1), r2d(b2)))
		# print('ik angles: {:.2f} {:.2f} {:.2f}'.format(r2d(a), r2d(b), r2d(g)))
		return r2d(a), r2d(b), r2d(g)  # coxaAngle, femurAngle, tibiaAngle

		# except Exception as e:
		# 	print('ik error:', e)
		# 	raise e

	# def ik2(self, x, y, z):
	# 	"""
	# 	Calculates the inverse kinematics from a given foot coordinate (x,y,z)[mm]
	# 	and returns the joint angles[degrees]
	#
	# 	Reference (there are typos)
	# 	https://tote.readthedocs.io/en/latest/ik.html
	# 	"""
	# 	# try:
	# 	Lc = self.coxaLength
	# 	Lf = self.femurLength
	# 	Lt = self.tibiaLength
	# 	a = atan2(y, x)
	# 	L1 = sqrt(x**2+y**2)
	# 	L = sqrt(z**2 + (L1-Lc)**2)
	# 	b1 = acos(z/L)
	# 	b2 = acos((Lt**2 - Lf**2 - L**2) / (-2.0 * Lf * L))  # issues?
	# 	b = b1 + b2
	# 	g = acos((Lf**2 + Lt**2 - L**2) / (2.0 * Lf * Lt))
	#
	# 	#### FIXES ###################################
	# 	g -= pi  # fix to align fk and ik frames
	# 	b -= pi/2  # wtf ... i need this!!!!
	# 	##############################################
	# 	# print('b1 b2: {:.2f} {:.2f}'.format(r2d(b1), r2d(b2)))
	# 	# print('ik angles: {:.2f} {:.2f} {:.2f}'.format(r2d(a), r2d(b), r2d(g)))
	# 	return r2d(a), r2d(b), r2d(g)  # coxaAngle, femurAngle, tibiaAngle

	def move(self, x, y, z):
		"""
		Attempts to move it's foot to coordinates [x,y,z]
		"""
		try:
			# a, b, c = self.ik(x, y, z)  # inverse kinematics
			# angles = [a, b, c]
			angles = self.ik(x, y, z)  # inverse kinematics
			if angles is None:
				return
			# print('angles: {:.2f} {:.2f} {:.2f}'.format(*angles))
			for i, servo in enumerate(self.servos):
				# print('i, servo:', i, servo)
				angle = angles[i]
				# print('servo {} angle {}'.format(i, angle))
				servo.angle = angle

		except Exception as e:
			print (e)
			raise

	def reset(self):
		# self.angles = self.resting_position
		self.move(*self.foot0)


if __name__ == "__main__":
	print('Hello cowboy!')
