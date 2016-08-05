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
import sys
import os
sys.path.insert(0, os.path.abspath('../..'))
from lib.zmqclass import Sub as zmqSub

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
	phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]  # foot pos in gait sequence
	maxl = 0.2
	minl = 0.1
	z = [minl, maxl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # leg height
	E = [0/9, 3/9, 6/9, 9/9, 6/9, 3/9, 0/9, -3/9, -6/9, -9/9, -6/9, -3/9]  # sway

	def __init__(self, robot):
		# self.current_step = 0
		self.legOffset = [0, 6, 3, 9]
		# self.i = 0
		self.robot = robot

	def __del__(self):
		"""
		This is harsh, I just throw the leg up into a storage position. Should
		be more graceful ... oh well.
		"""
		angles = [0, 90, 0]
		# angles = [0, 45, -135]
		for leg in range(0, 4): self.pose(angles, leg)
		time.sleep(1)

	def eachLeg(self, legNum, index, cmd):
		"""
		robot paper
		"""
		phi = self.phi
		offset = self.legOffset
		z = self.z
		E = self.E
		zrot = d2r(float(cmd[2]))
		rest = self.robot.getFoot0(legNum)
		# print('rest', rest)

		i = (index + offset[legNum]) % 12  # len(self.z)

		# get rotation distance: dist = rot_z(angle, rest) - rest
		# this just reduces the function calls and math
		c = cos(zrot)
		s = sin(zrot)
		rot = [
			c*rest[0] - s*rest[1] - rest[0],
			s*rest[0] + c*rest[1] - rest[1]
		]

		# combine delta move and delta rotation (add vectors)
		# delta is the length of the step
		# add together the linear distance and rotation distance
		# FIXME: there needs to be a limit (max length) otherwise you can command too much
		xx = cmd[0] + rot[0]
		yy = cmd[1] + rot[1]
		# xx = cmd[0]
		# yy = cmd[1]

		# create new move command
		move = np.array([
			xx/2 - phi[i]*xx,
			yy/2 - phi[i]*yy,
			# xx/2 - phi[i]*xx + xx*E[i]/3,  # these don't work
			# yy/2 - phi[i]*yy + yy*E[i]/3,
			-rest[2]*z[i]  # this will subtract off the height -> raise leg
		])

		# new foot position: newpos = rest + move
		newpos = rest + move

		#
		# if legNum in [0]:
		# 	print('Rot [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, rot[0], rot[1], rot[2]))
		# 	print('Move [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, move[0], move[1], move[2]))
		# 	print('leg {} Newpos [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(legNum, i, newpos[0], newpos[1], newpos[2]))

		# now move leg/servos
		self.robot.moveFoot(legNum, newpos)
		# time.sleep(0.25)
		time.sleep(0.01)

	def command(self, cmd):
		# handle no movement command ... do else where?
		if sqrt(cmd[0]**2 + cmd[1]**2 + cmd[2]**2) < 0.001:
			for leg in range(0, 4): self.robot.legs[leg].reset()
			time.sleep(0.005)
			return

		# frame rotations for each leg
		# frame = [pi/4, -pi/4, -3*pi/4, 3*pi/4]
		frame = [-pi/4, pi/4, 3*pi/4, -3*pi/4]  # opposite of paper

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
			# time.sleep(0.05)  # 20 Hz, not sure of value
			time.sleep(0.005)

	def pose(self, angles, leg=0):
		# Servo.all_stop()
		pts = self.robot.legs[leg].fk(*angles)  # allows angles out of range
		# self.robot.moveFoot(leg, pts)
		self.robot.legs[leg].move(*pts)
		# s = self.robot.legs[leg].servos
		# print('angles: {:.2f} {:.2f} {:.2f}'.format(s[0].angle, s[1].angle, s[2].angle))
		# print('pts: {:.2f} {:.2f} {:.2f}'.format(*pts))

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
		'legAngleLimits': [[-80, 80], [-80, 90], [-170, 0]],
		'servoRangeAngles': [[-90, 90], [-90, 90], [-180, 0]]
	}
	robot = Quadruped(test)
	crawl = CrawlGait(robot)

	Servo.all_stop()

	try:
		if 1:  # ps4 drives
			sub = zmqSub('js', ('localhost', '9000'))
			while True:
				topic, msg = sub.recv()

				# msg values range between (-1, 1)
				if msg and topic == 'js':
					# print('msg:', msg)
					# continue

					x = msg['cmd']['linear']['x']
					y = msg['cmd']['linear']['y']
					rz = msg['cmd']['angular']['z']
					cmd = [100*x, 100*y, 100*rz]
					print('***********************************')
					print('* xyz {:.2f} {:.2f} {:.2f} *'.format(x,y,rz))
					print('* cmd {:.2f} {:.2f} {:.2f} *'.format(*cmd))
					print('***********************************')
					crawl.command(cmd)
				time.sleep(0.01)
		elif 0:  # walk
			i = 5
			time.sleep(3)
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

		elif 0:  # set all 4 lgs to angles
			angles = [0, 90, 0]
			for leg in range(0, 4): crawl.pose(angles, leg)
			time.sleep(1)
			angles = [0, 45, -150]
			for leg in range(0, 4): crawl.pose(angles, leg)
			time.sleep(1)
			Servo.all_stop()

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
