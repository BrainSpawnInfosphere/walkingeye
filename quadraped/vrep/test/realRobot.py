
from __future__ import print_function
from __future__ import division
import time
import math
import numpy
from BaseLeg import Leg
# from realRobot import Robot
from Servo import Servo

# since i do a lot of dev on Apple, this creates a fake interface
import platform
if platform.system().lower() == 'linux':
	# pip install Adafruit_Python_PCA9685
	from Adafruit_Python_PCA9685 import PCA9685
	# import Adafruit_MCP230xx as Ada  # if more i2c i/o needed
else:
	class PCA9685(object):
		def __init__(self):
			pass

		def set_pwm(self, a, b, c):
			# print('fake servo')
			pass


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
	femurLength = None
	tibiaLength = None
	legs = []
	servos = []

	def __init__(self, robotData):

		# setup PWM controller
		# -------------------------------------------------------------------
		self.pwm = PCA9685()

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
		self.servos = [  # why am i saving these? legs stores them too!
			# leg 1
			Servo(pin=0, rate=-RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			Servo(pin=1, rate=RATE, pos0=1500, limits=robotData['femurServoLimits']),
			Servo(pin=2, rate=RATE, pos0=1500, limits=robotData['tibiaServoLimits']),
			# leg 2
			Servo(pin=4, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			Servo(pin=5, rate=RATE, pos0=1500, limits=robotData['femurServoLimits']),
			Servo(pin=6, rate=-RATE, pos0=1500, limits=robotData['tibiaServoLimits']),
			# leg 3
			Servo(pin=8, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			Servo(pin=9, rate=RATE, pos0=1500, limits=robotData['femurServoLimits']),
			Servo(pin=10, rate=RATE, pos0=1500, limits=robotData['tibiaServoLimits']),
			# leg 4
			Servo(pin=12, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			Servo(pin=13, rate=RATE, pos0=1500, limits=robotData['femurServoLimits']),
			Servo(pin=14, rate=RATE, pos0=1500, limits=robotData['tibiaServoLimits'])
		]

		servos = self.servos

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

		# front left, front right, back right, back left
		legs_resting_positions = [
			(front + offset - cg_offet_x, left + offset, resting_heigth),
			(front + offset - cg_offet_x, right - offset, resting_heigth),
			(back - offset - cg_offet_x, right - offset, resting_heigth),
			(back - offset - cg_offet_x, left + offset, resting_heigth)
		]

		rests = numpy.array(legs_resting_positions)

		# create array of legs
		# -------------------------------------------------------------------
		lengths = {'femurLength': robotData['femurLength'], 'tibiaLength': robotData['tibiaLength']}
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
			Leg("front_left", (length / 2, width / 2, heigth), rests[0], lengths),
			Leg("front_right", (length / 2, -width / 2, heigth), rests[1], lengths),
			Leg("rear_right", (-length / 2, -width / 2, heigth), rests[2], lengths),
			Leg("rear_left", (-length / 2, width / 2, heigth), rests[3], lengths)
		]

	# def move_leg_to_point(self, leg, x, y, z):
	# 	"""
	# 	Attempts to move 'leg' foot to position [x, y, z]
	# 	in:
	# 		leg - array number
	# 		x,y,z - 3d position
	# 	"""
	# 	self.legs[leg].move_to_pos(x, y, z)
	# 	time.sleep(0.0005)

	def init(self):
		"""
		"boot" function, it runs before the main loop
		:return:
		"""
		for servo in self.servos:
			servo.reset()
			# time.sleep(0.1)
		time.sleep(3)

	# def load_legs(self):
	# 	raise NotImplementedError()

	def __del__(self):
		pass

	def moveLegsToAngles(self, angles):
		"""
		Move legs to an arbitrary set of angles
		in: ??
		out: ??
		"""
		raise NotImplementedError()

	# def disconnect(self):
	# 	"""
	# 	disconnects serial.
	# 	"""
	# 	pass

	def finish_iteration(self):
		pass

	def commandServos(self):
		"""
		Send servo positions to pwm controller over i2c
		"""
		def angleToPWM(angle, min, max):
			servo_min = 150  # Min pulse length out of 4096
			servo_max = 600  # Max pulse length out of 4096
			m = (servo_max - servo_min) / (max - min)
			b = servo_max - m * max
			pulse = m * angle + b  # y=mx+b
			return int(pulse)

		# i = 0
		# for servo in self.servos:
		# 	pulse = angleToPWM(servo.angle, servo.minAngle, servo.maxAngle)
		# 	self.pwm.set_pwm(i, 0, pulse)
		# 	i += 1
		i = 0
		for leg in self.legs:
			angles = leg.angles
			for j in range(0,4):
				pulse = angleToPWM(self.servos[i+j].angle, self.servos[i+j].minAngle, self.servos[i+j].maxAngle)
				self.pwm.set_pwm(i+j, 0, pulse)
			i += 4  # next block of servos
