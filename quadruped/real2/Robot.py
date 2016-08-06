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
	def command(self): pass

class CrawlGait(object):
	"""
	Slow stable, 3 legs on the ground at all times

	This solution works but only allows 1 gait ... need to have multiple gaits
	"""
	phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]  # foot pos in gait sequence
	maxl = 0.2
	minl = 0.1
	z = [minl, maxl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # leg height

	def __init__(self, robot):
		self.legOffset = [0, 6, 3, 9]
		self.robot = robot

	def eachLeg(self, legNum, index, cmd):
		"""
		interpolates
		"""
		phi = self.phi           # phase
		offset = self.legOffset  # where in the gait is leg legNum
		z = self.z               # leg height
		rest = self.robot.getFoot0(legNum)
		i = (index + offset[legNum]) % 12  # len(self.z)

		# rotational commands -----------------------------------------------
		rest_rot = rot_z(-cmd['angle']/2, rest)
		rotational = cmd['rotational']
		xx = rotational[0]
		yy = rotational[1]

		# create new move command
		turn = np.array([
			xx/2 - phi[i]*xx,
			yy/2 - phi[i]*yy,
			0  # linear handles leg raising
		])

		# linear commands ----------------------------------------------------
		linear = cmd['linear']
		xx = linear[0]
		yy = linear[1]

		# create new move command
		move = np.array([
			xx/2 - phi[i]*xx,
			yy/2 - phi[i]*yy,
			-rest[2]*z[i]  # this will subtract off the height -> raise leg
		])

		# new foot position: newpos = rest + move ----------------------------
		newpos = rest_rot + move + turn

		#
		# if legNum in [0]:
		# 	print('Rot [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, rot[0], rot[1], rot[2]))
		# 	print('Move [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, move[0], move[1], move[2]))
		# 	print('leg {} Newpos [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(legNum, i, newpos[0], newpos[1], newpos[2]))

		# now move leg/servos
		self.robot.moveFoot(legNum, newpos)
		time.sleep(0.01)  # 4 legs * 12 steps each * 0.01 sec = 0.48 sec for one complete cycle

	def calcRotatedOffset(self, cmd):
		"""
		calculate the foot offsets for each leg and delta linear/rotational
		in - cmd(x,y,z_rotation)
		out - array(leg0, leg1, ...)
			where leg0 = {'linear': [x,y], 'rotational': [x,y], 'angle': zrotation(rads)}
		"""
		# frame rotations for each leg
		frame = [-pi/4, pi/4, 3*pi/4, -3*pi/4]  # opposite of paper

		# only calc this 4 times, not 12*4 times!
		rot_cmd = []  # (xx, yy) for each leg
		for i in range(0, 4):
			# I could do the same here as I do below for rotation
			rc = rot_z(frame[i], cmd)
			rest = self.robot.getFoot0(i)
			# rot_cmd.append(rc)
			# print('cmd[{}]: {:.2f} {:.2f} {:.2f}'.format(i, rc[0], rc[1], rc[2]))

			# get rotation distance: dist = rot_z(angle, rest) - rest
			# this just reduces the function calls and math
			zrot = d2r(float(cmd[2]))  # should I assume this is always radians? save conversion

			fromcenter = rest + np.array([72.12, 0, 0])

			rot = rot_z(zrot/2, fromcenter) - rot_z(-zrot/2, fromcenter)

			ans = {'linear': rc, 'rotational': rot, 'angle': zrot}

			rot_cmd.append(ans)

		return rot_cmd

	def command(self, cmd):
		# handle no movement command ... do else where?
		if sqrt(cmd[0]**2 + cmd[1]**2 + cmd[2]**2) < 0.001:
			for leg in range(0, 4): self.robot.legs[leg].reset()
			return

		# print('cmd[{}]: {:.2f} {:.2f} {:.2f}'.format(i, rc[0], rc[1], rc[2]))

		rot_cmd = self.calcRotatedOffset(cmd)

		for i in range(0, 12):  # iteration, there are 12 steps in gait cycle
			for legNum in [0, 2, 1, 3]:  # order them diagonally
				rcmd = rot_cmd[legNum]
				self.eachLeg(legNum, i, rcmd)  # move each leg appropriately


##########################

class Robot(object):
	def __init__(self):
		pass

class Quadruped(object):
	"""
	This is the low level driver
	"""
	def __init__(self, data):
		"""
		Sets up alll 4 legs and servos. Also setups limits for angles and servo
		pulses.
		"""
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

		This is harsh, I just throw the leg up into a storage position. Should
		be more graceful ... oh well.
		"""
		angles = [0, 90, 0]
		# angles = [0, 45, -135]
		# for leg in range(0, 4): self.pose(angles, leg)
		self.moveFootAngles(angles)
		time.sleep(1)

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
		# if i == 0: print('Leg 0 ------------------------------')
		self.legs[i].move(*pos)

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


class TestQuadruped(Quadruped):
	def __init__(self, data):
		Quadruped.__init__(self, data)

		Servo.all_stop()

		robot = Quadruped(test)
		self.crawl = CrawlGait(robot)

	def run(self):
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
				cmd = [100*x, 100*y, 40*rz]
				print('***********************************')
				print('* xyz {:.2f} {:.2f} {:.2f} *'.format(x, y, rz))
				print('* cmd {:.2f} {:.2f} {:.2f} *'.format(*cmd))
				print('***********************************')
				self.crawl.command(cmd)
			time.sleep(0.01)


def run():
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

	robot = TestQuadruped(test)
	robot.run()


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
					cmd = [100*x, 100*y, 40*rz]
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
