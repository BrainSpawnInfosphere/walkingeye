#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import numpy as np
# from math import sin, cos, acos, atan2, sqrt, pi
from math import radians as d2r
from math import degrees as r2d
# from tranforms import rot, T
from Interfaces import PCA9685
import logging
logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.ERROR)


class PWM(object):
	"""
	This handles low level pwm controller and timing
	"""
	maxAngle = 90.0  # servo max angle
	minAngle = -90.0
	pwm_max = 655  # Max pulse length out of 4096
	pwm_min = 130  # Min pulse length out of 4096
	pwm = PCA9685()

	def __init__(self, channel):
		"""
		"""
		# self.pwm = PCA9685()
		self.channel = channel
		# print('pwm channel', self.channel)
		self.logger = logging.getLogger(__name__)
		# self.logger.debug('pwm channel:', channel)  # nosetests doesn't like this????

	def set_freq(self, freq=60):
		self.pwm.set_pwm_freq(freq)

	def angleToPWM(self, angle):
		"""
		in:
			- angle: angle to convert to pwm pulse
			- mina: min servo angle
			- maxa: max servo angle
		out: pwm pulse size (0-4096)
		"""
		mina = self.minAngle
		maxa = self.maxAngle
		# servo_min = 150  # Min pulse length out of 4096
		# servo_max = 600  # Max pulse length out of 4096
		m = (self.pwm_max - self.pwm_min) / (maxa - mina)
		b = self.pwm_max - m * maxa
		pulse = m * angle + b  # y=m*x+b
		return int(pulse)


class Servo(PWM):
	"""
	Keeps info for servo and commands their movement.
	angles are in degrees
	servo commands are between -90 and 90 degrees, with 0 deg being center
	"""
	_angle = 0.0  # current angle
	# _angle0 = 0.0  # initial reset angle
	limitMinAngle = -90  # user difined limits
	limitMaxAngle = 90

	def __init__(self, channel, limits=None):
		"""
		pos0 [angle] - initial or neutral position
		limits [angle, angle] - [optional] set the angular limits of the servo to avoid collision
		"""
		PWM.__init__(self, channel)
		self._angle = 0.0

		if limits: self.setServoLimits(*limits)

	@property
	def angle(self):
		"""
		Returns the current servo angle
		"""
		# print('@property angle')
		return self._angle

	@angle.setter
	def angle(self, angle):
		"""
		Sets the servo angle and clamps it between [limitMinAngle, limitMaxAngle].
		It also commands the servo to move.
		"""
		self._angle = max(min(self.limitMaxAngle, angle), self.limitMinAngle)
		# self.move(self._angle)
		# print('@angle.setter: {} {}'.format(angle, self._angle))
		self.logger.debug('@angle.setter: {} {}'.format(angle, self._angle))
		pulse = self.angleToPWM(angle)
		self.pwm.set_pwm(self.channel, 0, pulse)

	def setServoLimits(self, minAngle, maxAngle):
		"""
		sets maximum and minimum achievable angles.
		in:
			minAngle - degrees
			maxAngle - degrees
		"""
		self.limitMaxAngle = maxAngle
		self.limitMinAngle = minAngle


def test_servo():
	s = Servo(10)
	s.angle = -90
	s.angle = 0
	s.angle = 90
	assert(s.angle == 90 and s.channel == 10)


if __name__ == "__main__":
	test_servo()
