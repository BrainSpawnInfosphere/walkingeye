#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import numpy as np
from math import sin, cos, acos, atan2, sqrt, pi
from math import radians as d2r
from math import degrees as r2d
from tranforms import rot, T
from Interfaces import PCA9685


class PWM(object):
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
		print('pwm channel', self.channel)

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

	# def move(self, angle):
	# 	"""
	# 	pulse: 0-4095
	# 	"""
	# 	# pulse = max(0, min(4095, pulse))
	# 	pulse = self.angleToPWM(angle)
	# 	self.pwm.set_pwm(self.channel, 0, pulse)


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
# 		print('@property angle')
		return self._angle

	@angle.setter
	def angle(self, angle):
		"""
		Sets the servo angle and clamps it between [limitMinAngle, limitMaxAngle].
		It also commands the servo to move.
		"""
		self._angle = max(min(self.limitMaxAngle, angle), self.limitMinAngle)
		# self.move(self._angle)
		print('@angle.setter: {} {}'.format(angle, self._angle))
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


class Leg(object):
	"""
	"""
	servos = []
	footPosition = [0.0, 0.0, 0.0]
	angles = [0.0, 0.0, 0.0]

	def __init__(self, lengths, channels, limits=[None, None, None]):
		"""
		"""
		if not len(channels) == 3: raise Exception('len(channels) = 3')

		self.coxaLength = lengths['coxaLength']
		self.tibiaLength = lengths['tibiaLength']
		self.femurLength = lengths['femurLength']

		self.foot0 = self.fk(0, 0, -90)

		# Create each servo and move it to the initial position
		# servo arrange: coxa femur tibia
		for i in range(0, 3):
			print('leg channels', channels)
			self.servos.append(Servo(channels[i], limits[i]))
			self.servos[i].angle = self.foot0[i]

	def fk(self, a, b, g):
		"""
		"""
		Lc = self.coxaLength
		Lf = self.femurLength
		Lt = self.tibiaLength

		phi = a
		theta2 = b
		theta3 = g

		params = [
			# a_ij alpha_ij  S_j  theta_j
			[Lc,   d2r(90),   0,   d2r(theta2)],  # frame 12
			[Lf,    d2r(0),   0,   d2r(theta3)]   # 23
		]

		r = T(params, d2r(phi))
		foot = r.dot(np.array([Lt, 0, 0, 1]))  # ok [ 37.4766594  37.4766594 -63. 1.]

		return foot[0:-1]  # DH return vector size 4, only grabe first 3 (x,y,z)

	def ik(self, x, y, z):
		"""
		Calculates the inverse kinematics from a given foot coordinate (x,y,z)[mm]
		and returns the joint angles
		"""
		Lc = self.coxaLength
		Lf = self.femurLength
		Lt = self.tibiaLength
		a = atan2(y, x)
		f = sqrt(x**2 + y**2) - Lc
		b1 = atan2(z, f)
		d = sqrt(f**2 + z**2)
		b2 = acos((Lf**2 + d**2 - Lt**2) / (2.0 * Lf * d))
		b = b1 + b2
		g = acos((Lf**2 + Lt**2 - d**2) / (2.0 * Lf * Lt))

		g -= pi  # fix to align fk and ik

		# print('ik angles:', r2d(a), r2d(b), r2d(g))

		return a, b, g  # coxaAngle, femurAngle, tibiaAngle

	def move(self, x, y, z):
		"""
		Attempts to move it's foot to coordinates [x,y,z]
		"""
		try:
			angles = self.ik(x, y, z)  # inverse kinematics
			print('move:', angles)
			for i, servo in enumerate(self.servos):
				servo.angle = angles[i]

		except Exception as e:
			print (e)
			raise

	def reset(self):
		self.angles = self.resting_position

def test_servo():
	s = Servo(10)
	s.angle = -90
	s.angle = 0
	s.angle = 90
	assert(s.angle == 90 and s.channel == 10)

if __name__ == "__main__":
	length = {
		'coxaLength': 10,
		'tibiaLength': 50,
		'femurLength': 100
	}

	channels = [0, 1, 2]
	limits = [[-45, 45], [-45, 45], [-90, 0]]

	leg = Leg(length, channels, limits)
	angles = [-45, 0, 100]
	print('angles:', angles)
	pts = leg.fk(*angles)
	print('pts:', pts)
	a, b, c = leg.ik(*pts)
	print('angles:', r2d(a), r2d(b), r2d(c))
	leg.move(*pts)
