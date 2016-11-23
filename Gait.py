#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import numpy as np
# import logging
from math import cos, sin, sqrt, pi
from math import radians as d2r

# make a static method in Gait? Nothing else uses it
def rot_z(t, c):
	"""
	t - theta [radians]
	c - [x,y,z] or [x,y] ... the function detects 2D or 3D vector
	"""
	if len(c) == 3:
		ans = np.array([
			c[0]*cos(t)-c[1]*sin(t),
			c[0]*sin(t)+c[1]*cos(t),
			c[2]
		])
	else:
		ans = np.array([
			c[0]*cos(t)-c[1]*sin(t),
			c[0]*sin(t)+c[1]*cos(t)
		])

	return ans


class Gait(object):
	"""
	Base class for gaits
	"""
	def __init__(self):
		# for a step pattern of 12, these are the offsets of each leg
		self.legOffset = [0, 6, 3, 9]
		# frame rotations for each leg
		self.frame = [pi/4, -pi/4, -3*pi/4, 3*pi/4]
		# the resting or idle position/orientation of a leg
		self.rest = None

	def calcRotatedOffset(self, cmd, i):
		"""
		calculate the foot offsets for each leg and delta linear/rotational
		in - cmd(x,y,z_rotation)
		out - array(leg0, leg1, ...)
			where leg0 = {'linear': [x,y], 'rotational': [x,y], 'angle': zrotation(rads)}
		"""
		# rotate the command into the leg frame
		frame_angle = self.frame[i]
		rc = rot_z(frame_angle, cmd)

		# get rotation distance: dist = rot_z(angle, rest) - rest
		# this just reduces the function calls and math
		zrot = d2r(float(cmd[2]))  # should I assume this is always radians? save conversion

		# fromcenter = self.rest + self.body

		# value of this?
		#  rot = rot_z(zrot/2, fromcenter) - rot_z(-zrot/2, fromcenter)

		#  ans = {'linear': rc, 'rotational': rot, 'angle': zrot}
		ans = {'linear': rc, 'angle': zrot}  # FIXME: 20161119, make a tuple?

		return ans

	def command(self, cmd, moveFoot, bulkWrite, steps=12):
		"""
		func is the quadruped move foot function for a specific leg
		"""
		# handle no movement command ... do else where?
		if sqrt(cmd[0]**2 + cmd[1]**2 + cmd[2]**2) < 0.001:
			for leg in range(0, 4):
				moveFoot(leg, self.rest)  # move to resting position
			bulkWrite()
			return

		# cmd = [100.0, 0.0, 0.0]

		# frame rotations for each leg
		# frame = [-pi/4, pi/4, 3*pi/4, -3*pi/4]

		for i in range(0, steps):  # iteration, there are 12 steps in gait cycle
			for legNum in [0, 2, 1, 3]:  # order them diagonally
				rcmd = self.calcRotatedOffset(cmd, legNum)
				pos = self.eachLeg(i, rcmd)  # move each leg appropriately
				# if legNum == 0: print('New  [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, pos[0], pos[1], pos[2]))
				moveFoot(legNum, pos)
			bulkWrite()


class DiscreteRippleGait(Gait):
	def __init__(self, h, r):
		Gait.__init__(self)
		self.phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]  # foot pos in gait sequence
		maxl = h  # lifting higher gives me errors
		minl = maxl/2
		self.z = [minl, maxl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # leg height
		self.rest = r  # idle leg position

	def eachLeg(self, index, cmd):
		"""
		interpolates the foot position of each leg
		cmd:
			linear (mm)
			angle (rads)
		"""
		rest = self.rest
		i = index % 12
		phi = self.phi[i]

		# rotational commands -----------------------------------------------
		angle = cmd['angle']/2-cmd['angle']*phi
		rest_rot = rot_z(-angle, rest)
		# rest_rot[2] = 0  # let linear handle z height

		# linear commands ----------------------------------------------------
		linear = cmd['linear']
		xx = linear[0]
		yy = linear[1]

		# create new move command
		move = np.array([
			xx/2 - phi*xx,
			yy/2 - phi*yy,
			self.z[i]
		])

		# new foot position: newpos = rot + move ----------------------------
		newpos = move + rest_rot
		# print('New  [](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(newpos[0], newpos[1], newpos[2]))
		return newpos


class ContinousRippleGait(Gait):
	alpha = 1.0

	def __init__(self, h, r):
		Gait.__init__(self)
		self.height = h
		self.rest = r

	@staticmethod
	def phi(x):
		"""
		The phase
		"""
		phi = 0.0
		if x <= 3.0:
			phi = 1/3*(3.0-x)
		else:
			phi = 1/9*(x-3)
		return phi

	def z(self, x):
		"""
		Leg height

		duty cycle:
			0-3: leg lifted
			3-12: leg on ground
			duty = (12-3)/12 = 0.75 = 75% a walking gait
		"""
		height = self.height
		z = 0.0
		if x <= 1:
			z = height/1.0*x
		elif x <= 2.0:
			z = height
		elif x <= 3.0:
			z = -height/1.0*(x-2.0)+height
		return z

	def eachLeg(self, index, cmd):
		"""
		interpolates the foot position of each leg
		"""
		rest = self.rest
		i = (index*self.alpha) % 12
		phi = self.phi(i)
		z = self.z(i)

		# rotational commands -----------------------------------------------
		angle = cmd['angle']/2-cmd['angle']*phi
		rest_rot = rot_z(-angle, rest)
		# rest_rot[2] = 0  # let linear handle z height

		# linear commands ----------------------------------------------------
		linear = cmd['linear']
		xx = linear[0]
		yy = linear[1]

		# create new move command
		move = np.array([
			xx/2 - phi*xx,
			yy/2 - phi*yy,
			z
		])

		# new foot position: newpos = rot + move ----------------------------
		newpos = move + rest_rot
		return newpos
