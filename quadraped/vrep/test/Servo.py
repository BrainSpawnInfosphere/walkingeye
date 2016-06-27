#!/usr/bin env python
from __future__ import print_function
from __future__ import division
import math


def clamp(n, minn, maxn):
	"""
	Returns n constrained between minn and maxm
	"""
	return max(min(maxn, n), minn)


class Servo(object):
	"""
	Class responsible for representing and controlling a real life servo.
	"""
	def __init__(self, pin, pos0, rate, limits=None):
		"""
		pin - pin number the servo is attached too
		pos0 - initial or neutral position
		rate - ???
		limits - [optional] set the angular limits of the servo
		"""
		self.pos0 = pos0
		self.rate = rate
		self.pin = pin

		if limits:
			self.setServoLimits(*limits)
		else:
			self.maxAngle = 180
			self.minAngle = -180

		# self.serial = serial
		self.angle = 0

	def setServoLimits(self, minAngle, maxAngle):
		"""
		sets maximum and minimum achievable angles.
		in:
			minAngle - degrees
			maxAngle - degrees
		"""
		self.maxAngle = maxAngle
		self.minAngle = minAngle

	def reset(self):
		"""
		Move servo to initial/neutral position
		in: None
		out: None
		"""
		self.angle = self.pos0

	def getServoAngle(self):
		"""
		Return the current commanded servo angle
		in: None
		out: servo angle [degrees]
		"""
		return self.angle

	def moveToAngle(self, angle):
		"""
		Moves the sevo to desired angle
		in: angle [radians]
		out: None
		"""
		angle = math.degrees(angle)

		# clamp to limits
		newAngle = clamp(angle, self.minAngle, self.maxAngle)

		if newAngle != self.angle:
			self.angle = newAngle
			# pos = int(self.pos0 + newAngle * self.rate)  # not sure what this does?
			# self.serial.queue.put(lambda: self.serial.move_servo_to(self.pin, pos))
			# send i2c command
