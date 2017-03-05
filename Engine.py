#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from Leg import Leg
import multiprocessing as mp
# import time
# import numpy as np
# import logging
# from math import cos, sin, sqrt, pi
# from math import radians as d2r
from pyxl320 import ServoSerial
from pyxl320 import DummySerial
from Servo import Servo


class RobotException(Exception):
	pass


"""
Quadruped:
- Engine({serial})
- I2C()
- IR()
- movement_states['walk', 'climb', 'animate', 'sit', 'stand']
	- these are used to call movements[] functions using command()
- movements[]
	- Gait:
		- command(x, func_move_foot) - moves all feet through 1 gait cycle (12 steps)
		- eachLeg(x,y,z)
	- Pose:
		- command(func_move_foot) - sends all feet through an animation sequence to final position
		- eachLeg(x,y,z)

Engine(): - handles movement hardware
- legs[4]
	- servos[3]
		- angle
		- setServoLimits()
		- bulkWrite() - change to sync
	- coxa, femur, tibia
	- fk()
	- ik()
	- moveFoot(x,y,z)
	- moveFootAngle(a,b,c)
- moveFoot(x,y,z) - gaits need a function to call
"""


class Engine(mp.Process):
	"""
	change name to Hardware???

	This is the low level driver that can be executed w/o using pyGecko.
	"""
	def __init__(self, data):
		"""
		Sets up all 4 legs and servos. Also setups limits for angles and servo
		pulses.
		"""
		mp.Process.__init__(self)
		if 'serialPort' in data:
			print('Using servo serial port: {}'.format(data['serialPort']))
			ser = ServoSerial(data['serialPort'])
		else:
			print('Using dummy serial port!!!')
			ser = DummySerial('test_port')

		ser.open()
		Servo.ser = ser  # set static serial port

		# if 'legLengths' not in data or 'legAngleLimits' not in data:
		# 	raise RobotException('Quadruped json data missing required keys')
		#
		# if 'legOffset' not in data:
		# 	raise RobotException('Quadruped json data missing required keys')

		self.legs = []
		for i in range(0, 4):  # 4 legs
			channel = i*3  # 3 servos per leg
			self.legs.append(
				# Leg(
				# 	data['legLengths'],
				# 	[channel+1, channel+2, channel+3],  # servos numbered 1-12
				# 	self.ser,
				# 	data['legAngleLimits'],
				# 	data['legOffset']
				# )
				Leg([channel+1, channel+2, channel+3])
			)

	def __del__(self):
		"""
		Leg kills all servos on exit
		"""
		# self.sit()
		pass

	# def sit(self):
	# 	"""
	# 	sequence to sit down nicely
	# 	"""
	# 	pass
	#
	# def stand(self):
	# 	"""
	# 	sequence to stand up nicely
	# 	"""
	# 	pass

	def getFoot0(self, i):
		return self.legs[i].foot0

	def moveFoot(self, i, pos):
		"""
		moveFoot -> moveFootPosition ?

		Moves the foot of leg i to a position (x,y,z)
		"""
		return self.legs[i].moveFoot(*pos)

	def bulkWrite(self):
		# self.legs[0].servos[0].bulkWrite()
		Servo.bulkWrite()

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
