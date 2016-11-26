#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import numpy as np
from numpy.linalg import norm
# import logging
from math import cos, sin, sqrt, pi
# from math import radians as d2r
from Servo import Servo
import time



class Correction(object):
	# cmrot
	leg2body = [pi/4, -pi/4, -3*pi/4, 3*pi/4]  # legs to body frame

	# frame
	cmd2leg = [-pi/4, pi/4, 3*pi/4, -3*pi/4]  # cmds to leg frame

	def __init__(self):
		# account for base, in base frame
		cm = 45*cos(pi/4)
		self.base = [
			np.array([cm, cm, 0]),
			np.array([cm, -cm, 0]),
			np.array([-cm, -cm, 0]),
			np.array([-cm, cm, 0])
		]

	def checkStable(self, feet):
		"""
		Check CM (located at [0,0]) is inside the triangle formed by the feet.
		in:
			feet = [[index, legNum, foot], ...] there are 3 of these
		out:
			True - CM is inside
			False - CM is outside
		"""
		pass

	def calcCorrection(self, feet, moveFoot):
		"""
		in:
			feet = [[index, legNum, foot], ...] there are 3 of these
					index - tells if foot is up/down
					legNum - which leg [0-3]
					foot - (x,y,z) is converted to 2D
		out:
			correction = [x,y,0] is only a 2D correction
		"""
		# hate this!!!
		temp = []  # [[x,y,z], [x,y,z], [x,y,z]] feet positions

		base = self.base

		for p in feet:  # p = [index, (x,y,z), legNum]
			index = p[0]
			legNum = p[1]
			foot = p[2]
			if index > 2:
				temp.append(rot_z(self.cmrot[legNum], foot) + base[legNum])
		# if len(temp) != 3:
		# 	print('fuck ... wrong points:', len(temp))

		correction = self.checkCM(temp)
		correction = np.array([0, 0, 0])
		print('correction: {:.2f} {:.2f} {:.2f}'.format(*correction))

		temp = []  # double check CM
		order = [0, 2, 1, 3]
		for i in range(0, 4):
			index = feet[i][0]
			legNum = order[i]
			n = feet[i][1]
			if index > 2:  # check index to see if leg moving
				n = n+rot_z(self.frame[legNum], correction)  # leg space
				# temp.append(rot_z(self.cmrot[footPos[i][2]], n)+base[footPos[i][2]])
				temp.append(rot_z(self.cmrot[feet[i][2]], n)+base[feet[i][2]])
				# print('index', footPos[legNum][0])
			moveFoot(legNum, n)

		for i in range(0, len(temp)):
			print('Foot[?]: {:.2f} {:.2f} {:.2f}'.format(*(temp[i])))

		# print('temp len:{}'.format(len(temp)))
		print('double check: {}'.format(inSideCM(temp, True)))



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


def inSideCM(pts, p=False):
	"""
	Determine if a point P is inside of a triangle composed of points
	A, B, and C.
	pts = [A,B,C]
	P = [0,0] at the center of mass of the robot
	returns True (inside triangle) or False (outside the triangle)
	"""
	# print('inSideCM pts:', pts)
	A = pts[0][0:2]
	B = pts[1][0:2]
	C = pts[2][0:2]
	P = np.array([0, 0])  # CM is at the center :)

	# Compute vectors
	v0 = C - A
	v1 = B - A
	v2 = P - A

	# Compute dot products
	dot00 = np.dot(v0, v0)
	dot01 = np.dot(v0, v1)
	dot02 = np.dot(v0, v2)
	dot11 = np.dot(v1, v1)
	dot12 = np.dot(v1, v2)

	# Compute barycentric coordinates
	invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
	u = (dot11 * dot02 - dot01 * dot12) * invDenom
	v = (dot00 * dot12 - dot01 * dot02) * invDenom

	if p:
		print(u, v)

	# Check if point is in triangle
	return (u >= 0) and (v >= 0) and (u + v < 1)


def lineIntersection(p1, p2, p3, p4):
	"""
	Find the intersection of 2 lines.
	line 1: p1, p2
	line 2: p3, p4
	"""
	x1 = p1[0]
	x2 = p2[0]
	x3 = p3[0]
	x4 = p4[0]
	y1 = p1[1]
	y2 = p2[1]
	y3 = p3[1]
	y4 = p4[1]

	denom = ((x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4))
	if abs(denom) < 0.00001:
		# print('crap {}'.format(denom))
		return np.array([0, 0])
	x = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4))/denom
	y = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4))/denom
	return np.array([x, y])


def vmin(a):
	"""
	Find the minimum vector in an array of 2D vectors.
	in = [[1,2], [2,3], ...]
	out = [1,2]
	"""
	minv = 0
	min_val = 1000000000000000
	for p in a:
		val = norm(p)
		if val < min_val:
			min_val = val
			minv = p
	return minv


def checkCM(pts):
	"""
	Given the robot's foot locations, provide correction if the
	center of mass (CM) is outside the triangle formed by the 3
	foot locations.
	pts = [foot0, foot1, foot2]
	correction = [x,y]
	"""
	# pts2 = []
	# for i in range(0, 3):
	# 	pts2.append(pts[i][0:2])
	# pts = pts2

	pts = [
		pts[0][0:2],
		pts[1][0:2],
		pts[2][0:2],
	]

	# print('2d', pts)
	correction = np.array([0, 0, 0])

	if not inSideCM(pts):
		a = []
		for i in range(0, 3):
			p0 = pts[i]
			p1 = pts[(i+1) % 3]
			x1 = 50
			x0 = -50
			cm1 = np.array([x1, -(p1[0] - p0[0])/(p1[1] - p0[1])*x1])
			cm0 = np.array([x0, -(p1[0] - p0[0])/(p1[1] - p0[1])*x0])
			xx = lineIntersection(p0, p1, cm0, cm1)
			a.append(xx)
		a = vmin(a)
		# print(a)
		correction = np.array([-a[0], -a[1], 0.0])
	return correction

# cm = 45*cos(pi/4)
#
# offset = [
# 	np.array([cm, cm]),
# 	np.array([cm, -cm]),
# 	np.array([-cm, -cm]),
# 	np.array([-cm, cm])
# ]
#
# pts = [
# 	np.array([30,60]) + offset[0],    # 0
# 	np.array([40,-25]) + offset[1],   # 1
# 	np.array([-31, 61]) + offset[3]   # 3
# ]
#
# corr = checkCM(pts)
# print(corr)


class Gait(object):
	"""
	Base class for gaits
	"""
	def __init__(self):
		# for a step pattern of 12, these are the offsets of each leg
		self.legOffset = [0, 6, 3, 9]
		# frame rotations for each leg
		self.cmrot = [pi/4, -pi/4, -3*pi/4, 3*pi/4]
		self.frame = [-pi/4, pi/4, 3*pi/4, -3*pi/4]  # this seem to work better ... wtf?
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
		# zrot = d2r(float(cmd[2]))  # should I assume this is always radians? save conversion
		zrot = cmd[2]
		# fromcenter = self.rest + self.body

		# value of this?
		#  rot = rot_z(zrot/2, fromcenter) - rot_z(-zrot/2, fromcenter)

		#  ans = {'linear': rc, 'rotational': rot, 'angle': zrot}
		ans = {'linear': rc, 'angle': zrot}  # FIXME: 20161119, make a tuple?

		return ans

	def command(self, cmd, moveFoot, steps=12):
		"""
		func is the quadruped move foot function for a specific leg
		"""
		# handle no movement command ... do else where?
		if sqrt(cmd[0]**2 + cmd[1]**2 + cmd[2]**2) < 0.001:
			for leg in range(0, 4):
				moveFoot(leg, self.rest)  # move to resting position
				# print('Foot[{}]: {:.2f} {:.2f} {:.2f}'.format(leg, *(self.rest)))
			# Servo.bulkWrite()
			return

		# cmd = [100.0, 0.0, 0.0]

		# frame rotations for each leg
		# frame = [-pi/4, pi/4, 3*pi/4, -3*pi/4]

		for i in range(0, steps):  # iteration, there are 12 steps in gait cycle
			footPos = []
			for legNum in [0, 2, 1, 3]:  # order them diagonally
				rcmd = self.calcRotatedOffset(cmd, legNum)
				index = (i + self.legOffset[legNum]) % 12
				pos = self.eachLeg(index, rcmd)  # move each leg appropriately
				# print('Foot[{}]: {:.2f} {:.2f} {:.2f}'.format(legNum, *(pos)))
				# if legNum == 0: print('New  [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, pos[0], pos[1], pos[2]))
				footPos.append([index, pos, legNum])  # all in leg frame
			# hate this!!!
			temp = []

			# account for base, in base frame
			cm = 45*cos(pi/4)
			base = [
				np.array([cm, cm, 0]),
				np.array([cm, -cm, 0]),
				np.array([-cm, -cm, 0]),
				np.array([-cm, cm, 0])
			]

			for p in footPos:  # p = [index, (x,y,z), legNum]
				if p[0] > 2: temp.append(rot_z(self.cmrot[p[2]], p[1])+base[p[2]])
			if len(temp) != 3:
				print('fuck ... wrong points:', len(temp))

			correction = checkCM(temp)
			# correction = np.array([0, 0, 0])
			print('correction: {:.2f} {:.2f} {:.2f}'.format(*correction))

			temp = []  # double check CM
			order = [0, 2, 1, 3]
			for i in range(0, 4):
				index = footPos[i][0]
				legNum = order[i]
				n = footPos[i][1]
				if index > 2:  # check index to see if leg moving
					n = n+rot_z(self.frame[legNum], correction)  # leg space
					# temp.append(rot_z(self.cmrot[footPos[i][2]], n)+base[footPos[i][2]])
					temp.append(rot_z(self.cmrot[footPos[i][2]], n)+base[footPos[i][2]])
					# print('index', footPos[legNum][0])
				moveFoot(legNum, n)

			for i in range(0, len(temp)):
				print('Foot[?]: {:.2f} {:.2f} {:.2f}'.format(*(temp[i])))

			# print('temp len:{}'.format(len(temp)))
			print('double check: {}'.format(inSideCM(temp, True)))

			# bulkWrite()
			Servo.bulkWrite(Servo.ser)
			# time.sleep(0.1)
			time.sleep(0.25)
			# time.sleep(1)


class DiscreteRippleGait(Gait):
	def __init__(self, h, r):
		Gait.__init__(self)
		self.phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]  # foot pos in gait sequence
		maxl = h  # lifting higher gives me errors
		minl = maxl/2
		# self.z = [minl, maxl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # leg height
		self.z = [minl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # leg height
		self.rest = r  # idle leg position

	def eachLeg(self, index, cmd):
		"""
		interpolates the foot position of each leg
		cmd:
			linear (mm)
			angle (rads)
		"""
		rest = self.rest
		i = index
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


# class ContinousRippleGait(Gait):
# 	alpha = 1.0
#
# 	def __init__(self, h, r):
# 		Gait.__init__(self)
# 		self.height = h
# 		self.rest = r
#
# 	@staticmethod
# 	def phi(x):
# 		"""
# 		The phase
# 		"""
# 		phi = 0.0
# 		if x <= 3.0:
# 			phi = 1/3*(3.0-x)
# 		else:
# 			phi = 1/9*(x-3)
# 		return phi
#
# 	def z(self, x):
# 		"""
# 		Leg height
#
# 		duty cycle:
# 			0-3: leg lifted
# 			3-12: leg on ground
# 			duty = (12-3)/12 = 0.75 = 75% a walking gait
# 		"""
# 		height = self.height
# 		z = 0.0
# 		if x <= 1:
# 			z = height/1.0*x
# 		elif x <= 2.0:
# 			z = height
# 		elif x <= 3.0:
# 			z = -height/1.0*(x-2.0)+height
# 		return z
#
# 	def eachLeg(self, index, cmd):
# 		"""
# 		interpolates the foot position of each leg
# 		"""
# 		rest = self.rest
# 		i = (index*self.alpha) % 12
# 		phi = self.phi(i)
# 		z = self.z(i)
#
# 		# rotational commands -----------------------------------------------
# 		angle = cmd['angle']/2-cmd['angle']*phi
# 		rest_rot = rot_z(-angle, rest)
# 		# rest_rot[2] = 0  # let linear handle z height
#
# 		# linear commands ----------------------------------------------------
# 		linear = cmd['linear']
# 		xx = linear[0]
# 		yy = linear[1]
#
# 		# create new move command
# 		move = np.array([
# 			xx/2 - phi*xx,
# 			yy/2 - phi*yy,
# 			z
# 		])
#
# 		# new foot position: newpos = rot + move ----------------------------
# 		newpos = move + rest_rot
# 		return newpos
