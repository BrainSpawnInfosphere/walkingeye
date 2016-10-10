#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import logging
from pyxl320 import Packet, xl320
# from pyxl320 import ServoSerial
# from pyxl320 import DummySerial
# logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# FIXME 2016-10-09 move RC and Robotis servo code to pygecko?
# FIXME 2016-10-09 clean up global serial port
# global serial
# # ser = ServoSerial('/dev/tty.usbserial-A5004Flb')
# ser = DummySerial('test_port')
# ser.open()


# def fix(lb, hb):
# 	return (hb << 8) + lb


# class Base(object):
# 	def __init__(self, dummy=False):
# 		self.ser = None
# 		if dummy:
# 			self.ser = DummySerial('test_port')
# 		else:
# 			self.ser = ServoSerial('/dev/tty.usbserial-A5004Flb')


class Servo(object):
	"""
	Keeps info for servo and commands their movement.
	angles are in degrees

	            0
	-150 ------ + ------- 150  kinematics (servo_k)
	           150
	   0 ------ + ------- 300  real servo (servo_r)

	servo_k commands are between -150 and 150 degrees, with 0 deg being center

	servo to kinematics: servo_r = servo_k + 150
	kinematics to servo: servo_k = servo_r - 150
	"""
	_angle = 0.0  # current angle

	def __init__(self, ID, serialObj, limits=None):
		"""
		limits [angle, angle] - [optional] set the angular limits of the servo to avoid collision
		"""
		self.ID = ID
		self.ser = serialObj

		# get current location
		pkt = Packet.makeReadPacket(self.ID, xl320.XL320_PRESENT_POSITION, [2])
		self.ser.write(pkt)
		ret = self.ser.read()

		# servos are centered at 150 deg
		# angle = fix(*ret[6:8])  # FIXME
		# angle -= 150
		# self._angle = angle

		if limits: self.setServoLimits(*limits)
		else: self.setServoLimits(0.0, 300.0)

	@property
	def angle(self):
		"""
		Returns the current servo angle
		"""
		return self._angle

	@angle.setter
	def angle(self, angle):
		"""
		Sets the servo angle and clamps it between [limitMinAngle, limitMaxAngle].
		It also commands the servo to move.
		"""
		if self.minAngle < angle > self.maxAngle:
			raise Exception('@angle.setter')

		if self._angle != angle:
			# servos are centered at 150 deg
			angle += 150.0
			self._angle = angle
			pkt = Packet.makeServoPacket(self.ID, angle)
			self.ser.sendPkt(pkt)

	def setServoLimits(self, minAngle, maxAngle):
		"""
		sets maximum and minimum achievable angles. Remeber, the limits have to
		be within the servo range of [0, 180] ... anything more of less won't
		work unless your change setServoRangleAngle() to something other than
		0 - 180.

		in:
			minAngle - degrees
			maxAngle - degrees
		"""
		self.minAngle = minAngle
		self.maxAngle = maxAngle

		# # pktmax, pktmin = Packet.makeServoLimits(self.ID, maxAngle, minAngle)
		# angle = int(maxAngle/300.0*1023)
		# pkt = Packet.makeWritePacket(self.ID, xl320.XL320_CCW_ANGLE_LIMIT, Packet.le(angle))
		# ser.write(pkt)
		# # # ser.read()
		# angle = int(minAngle/300.0*1023)
		# pkt = Packet.makeWritePacket(self.ID, xl320.XL320_CW_ANGLE_LIMIT, Packet.le(angle))
		# ser.write(pkt)
		# # ser.read()

		pkt = Packet.makeServoMinLimitPacket(self.ID, minAngle)
		self.ser.sendPkt(pkt)
		pkt = Packet.makeServoMaxLimitPacket(self.ID, maxAngle)
		self.ser.sendPkt(pkt)

	def stop(self):
		pass

	@staticmethod
	def all_stop():  # this serves no purpose ... remove in RC also
		pass


if __name__ == "__main__":
	# cmd_servo()
	# swing_servo()
	# test_limits()
	# checks()
	print('Hello space cowboy!')
