#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from Leg import Leg
import time
import numpy as np
# from tranforms import rotateAroundCenter, distance
import logging
from math import cos, sin, sqrt, pi
from math import radians as d2r
from Servo import Servo

logging.getLogger("Adafruit_I2C").setLevel(logging.ERROR)

##########################

# move to transforms?
def rot_z(t, c):
	"""
	t - theta [radians]
	c - [x,y,z]
	"""
	return [c[0]*cos(t)-c[1]*sin(t), c[0]*sin(t)+c[1]*cos(t), c[2]]


class CrawlGait(object):
	"""
	Slow stable, 3 legs on the ground at all times

	This solution works but only allows 1 gait ... need to have multiple gaits
	"""
	# offset = [0, 6, 3, 9]
	phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]
	maxl = 0.50
	minl = 0.25
	# z = [minl, maxl, maxl, minl, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
	z = [minl, maxl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

	def __init__(self, robot):
		# self.current_step = 0
		self.legOffset = [0, 6, 3, 9]
		# self.i = 0
		self.robot = robot

	def eachLeg(self, legNum, index, cmd):
		"""
		robot paper
		"""
		phi = self.phi
		offset = self.legOffset
		z = self.z
		# offset = [0, 6, 3, 9]
		# phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]
		# # z = [minl, maxl, maxl, minl, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
		# z = [minl, maxl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		# delta = sqrt(cmd[0]**2 + cmd[1]**2)
		zrot = d2r(float(cmd[2]))
		rest = self.robot.getFoot0(legNum)
		# print('rest', rest)

		i = (index + offset[legNum]) % 12  # len(self.z)
		c = cos(zrot)
		s = sin(zrot)
		rot = np.array([
			c*rest[0]-s*rest[1],
			s*rest[0]+c*rest[1],
			rest[2]  # need this for subtraction
		])

		rot -= rest  # make rot a delta rotation

		# combine delta move and delta rotation (add vectors)
		xx = cmd[0] + rot[0]
		yy = cmd[1] + rot[1]
		move = np.array([
			xx/2 - phi[i]*xx,
			yy/2 - phi[i]*yy,
			-rest[2]*z[i]
		])
		newpos = rest + move

		if legNum in [0]:
			# print('Rot [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, rot[0], rot[1], rot[2]))
			# print('Move [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, move[0], move[1], move[2]))
			print('leg {} Newpos [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(legNum, i, newpos[0], newpos[1], newpos[2]))

		# now move leg/servos
		self.robot.moveFoot(legNum, newpos)

	def command(self, cmd):
		# frame rotations for each leg
		frame = [pi/4, -pi/4, -3*pi/4, 3*pi/4]

		# only calc this 4 times, not 12*4 times!
		rot_cmd = []
		for i in range(0, 4):
			rc = rot_z(frame[i], cmd)
			rot_cmd.append(rc)
			print('cmd[{}]: {:.2f} {:.2f} {:.2f}'.format(i, rc[0], rc[1], rc[2]))

		for i in range(0, 12):  # iteration, there are 12 steps in gait cycle
			for legNum in [0, 2, 1, 3]:  # order them diagonally
				# rcmd = rot_z(frame[legNum], cmd)
				rcmd = rot_cmd[legNum]
				self.eachLeg(legNum, i, rcmd)  # move each leg appropriately
			# self.eachLeg(0, i, cmd)
			time.sleep(0.05)  # 20 Hz, not sure of value
			# time.sleep(0.5)

	# def step(self, i, cmd):
	# 	"""
	# 	"""
	# 	# put this stuff back!!!!!!!!!! FIXME!!!!
	# 	# for legNum in [0, 2, 1, 3]:  # order them diagonally
	# 	# 	self.eachLeg(legNum, i, cmd)  # move each leg appropriately
	# 	# 	time.sleep(0.01)  # need some time to wait for servos to move
	# 	self.eachLeg(0, i, cmd)

	def pose(self, angles, leg=0):
		Servo.all_stop()
		pts = self.robot.legs[leg].fk(*angles)  # allows angles out of range
		# self.robot.moveFoot(leg, pts)
		self.robot.legs[leg].move(*pts)
		s = self.robot.legs[leg].servos
		print('angles: {:.2f} {:.2f} {:.2f}'.format(s[0].angle, s[1].angle, s[2].angle))
		print('pts: {:.2f} {:.2f} {:.2f}'.format(*pts))

##########################


class Quadruped(object):
	"""
	"""
	def __init__(self, data):
		self.legs = []
		for i in range(0, 4):
			channel = i*4
			self.legs.append(
				Leg(
					data['legLengths'],
					[channel, channel+1, channel+2]
				)
			)

			# grab init data for servos from json data file
			for s in range(0, 3):
				if 'servoRangeAngles' in data:  # mapping of angles to pulses
					self.legs[i].servos[s].setServoRangeAngle(*data['servoRangeAngles'][s])
				if 'legAngleLimits' in data:  # user defined limits to avoid servo issues
					self.legs[i].servos[s].setServoLimits(*data['legAngleLimits'][s])
				if 'servoRangePulse' in data:  # mapping of msec to pulses
					raise Exception('servoRangePulse not implemented in json file yet ... bye')

	def __del__(self):
		"""
		Leg kills all servos on exit
		"""
		pass

	def getFoot0(self, i):
		return self.legs[i].foot0

	def moveFoot(self, i, pos):
		# if i == 0: print('Leg 0 ------------------------------')
		self.legs[i].move(*pos)


if __name__ == "__main__":
	# angles are always [min, max]
	# S0 is mapped backwards because of servo orientation
	# leg 1: [180, 0], [-90, 90], [0, -180]     [45, 0, -90]
	# leg 2: [[0, 180], [-90, 90], [0, -180]]   [45,-20, -70]
	test = {
		'legLengths': {
			'coxaLength': 26,
			'femurLength': 42,
			'tibiaLength': 63
		},
		'legAngleLimits': [[-80, 80], [-80, 80], [-170, -10]],
		'servoRangeAngles': [[-90, 90], [-90, 90], [-180, 0]]
	}
	robot = Quadruped(test)
	crawl = CrawlGait(robot)

	Servo.all_stop()

	try:
		if 1:  # walk
			i = 5
			while i:
				print('step:', i)
				crawl.command([100.0, 0.0, 0.0])  # x mm, y mm, theta degs
				# time.sleep(1)
				i -= 1
		elif 0:  # set leg to specific orientation
			angles = [0, 0, -90]
			crawl.pose(angles, 2)
			time.sleep(1)
			Servo.all_stop()
			time.sleep(0.5)
		elif 0:
			# Alpha:
			# Beta: -60 to 90 is good
			# Gamma: 0 to -180 is good
			leg = 1
			dt = 0.1
			for i in range(-90, 90, 10):
				angles = [i, 60, 0]
				print('--------------------')
				print('cmd angles: {:.2f} {:.2f} {:.2f}'.format(*angles))
				crawl.pose(angles, leg)
				time.sleep(dt)
			for i in range(0, 90, 10):
				angles = [0, i, 0]
				print('--------------------')
				print('cmd angles: {:.2f} {:.2f} {:.2f}'.format(*angles))
				crawl.pose(angles, leg)
				time.sleep(dt)
			for i in range(-160, -10, 10):
				angles = [0, 60, i]
				print('--------------------')
				print('cmd angles: {:.2f} {:.2f} {:.2f}'.format(*angles))
				crawl.pose(angles, leg)
				time.sleep(dt)
			Servo.all_stop()
			time.sleep(0.5)
		else:
			angles = [0, 0, 0]
			crawl.pose(angles, 0)
			crawl.pose(angles, 1)
			time.sleep(1)
			Servo.all_stop()
			time.sleep(0.1)

	except Exception as e:
		print(e)
		print('Crap!!!!')
		Servo.all_stop()
		time.sleep(1)
		raise
