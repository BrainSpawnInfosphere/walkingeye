
from __future__ import print_function
from __future__ import division
import time
# import math
import numpy
from BaseLeg import Leg
# from realRobot import Robot
# from Servo import Servo
from Interfaces import PCA9685


class Servo(object):
	"""
	Keeps info for servo. This only holds angle info and all angles are in
	degrees.
	"""
	_angle = 0.0
	_pos0 = 0.0
	maxAngle = 90.0
	minAngle = -90.0

	def __init__(self, pos0=0.0, limits=None):
		"""
		pos0 [angle] - initial or neutral position
		limits [angle, angle] - [optional] set the angular limits of the servo to avoid collision
		"""
		self.pos0 = pos0
		self.angle = pos0

		if limits: self.setServoLimits(*limits)

	@property
	def angle(self):
# 		print('@property angle')
		return self._angle

	@angle.setter
	def angle(self, angle):
		"""
		Sets the servo angle and clamps it between [minAngle, maxAngle]
		"""
		self._angle = max(min(self.maxAngle, angle), self.minAngle)
# 		print('@angle.setter: {} {}'.format(angle, self._angle))

	@property
	def pos0(self):
# 		print('@property pos0')
		return self._pos0

	@angle.setter
	def pos0(self, angle):
		"""
		Sets the servo initial angle and clamps it between [minAngle, maxAngle]
		"""
		self._pos0 = max(min(self.maxAngle, angle), self.minAngle)
# 		print('@pos0.setter: {} {}'.format(angle, self._angle))

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
		self._angle = self._pos0


class ServoController(object):
	"""
	A controller that talks to the i2c servo controller. Normal RC servos operate between
	max CCW (1.0 msec) to max CW (2.0 msec) in which these two positions should be ~180
	degrees apart. However, every servo is a little different with most servos having
	>180 degrees of motion.


	Tried to optimize pwm params for TG9e servos.
	TG9e = [130, 655] -> [1ms, 2ms] and appears to be ~190 degrees
	"""
	servos = []

	# these are used to convert an angle [degrees] into a pulse
	pwm_max = 655  # Max pulse length out of 4096
	pwm_min = 130  # Min pulse length out of 4096
	minAngle = -90  # not sure the right way to do this!
	maxAngle = 90

	def __init__(self, freq=60):
		self.pwm = PCA9685()
		self.pwm.set_pwm_freq(freq)
		for i in range(0, 16): self.servos.append(Servo())

	# def moveAllServos(self, angle=None):
	# 	for i, servo in enumerate(self.servos):
	# 		if angle is None:
	# 			angle = servo.angle
	# 		pulse = self.angleToPWM(angle, servo.minAngle, servo.maxAngle)
	# 		self.pwm.set_pwm(i, 0, pulse)

	def moveServo(self, i, angle=None):
		servo = self.servos[i]
		if angle: servo.angle = angle  # ensure limits are ok
		pulse = self.angleToPWM(servo.angle)
		self.pwm.set_pwm(i, 0, pulse)

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

	def allStop(self):  # FIXME: 20160702 can i stop individual servos too?
		self.pwm.set_all_pwm(0, 0x1000)

	def resetAll(self):
		for servo in self.servos:
			servo.reset()

	# def checkPwmRange(self, channel):
	# 	self.allStop()
	# 	for i in range(0, 700, 10):
	# 		print('pos: {}'.format(i))
	# 		self.pwm.set_pwm(channel, 0, i)
	# 		time.sleep(1)
	# 		# towerpro 100-660
	# 		# tg9e 130-650
	# 	self.allStop()

############################################################


class QuadrupedRobot(object):
	"""
	Class responsible for representing and controlling the real-life robot. It
	also holds:
	- pwm controller interface
	- servo parameters
	- leg/feet
	"""
	width = None
	length = None
	heigth = None
	pwm = None
	coxaLength = None
	femurLength = None
	tibiaLength = None
	legs = []
	servos = []

	def __init__(self, robotData):

		# setup PWM controller
		# -------------------------------------------------------------------
		# self.pwm = PCA9685()
		self.servoCtrl = ServoController()

		# get physical size
		# -------------------------------------------------------------------
		self.width = robotData['width']
		self.length = robotData['length']
		self.heigth = robotData['resting_heigth']
		self.femurLength = robotData['femurLength']
		self.tibiaLength = robotData['tibiaLength']

		# setup leg servos
		# -------------------------------------------------------------------
		RATE = robotData['genericServoRate']
		# self.servos = [  # why am i saving these? legs stores them too!
		# 	# leg 1
		# 	Servo(pin=0, rate=-RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
		# 	Servo(pin=1, rate=RATE, pos0=1500, limits=robotData['femurServoLimits']),
		# 	Servo(pin=2, rate=RATE, pos0=1500, limits=robotData['tibiaServoLimits']),
		# 	# leg 2
		# 	Servo(pin=4, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
		# 	Servo(pin=5, rate=RATE, pos0=1500, limits=robotData['femurServoLimits']),
		# 	Servo(pin=6, rate=-RATE, pos0=1500, limits=robotData['tibiaServoLimits']),
		# 	# leg 3
		# 	Servo(pin=8, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
		# 	Servo(pin=9, rate=RATE, pos0=1500, limits=robotData['femurServoLimits']),
		# 	Servo(pin=10, rate=RATE, pos0=1500, limits=robotData['tibiaServoLimits']),
		# 	# leg 4
		# 	Servo(pin=12, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
		# 	Servo(pin=13, rate=RATE, pos0=1500, limits=robotData['femurServoLimits']),
		# 	Servo(pin=14, rate=RATE, pos0=1500, limits=robotData['tibiaServoLimits'])
		# ]
		# servos = [  # why am i saving these? legs stores them too!
		# 	# leg 1
		# 	Servo(pos0=0.0, limits=robotData['shoulderServoLimits']),
		# 	Servo(pos0=0.0, limits=robotData['femurServoLimits']),
		# 	Servo(pos0=0.0, limits=robotData['tibiaServoLimits']),
		# 	# leg 2
		# 	Servo(pos0=0.0, limits=robotData['shoulderServoLimits']),
		# 	Servo(pos0=0.0, limits=robotData['femurServoLimits']),
		# 	Servo(pos0=0.0, limits=robotData['tibiaServoLimits']),
		# 	# leg 3
		# 	Servo(pos0=0.0, limits=robotData['shoulderServoLimits']),
		# 	Servo(pos0=0.0, limits=robotData['femurServoLimits']),
		# 	Servo(pos0=0.0, limits=robotData['tibiaServoLimits']),
		# 	# leg 4
		# 	Servo(pos0=0.0, limits=robotData['shoulderServoLimits']),
		# 	Servo(pos0=0.0, limits=robotData['femurServoLimits']),
		# 	Servo(pos0=0.0, limits=robotData['tibiaServoLimits'])
		# ]

		for i in range(0,16,4):
			self.servoCtrl.servos[i].setServoLimits(*robotData['shoulderServoLimits'])
			self.servoCtrl.servos[i+1].setServoLimits(*robotData['femurServoLimits'])
			self.servoCtrl.servos[i+2].setServoLimits(*robotData['tibiaServoLimits'])

		# servos = self.servos

		# calculate initial leg positions
		# -------------------------------------------------------------------
		width = self.width
		length = self.length
		heigth = self.heigth
		totalDistance = robotData['femurLength'] + robotData['tibiaLength']
		front = length / 2
		back = -length / 2
		left = width / 2
		right = -width / 2
		offset = totalDistance / 2

		resting_heigth = robotData['resting_heigth']

		cg_offet_x = robotData['cg_offet_x']

		p = (37.4766594,  37.4766594, -63.)

		# front left, front right, back right, back left
		# legs_resting_positions = [
		# 	(front + offset - cg_offet_x, left + offset, resting_heigth),
		# 	(front + offset - cg_offet_x, right - offset, resting_heigth),
		# 	(back - offset - cg_offet_x, right - offset, resting_heigth),
		# 	(back - offset - cg_offet_x, left + offset, resting_heigth)
		# ]
		legs_resting_positions = [p,p,p,p]

		# print('leg neutral:', legs_resting_positions)

		rests = numpy.array(legs_resting_positions)

		# create array of legs
		# -------------------------------------------------------------------
		lengths = {
			'coxaLength': robotData['coxaLength'],
			'femurLength': robotData['femurLength'],
			'tibiaLength': robotData['tibiaLength']
		}
		# self.legs = {
		# 	"front_left": RealLeg("front_left", (length / 2, width / 2, heigth), servos[1], servos[0], servos[2], rests[0], lengths),
		# 	"front_right": RealLeg("front_right", (length / 2, -width / 2, heigth), servos[3], servos[4], servos[5], rests[1], lengths),
		# 	"rear_right": RealLeg("rear_right", (-length / 2, -width / 2, heigth), servos[6], servos[7], servos[8], rests[2], lengths),
		# 	"rear_left": RealLeg("rear_left", (-length / 2, width / 2, heigth), servos[9], servos[10], servos[11], rests[3], lengths)
		# }
		# self.legs = [ # what is the value of naming them? use a number if anything?
		# 	Leg("front_left", (length / 2, width / 2, heigth), servos[0], servos[1], servos[2], rests[0], lengths),
		# 	Leg("front_right", (length / 2, -width / 2, heigth), servos[4], servos[5], servos[6], rests[1], lengths),
		# 	Leg("rear_right", (-length / 2, -width / 2, heigth), servos[8], servos[9], servos[10], rests[2], lengths),
		# 	Leg("rear_left", (-length / 2, width / 2, heigth), servos[12], servos[13], servos[14], rests[3], lengths)
		# ]
		self.legs = [
			Leg("front_left", (length / 2, width / 2, heigth), lengths),
			Leg("front_right", (length / 2, -width / 2, heigth), lengths),
			Leg("rear_right", (-length / 2, -width / 2, heigth), lengths),
			Leg("rear_left", (-length / 2, width / 2, heigth), lengths)
		]

		self.legs[0].set_resting_pos(45, 0, -90)
		self.legs[1].set_resting_pos(45, 0, -90)
		self.legs[2].set_resting_pos(45, 0, -90)
		self.legs[3].set_resting_pos(45, 0, -90)

	def init(self):
		"""
		"boot" function, it runs before the main loop
		:return:
		"""
		# for servo in self.servos:
		# 	servo.reset()
			# time.sleep(0.1)
		self.servoCtrl.resetAll()
		time.sleep(3)

	def __del__(self):
		pass

	def moveLegsToAngles(self, angles):
		"""
		Move legs to an arbitrary set of angles
		in: ??
		out: ??
		"""
		raise NotImplementedError()

	def commandServos(self):
		"""
		Send servo positions to pwm controller over i2c
		"""
		# def angleToPWM(angle, min, max):
		# 	servo_min = 150  # Min pulse length out of 4096
		# 	servo_max = 600  # Max pulse length out of 4096
		# 	m = (servo_max - servo_min) / (max - min)
		# 	b = servo_max - m * max
		# 	pulse = m * angle + b  # y=mx+b
		# 	return int(pulse)

		# i = 0
		# for servo in self.servos:
		# 	pulse = angleToPWM(servo.angle, servo.minAngle, servo.maxAngle)
		# 	self.pwm.set_pwm(i, 0, pulse)
		# 	i += 1
		# i = 0
		# for leg in self.legs:
		# 	angles = leg.angles
		# 	for j in range(0,4):
		# 		pulse = angleToPWM(self.servos[i+j].angle, self.servos[i+j].minAngle, self.servos[i+j].maxAngle)
		# 		self.pwm.set_pwm(i+j, 0, pulse)
		# 	i += 4  # next block of servos

		for i, leg in enumerate(self.legs):
			a, b, c = leg.angles
			self.servoCtrl.moveServo(4*i, a)
			self.servoCtrl.moveServo(4*i+1, b)
			self.servoCtrl.moveServo(4*i+2, c)
