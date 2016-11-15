#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from Leg import Leg
# import time
# import numpy as np
# import logging
# from math import cos, sin, sqrt, pi
# from math import radians as d2r
from pyxl320 import ServoSerial
from pyxl320 import DummySerial

# from Gait import DiscreteRippleGait, ContinousRippleGait
#
##########################
#
#
# # move to kinematics?
# def rot_z(t, c):
# 	"""
# 	t - theta [radians]
# 	c - [x,y,z] or [x,y] ... the function detects 2D or 3D vector
# 	"""
# 	if len(c) == 3:
# 		ans = np.array([
# 			c[0]*cos(t)-c[1]*sin(t),
# 			c[0]*sin(t)+c[1]*cos(t),
# 			c[2]
# 		])
# 	else:
# 		ans = np.array([
# 			c[0]*cos(t)-c[1]*sin(t),
# 			c[0]*sin(t)+c[1]*cos(t)
# 		])
#
# 	return ans
#
#
# class Gait(object):
# 	def command(self):
# 		pass
#
#
# class CrawlGait(object):
# 	"""
# 	Slow stable, 3 legs on the ground at all times
#
# 	This solution works but only allows 1 gait ... need to have multiple gaits
# 	"""
# 	phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]  # foot pos in gait sequence
# 	maxl = 25  # lifting higher gives me errors
# 	minl = 12.5
# 	z = [minl, maxl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # leg height
#
# 	def __init__(self, robot):
# 		self.legOffset = [0, 6, 3, 9]
# 		self.robot = robot
#
# 	def eachLeg(self, legNum, index, cmd):
# 		"""
# 		interpolates
# 		"""
# 		phi = self.phi           # phase
# 		offset = self.legOffset  # where in the gait is leg legNum
# 		z = self.z               # leg height
# 		rest = self.robot.getFoot0(legNum)
# 		i = (index + offset[legNum]) % 12  # len(self.z)
#
# 		# rotational commands -----------------------------------------------
# 		rest_rot = rot_z(-cmd['angle']/2, rest)
# 		rotational = cmd['rotational']
# 		xx = rotational[0]
# 		yy = rotational[1]
#
# 		# create new move command
# 		turn = np.array([
# 			xx/2 - phi[i]*xx,
# 			yy/2 - phi[i]*yy,
# 			0  # linear handles leg raising
# 		])
#
# 		# linear commands ----------------------------------------------------
# 		linear = cmd['linear']
# 		xx = linear[0]
# 		yy = linear[1]
#
# 		# create new move command
# 		move = np.array([
# 			xx/2 - phi[i]*xx,
# 			yy/2 - phi[i]*yy,
# 			# -rest[2]*z[i]  # this will subtract off the height -> raise leg
# 			+z[i]
# 		])
#
# 		# new foot position: newpos = rest + move ----------------------------
# 		newpos = rest_rot + move + turn
#
# 		#
# 		if legNum in [0]:
# 			# print('Rot [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, rot[0], rot[1], rot[2]))
# 			# print('Move [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, move[0], move[1], move[2]))
# 			print('New  [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, newpos[0], newpos[1], newpos[2]))
#
# 		# now move leg/servos
# 		self.robot.moveFoot(legNum, newpos)
# 		time.sleep(0.01)  # 4 legs * 12 steps each * 0.01 sec = 0.48 sec for one complete cycle
#
# 	def calcRotatedOffset(self, cmd):
# 		"""
# 		calculate the foot offsets for each leg and delta linear/rotational
# 		in - cmd(x,y,z_rotation)
# 		out - array(leg0, leg1, ...)
# 			where leg0 = {'linear': [x,y], 'rotational': [x,y], 'angle': zrotation(rads)}
# 		"""
# 		# frame rotations for each leg
# 		frame = [-pi/4, pi/4, 3*pi/4, -3*pi/4]
#
# 		# only calc this 4 times, not 12*4 times!
# 		rot_cmd = []  # (xx, yy) for each leg
# 		for i in range(0, 4):
# 			# I could do the same here as I do below for rotation
# 			rc = rot_z(frame[i], cmd)
# 			rest = self.robot.getFoot0(i)
# 			# rot_cmd.append(rc)
# 			# print('cmd[{}]: {:.2f} {:.2f} {:.2f}'.format(i, rc[0], rc[1], rc[2]))
#
# 			# get rotation distance: dist = rot_z(angle, rest) - rest
# 			# this just reduces the function calls and math
# 			zrot = d2r(float(cmd[2]))  # should I assume this is always radians? save conversion
#
# 			fromcenter = rest + np.array([72.12, 0, 0])
#
# 			rot = rot_z(zrot/2, fromcenter) - rot_z(-zrot/2, fromcenter)
#
# 			ans = {'linear': rc, 'rotational': rot, 'angle': zrot}
#
# 			rot_cmd.append(ans)
#
# 		return rot_cmd
#
# 	def command(self, cmd):
# 		# handle no movement command ... do else where?
# 		if sqrt(cmd[0]**2 + cmd[1]**2 + cmd[2]**2) < 0.001:
# 			for leg in range(0, 4):
# 				self.robot.legs[leg].reset()
# 			return
#
# 		# print('cmd[{}]: {:.2f} {:.2f} {:.2f}'.format(i, rc[0], rc[1], rc[2]))
#
# 		rot_cmd = self.calcRotatedOffset(cmd)
#
# 		for i in range(0, 12):  # iteration, there are 12 steps in gait cycle
# 			# for legNum in [0, 2, 1, 3]:  # order them diagonally
# 			for legNum in [0]:  # order them diagonally
# 				rcmd = rot_cmd[legNum]
# 				self.eachLeg(legNum, i, rcmd)  # move each leg appropriately
# 			time.sleep(0.5)
#
#
# ###########################
#
#
#
# class ScaleCrawlGait(object):
# 	"""
# 	Slow stable, 3 legs on the ground at all times
#
# 	This solution works but only allows 1 gait ... need to have multiple gaits
# 	"""
# 	phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]  # foot pos in gait sequence
# 	maxl = 25  # lifting higher gives me errors
# 	minl = 12.5
# 	z = [minl, maxl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # leg height
#
# 	def __init__(self, robot):
# 		self.legOffset = [0, 6, 3, 9]
# 		self.robot = robot
#
# 	def eachLeg(self, legNum, index, cmd):
# 		"""
# 		interpolates
# 		"""
# 		phi = self.phi           # phase
# 		offset = self.legOffset  # where in the gait is leg legNum
# 		z = self.z               # leg height
# 		rest = self.robot.getFoot0(legNum)
# 		i = (index + offset[legNum]) % 12  # len(self.z)
#
# 		# rotational commands -----------------------------------------------
# 		rest_rot = rot_z(-cmd['angle']/2, rest)
# 		rotational = cmd['rotational']
# 		xx = rotational[0]
# 		yy = rotational[1]
#
# 		# create new move command
# 		turn = np.array([
# 			xx/2 - phi[i]*xx,
# 			yy/2 - phi[i]*yy,
# 			0  # linear handles leg raising
# 		])
#
# 		# linear commands ----------------------------------------------------
# 		linear = cmd['linear']
# 		xx = linear[0]
# 		yy = linear[1]
#
# 		# create new move command
# 		move = np.array([
# 			xx/2 - phi[i]*xx,
# 			yy/2 - phi[i]*yy,
# 			# -rest[2]*z[i]  # this will subtract off the height -> raise leg
# 			z[i]
# 		])
#
# 		# new foot position: newpos = rest + move ----------------------------
# 		newpos = rest_rot + move + turn
#
# 		#
# 		if legNum in [0]:
# 			# print('Rot [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, rot[0], rot[1], rot[2]))
# 			# print('Move [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, move[0], move[1], move[2]))
# 			print('New  [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, newpos[0], newpos[1], newpos[2]))
#
# 		# now move leg/servos
# 		self.robot.moveFoot(legNum, newpos)
# 		time.sleep(0.01)  # 4 legs * 12 steps each * 0.01 sec = 0.48 sec for one complete cycle
#
# 	def calcRotatedOffset(self, cmd):
# 		"""
# 		calculate the foot offsets for each leg and delta linear/rotational
# 		in - cmd(x,y,z_rotation)
# 		out - array(leg0, leg1, ...)
# 			where leg0 = {'linear': [x,y], 'rotational': [x,y], 'angle': zrotation(rads)}
# 		"""
# 		# frame rotations for each leg
# 		frame = [-pi/4, pi/4, 3*pi/4, -3*pi/4]
#
# 		# only calc this 4 times, not 12*4 times!
# 		rot_cmd = []  # (xx, yy) for each leg
# 		for i in range(0, 4):
# 			# I could do the same here as I do below for rotation
# 			rc = rot_z(frame[i], cmd)
# 			rest = self.robot.getFoot0(i)
# 			# rot_cmd.append(rc)
# 			# print('cmd[{}]: {:.2f} {:.2f} {:.2f}'.format(i, rc[0], rc[1], rc[2]))
#
# 			# get rotation distance: dist = rot_z(angle, rest) - rest
# 			# this just reduces the function calls and math
# 			zrot = d2r(float(cmd[2]))  # should I assume this is always radians? save conversion
#
# 			fromcenter = rest + np.array([72.12, 0, 0])
#
# 			rot = rot_z(zrot/2, fromcenter) - rot_z(-zrot/2, fromcenter)
#
# 			ans = {'linear': rc, 'rotational': rot, 'angle': zrot}
#
# 			rot_cmd.append(ans)
#
# 		return rot_cmd
#
# 	def command(self, cmd):
# 		# handle no movement command ... do else where?
# 		if sqrt(cmd[0]**2 + cmd[1]**2 + cmd[2]**2) < 0.001:
# 			for leg in range(0, 4):
# 				self.robot.legs[leg].reset()
# 			return
#
# 		# print('cmd[{}]: {:.2f} {:.2f} {:.2f}'.format(i, rc[0], rc[1], rc[2]))
# 		scale = 0.50
# 		cmd = [scale*204.0, 0.0, 0.0]
# 		rot_cmd = self.calcRotatedOffset(cmd)
#
# 		for i in range(0, 12):  # iteration, there are 12 steps in gait cycle
# 			# for legNum in [0, 2, 1, 3]:  # order them diagonally
# 			for legNum in [0]:  # order them diagonally
# 				rcmd = rot_cmd[legNum]
# 				self.eachLeg(legNum, i, rcmd)  # move each leg appropriately
# 			time.sleep(0.5)
#
#
#
# ##########################
#
#
# class TimeCrawlGait(object):
# 	"""
# 	Slow stable, 3 legs on the ground at all times
#
# 	This solution works but only allows 1 gait ... need to have multiple gaits
# 	"""
# 	# phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]  # foot pos in gait sequence
# 	# maxl = 0.2
# 	# minl = 0.1
# 	# z = [minl, maxl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # leg height
#
# 	def __init__(self, robot):
# 		self.legOffset = [0.0, 6.0, 3.0, 9.0]
# 		self.robot = robot
# 		self.height = 5.0  # leg pickup height in mm
# 		self.alpha = 1.0   # speed modifier, smaller/slower, larger/faster
#
# 	def phi(self, x):
# 		phi = 0.0
# 		if x > 12.0:
# 			print('crap ... too high: {}'.format(x))
# 		elif x > 3.0:
# 			phi = 1/9*(x-3.0)
# 		else:
# 			phi = -1/3 + 1.0
# 		return phi
#
# 	def z(self, x):
# 		z = 0.0
# 		if x <= 1.5:
# 			z = self.height/1.5*x
# 		elif x <= 3.0:
# 			z = -self.height/1.5*(x-1.5)
# 		return z
#
# 	def eachLeg(self, legNum, index, cmd):
# 		"""
# 		interpolates
# 		"""
# 		x = (index + self.legOffset[legNum]) % 12.0
# 		# x = (self.alpha*(time.time() + self.legOffset[legNum])) % 12.0
# 		phi = self.phi(x)           # phase
# 		# offset = self.legOffset  # where in the gait is leg legNum
# 		z = self.z(x)               # leg height
# 		rest = self.robot.getFoot0(legNum)
# 		# i = (index + offset[legNum]) % 12  # len(self.z)
#
# 		# rotational commands -----------------------------------------------
# 		rest_rot = rot_z(-cmd['angle']/2, rest)
# 		rotational = cmd['rotational']
# 		xx = rotational[0]
# 		yy = rotational[1]
#
# 		# create new move command
# 		turn = np.array([
# 			xx/2 - phi*xx,
# 			yy/2 - phi*yy,
# 			0  # linear handles leg raising
# 		])
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
# 			-rest[2]*z  # this will subtract off the height -> raise leg
# 		])
#
# 		# new foot position: newpos = rest + move ----------------------------
# 		newpos = rest_rot + move + turn
#
# 		#
# 		if legNum in [0]:
# 			# print('Rot [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, rot[0], rot[1], rot[2]))
# 			# print('Move [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, move[0], move[1], move[2]))
# 			print('New  [{:.2f}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(x, newpos[0], newpos[1], newpos[2]))
#
# 		# now move leg/servos
# 		self.robot.moveFoot(legNum, newpos)
# 		# time.sleep(0.01)  # 4 legs * 12 steps each * 0.01 sec = 0.48 sec for one complete cycle
#
# 	def calcRotatedOffset(self, cmd):
# 		"""
# 		calculate the foot offsets for each leg and delta linear/rotational
# 		in - cmd(x,y,z_rotation)
# 		out - array(leg0, leg1, ...)
# 			where leg0 = {'linear': [x,y], 'rotational': [x,y], 'angle': zrotation(rads)}
# 		"""
# 		# frame rotations for each leg
# 		frame = [-pi/4, pi/4, 3*pi/4, -3*pi/4]
#
# 		# only calc this 4 times, not 12*4 times!
# 		rot_cmd = []  # (xx, yy) for each leg
# 		for i in range(0, 4):
# 			# I could do the same here as I do below for rotation
# 			rc = rot_z(frame[i], cmd)
# 			rest = self.robot.getFoot0(i)
# 			# rot_cmd.append(rc)
# 			# print('cmd[{}]: {:.2f} {:.2f} {:.2f}'.format(i, rc[0], rc[1], rc[2]))
#
# 			# get rotation distance: dist = rot_z(angle, rest) - rest
# 			# this just reduces the function calls and math
# 			zrot = d2r(float(cmd[2]))  # should I assume this is always radians? save conversion
#
# 			fromcenter = rest + np.array([72.12, 0, 0])
#
# 			rot = rot_z(zrot/2, fromcenter) - rot_z(-zrot/2, fromcenter)
#
# 			ans = {'linear': rc, 'rotational': rot, 'angle': zrot}
#
# 			rot_cmd.append(ans)
#
# 		return rot_cmd
#
# 	def command(self, cmd):
# 		# handle no movement command ... do else where?
# 		if sqrt(cmd[0]**2 + cmd[1]**2 + cmd[2]**2) < 0.001:
# 			for leg in range(0, 4):
# 				self.robot.legs[leg].reset()
# 			return
#
# 		# print('cmd[{}]: {:.2f} {:.2f} {:.2f}'.format(i, rc[0], rc[1], rc[2]))
#
# 		rot_cmd = self.calcRotatedOffset(cmd)
#
# 		# for i in range(0, 12):  # iteration, there are 12 steps in gait cycle
# 		delta = 1
# 		for index in range(0, 12*delta):
# 			i = index/delta
# 			# for legNum in [0, 2, 1, 3]:  # order them diagonally
# 			for legNum in [0]:  # order them diagonally
# 				rcmd = rot_cmd[legNum]
# 				self.eachLeg(legNum, i, rcmd)  # move each leg appropriately
# 			# time.sleep(1/delta)


##########################

class RobotException(Exception):
	pass


class Robot(object):
	def __init__(self):
		pass


class Quadruped(object):
	"""
	This is the low level driver
	"""
	def __init__(self, data):
		"""
		Sets up all 4 legs and servos. Also setups limits for angles and servo
		pulses.
		"""
		if 'serialPort' in data:
			self.ser = ServoSerial(data['serialPort'])
		else:
			self.ser = DummySerial('test_port')

		self.ser.open()

		if 'legLengths' not in data or 'legAngleLimits' not in data:
			raise RobotException('Quadruped json data missing required keys')

		if 'legOffset' not in data:
			raise RobotException('Quadruped json data missing required keys')

		self.legs = []
		for i in range(0, 4):  # 4 legs
			channel = i*3  # 3 servos per leg
			self.legs.append(
				Leg(
					data['legLengths'],
					[channel+1, channel+2, channel+3],  # servos numbered 1-12
					self.ser,
					data['legAngleLimits'],
					data['legOffset']
				)
			)

	def __del__(self):
		"""
		Leg kills all servos on exit
		"""
		self.sit()
		pass

	def sit(self):
		"""
		sequence to sit down nicely
		"""
		pass

	def stand(self):
		"""
		sequence to stand up nicely
		"""
		pass

	def getFoot0(self, i):
		return self.legs[i].foot0

	def moveFoot(self, i, pos):
		"""
		moveFoot -> moveFootPosition ?

		Moves the foot of leg i to a position (x,y,z)
		"""
		return self.legs[i].move(*pos)

	def moveFootAngles(self, angles, leg=None):
		"""
		Sets servos of a leg, or all legs if no leg identified, to given angles.
		"""
		if leg is None:
			for i in range(0, 4):
				pts = self.legs[i].fk(*angles)  # allows angles out of range
				self.legs[i].move(*pts)
		else:
			pts = self.legs[leg].fk(*angles)  # allows angles out of range
			self.legs[leg].move(*pts)
