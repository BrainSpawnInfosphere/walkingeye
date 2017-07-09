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
# from pyxl320 import DummySerial
from Servo import Servo
from pyxl320 import Packet
from pyxl320 import xl320
import time

# syncwrite is broken ... fix!


class Engine(object):
	"""
	change name to Hardware???

	This is the low level driver that can be executed w/o using pyGecko.
	"""
	def __init__(self, data={}):
		"""
		Sets up all 4 legs and servos. Also setups limits for angles and servo
		pulses.
		"""
		if 'serialPort' in data:
			try:
				ser = ServoSerial(data['serialPort'])
				print('Using servo serial port: {}'.format(data['serialPort']))

			except:
				print('bye ...')
				exit(1)
		else:
			print('Using dummy serial port!!!')
			ser = ServoSerial('test_port', fake=True)
			# raise Exception('No serial port given')

		ser.open()
		Servo.ser = ser  # set static serial port, not sure I like this

		if 'write' in data:
			method = data['write']
			if method == 'sync':
				Servo.syncServoWrite = True  # FIXME: this is broken
			elif method == 'bulk':
				Servo.bulkServoWrite = True

		# print('*** using sync write ***')

		self.legs = []
		for i in range(0, 4):  # 4 legs
			channel = i*3  # 3 servos per leg
			self.legs.append(
				Leg([channel+1, channel+2, channel+3])
			)

		self.stand()

	def __del__(self):
		"""
		Leg kills (reboots) all servos on exit.

		Eventually will put the robot in sit pose.
		"""
		self.sit()
		pkt = Packet.makeRebootPacket(xl320.XL320_BROADCAST_ADDR)
		Servo.ser.write(pkt)
		Servo.ser.write(pkt)
		time.sleep(1)
		print('Engine __del__')
		Servo.ser.close()  # close static serial port

	def sit(self):
		"""
		sequence to sit down nicely
		"""
		print('Engine::sit()')
		raw = (150, 270, 100)
		angles = self.legs[0].convertRawAngles(*raw)
		print('sit:', angles)
		for i in range(4):
			self.legs[i].moveFootAngles(*angles)
		# Servo.syncWrite(Servo.ser)  # FIXME: ugly
		self.legs[0].servos[0].write()
		time.sleep(1)

	def stand(self):
		"""
		sequence to stand up nicely
		"""
		print('Engine::stand()')
		raw = (150, 175, 172)
		angles = self.legs[0].convertRawAngles(*raw)
		print('stand:', angles)
		for i in range(4):
			self.legs[i].moveFootAngles(*angles)
		# Servo.syncWrite(Servo.ser)  # FIXME: ugly
		self.legs[0].servos[0].write()
		time.sleep(1)

	def getFoot0(self, i):
		return self.legs[i].foot0

	def moveFoot(self, i, pos):
		"""
		moveFoot -> moveFootPosition ?

		Moves the foot of leg i to a position (x,y,z)
		"""
		return self.legs[i].moveFoot(*pos)
