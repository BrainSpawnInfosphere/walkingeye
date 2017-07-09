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
from pyxl320 import ServoSerial
from pyxl320 import DummySerial
from Leg import Leg
from Gait import Gait

"""
Gait <- walking/climbing/dance/bored
pose <- sit/stand

move = move_array[0]
if move.type is 'walk':
	move.command(x)
elif move.type is 'climb':
	move.command(x)

array of movements [walk(dir, height), sit, stand, climb, dance, bored]

bored is its equivelant of twiddling its thumbs

FSM:
- states: happy, sad, bored, neutral

"""


class Pose(Gait):
	def __init__(self, r):
		Gait.__init__(self)
		self.rest = r  # idle leg position

	def eachLeg(self, index):
		"""
		interpolates the foot position of each leg
		cmd:
			linear (mm)
			angle (rads)
		"""
		rest = self.rest
		print('rest', rest)

		newpos = rest
		newpos[2] += 3.0*index
		return newpos

	def run(self):
		# need to do for each leg
		for i in range(12):
			foot = self.eachLeg(i)
			print('foot anim:', foot)


def run():
	# sport = '/dev/serial0'
	sport = None
	if sport:
		ser = ServoSerial(sport)
	else:
		ser = DummySerial('test')

	Servo.ser = ser  # set static servo serial comm

	leg = Leg([1, 2, 3])
	foot0 = leg.foot0
	print('foot0', foot0)

	angles = [0, 0, 0]
	pts = leg.fk(*angles)  # allows angles out of range
	print('pts', pts)
	leg.moveFoot(*pts)

	sit = Pose(leg.foot0)
	sit.run()
	time.sleep(2)
	print('Bye')


if __name__ == "__main__":
	run()


# # make a static method in Gait? Nothing else uses it
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
# class RobotTransform(object):
# 	"""
# 	Converts pts between the leg and body frame.
# 	"""
# 	def __init__(self, radius):
# 		"""
# 		in:
# 			radius - radius of body from CM in mm
# 			anglesB2L - angles to transform between body and leg frames
# 		"""
# 		# cmrot
# 		self.leg2body = [pi/4, -pi/4, -3*pi/4, 3*pi/4]  # legs to body frame # orig
# #         self.leg2body = [-pi/4, pi/4, 3*pi/4, -3*pi/4]  # legs to body frame
# 		# frame
# 		self.body2leg = [-pi/4, pi/4, 3*pi/4, -3*pi/4]  # body to leg frame # orig
# #         self.body2leg = [pi/4, -pi/4, -3*pi/4, 3*pi/4]  # body to leg frame
# 		# account for base, in base frame
# 		cm = radius*cos(pi/4)
# 		self.base = [
# 			np.array([cm, cm, 0]),
# 			np.array([cm, -cm, 0]),
# 			np.array([-cm, -cm, 0]),
# 			np.array([-cm, cm, 0])
# 		]
#
# 	def leg2Body(self, legNum, pts):
# 		"""
# 		Converts points from leg_frame to body_frame
# 		"""
# 		pts2 = rot_z(self.leg2body[legNum], pts) + self.base[legNum]
# 		return pts2
#
# 	def body2Leg(self, legNum, pts):
# 		"""
# 		Converts points from body_frame to leg_frame
# 		"""
# 		pts2 = rot_z(self.body2leg[legNum], pts-self.base[legNum])
# 		return pts2
#
#
# class Gait(object):
# 	"""
# 	Base class for gaits ans poses
# 	- should leg lengths be static?
# 	- rotation angles between frames are static
# 	"""
# 	def __init__(self):
# 		# for a step pattern of 12, these are the offsets of each leg
# 		self.legOffset = [0, 6, 3, 9]
# 		# frame rotations for each leg
# 		self.cmrot = [pi/4, -pi/4, -3*pi/4, 3*pi/4]
# 		self.frame = [-pi/4, pi/4, 3*pi/4, -3*pi/4]  # this seem to work better ... wtf?
# 		# the resting or idle position/orientation of a leg
# 		self.rest = None
#
# 	def calcRotatedOffset(self, cmd, i):
# 		"""
# 		calculate the foot offsets for each leg and delta linear/rotational
# 		in - cmd(x,y,z_rotation)
# 		out - array(leg0, leg1, ...)
# 			where leg0 = {'linear': [x,y], 'rotational': [x,y], 'angle': zrotation(rads)}
# 		"""
# 		# rotate the command into the leg frame
# 		frame_angle = self.frame[i]
# 		rc = rot_z(frame_angle, cmd)
#
# 		# get rotation distance: dist = rot_z(angle, rest) - rest
# 		# this just reduces the function calls and math
# 		# zrot = d2r(float(cmd[2]))  # should I assume this is always radians? save conversion
# 		zrot = cmd[2]
# 		# fromcenter = self.rest + self.body
#
# 		# value of this?
# 		#  rot = rot_z(zrot/2, fromcenter) - rot_z(-zrot/2, fromcenter)
#
# 		#  ans = {'linear': rc, 'rotational': rot, 'angle': zrot}
# 		ans = {'linear': rc, 'angle': zrot}  # FIXME: 20161119, make a tuple?
#
# 		return ans
#
# 	def command(self, cmd, moveFoot, steps=12):
# 		"""
# 		func is the quadruped move foot function for a specific leg
# 		"""
# 		# handle no movement command ... do else where?
# 		# if sqrt(cmd[0]**2 + cmd[1]**2 + cmd[2]**2) < 0.001:
# 		# 	for leg in range(0, 4):
# 		# 		moveFoot(leg, self.rest)  # move to resting position
# 		# 		# print('Foot[{}]: {:.2f} {:.2f} {:.2f}'.format(leg, *(self.rest)))
# 		# 	# Servo.bulkWrite()
# 		# 	return
#
# 		# cmd = [100.0, 0.0, 0.0]
#
# 		# frame rotations for each leg
# 		# frame = [-pi/4, pi/4, 3*pi/4, -3*pi/4]
#
# 		for i in range(0, steps):  # iteration, there are 12 steps in gait cycle
# 			footPos = []
# 			for legNum in [0, 2, 1, 3]:  # order them diagonally
# 				rcmd = self.calcRotatedOffset(cmd, legNum)
# 				index = (i + self.legOffset[legNum]) % 12
# 				pos = self.eachLeg(index, rcmd)  # move each leg appropriately
# 				# print('Foot[{}]: {:.2f} {:.2f} {:.2f}'.format(legNum, *(pos)))
# 				# if legNum == 0: print('New  [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, pos[0], pos[1], pos[2]))
# 				footPos.append([index, legNum, pos])  # all in leg frame
#
# 			# corr = Correction()
# 			# c = corr.calcCorrection(footPos)
# 			# feet = corr.rotateFeetCorrected(footPos, c)
# 			feet = footPos
# 			print('----------------------------')
# 			for foot in feet:
# 				legNum = foot[1]
# 				ft = foot[2]
# 				moveFoot(legNum, ft)
# 				print('Foot[{}]: {:.2f} {:.2f} {:.2f}'.format(legNum, *ft))
#
# 			# bulkWrite()
# 			Servo.bulkWrite(Servo.ser)
# 			time.sleep(0.1)
# 			# time.sleep(0.25)
# 			# time.sleep(1)
