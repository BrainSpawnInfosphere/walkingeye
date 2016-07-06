#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import numpy as np
from math import sin, cos, acos, atan2, sqrt, pi
from math import radians as d2r
from math import degrees as r2d
from tranforms import rot, T


class Leg(object):
	"""
	This should be an abstract leg, it's responsible for moving and locating each leg.
	"""

	position = None  # leg refence frame loc in body reference frame
	# orientation = None  # might be useful
	ydirection = 1
	footPosition = [0.0, 0.0, 0.0]
	angles = [0.0, 0.0, 0.0]

	def __init__(self, name, position, lengths):
		"""
		:param name: leg name, used to get it's pointing difection in some implementations
		:param position: body-relative leg position
		:param resting_position: feet resting position
		lengths: lengths of leg segments
		:return:
		"""
		self.name = name
		self.position = position
		# self.resting_position = resting_position
		self.coxaLength = lengths['coxaLength']
		self.tibiaLength = lengths['tibiaLength']
		self.femurLength = lengths['femurLength']
		# self.angles = self.ik_to(*resting_position)

		if "right" in self.name:
			self.ydirection = -1

	def set_resting_pos(self, a, b, c):
		self.angles = np.array([a, b, c])
		self.resting_position = self.fk_to(a, b, c)

	def fk_to(self, a, b, g):
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

		return foot

	def ik_to(self, x, y, z):
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

		return a, b, g  # coxaAngle, femurAngle, tibiaAngle

	# change def setFoot(self, x, y, z):
	def move_to_pos(self, x, y, z):
		"""
		Attempts to move it's foot to coordinates [x,y,z]
		"""
		try:
			angles = self.ik_to(x, y, z)  # inverse kinematics
			self.footPosition = np.array([x, y, z])
			self.angles = angles
		except Exception as e:
			print (e)
			raise

	def reset(self):
		self.angles = self.resting_position
