#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from Leg import Leg
from pyxl320 import ServoSerial
from pyxl320 import DummySerial
from Servo import Servo


class RobotException(Exception):
	pass


class Engine(object):
	"""
	change name to Hardware???

	This is the low level driver that can be executed w/o using pyGecko.
	"""
	def __init__(self, data):
		"""
		Sets up all 4 legs and servos. Also setups limits for angles and servo
		pulses.
		"""
		# mp.Process.__init__(self)
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

	# def bulkWrite(self):
	# 	# self.legs[0].servos[0].bulkWrite()
	# 	Servo.bulkWrite()

	# def moveFootAngles(self, angles, leg=None):
	# 	"""
	# 	Sets servos of a leg, or all legs if no leg identified, to given angles.
	# 	"""
	# 	if leg is None:
	# 		for i in range(0, 4):
	# 			pts = self.legs[i].fk(*angles)  # allows angles out of range
	# 			self.legs[i].move(*pts)
	# 	else:
	# 		pts = self.legs[leg].fk(*angles)  # allows angles out of range
	# 		self.legs[leg].move(*pts)
