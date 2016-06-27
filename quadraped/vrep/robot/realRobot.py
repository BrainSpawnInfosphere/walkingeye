
from __future__ import print_function
from __future__ import division
import time
import math
import numpy
from realLeg import RealLeg
from BaseRobot import Robot

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

# from robot import robotData
# from robot.robotInterfaces.legInterfaces.realLeg import RealLeg
# from robot.robotInterfaces.realRobot.serialServoCommander import SerialComms
# from robot.robotInterfaces.genericRobot import Robot

# RATE = robotData.genericServoRate


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


class RealRobot(Robot):
	"""
	Class responsible for representing and controlling the real-life robot.
	"""
	# width = robotData.width
	# length = robotData.length
	# heigth = robotData.heigth

	def __init__(self, robotData):

		self.pwm = PCA9685()

		self.width = robotData['width']
		self.length = robotData['length']
		self.heigth = robotData['resting_heigth']

		width = self.width
		length = self.length
		heigth = self.heigth
		# self.serial = SerialComms()
		# print("created new RealRobot attached to:", self.serial)
		# serial = self.serial
		RATE = robotData['genericServoRate']
		self.servos = [
			# leg 1
			Servo(pin=2, rate=-RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			Servo(pin=3, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			Servo(pin=4, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			# leg 2
			Servo(pin=5, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			Servo(pin=6, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			Servo(pin=7, rate=-RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			# leg 3
			Servo(pin=8, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			Servo(pin=9, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			Servo(pin=10, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			# leg 4
			Servo(pin=11, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			Servo(pin=12, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits']),
			Servo(pin=13, rate=RATE, pos0=1500, limits=robotData['shoulderServoLimits'])
		]

		servos = self.servos

		totalDistance = robotData['femurLength'] + robotData['tibiaLength']
		front = length/2
		back = -length/2
		left = width/2
		right = -width/2
		offset = totalDistance/2

		resting_heigth = robotData['resting_heigth']

		cg_offet_x = robotData['cg_offet_x']

		legs_resting_positions = [(front+offset - cg_offet_x, left+offset, resting_heigth),
		                          (front+offset - cg_offet_x, right-offset, resting_heigth),
		                          (back-offset - cg_offet_x, right-offset, resting_heigth),
		                          (back-offset - cg_offet_x, left+offset, resting_heigth)]    ### front left, front right, back right, back left

		legs_resting_positions = numpy.array(legs_resting_positions)

		rests = legs_resting_positions
		lengths = {'femurLength': robotData['femurLength'], 'tibiaLength': robotData['tibiaLength']}
		self.legs = {
			"front_left": RealLeg("front_left", (length / 2, width / 2, heigth), servos[1], servos[0], servos[2], rests[0], lengths),
			"front_right": RealLeg("front_right", (length / 2, -width / 2, heigth), servos[3], servos[4], servos[5], rests[1], lengths),
			"rear_right": RealLeg("rear_right", (-length / 2, -width / 2, heigth), servos[6], servos[7], servos[8], rests[2], lengths),
			"rear_left": RealLeg("rear_left", (-length / 2, width / 2, heigth), servos[9], servos[10], servos[11], rests[3], lengths)}
		# self.feet = [False, False, False, False]

	# def read_feet(self):
	# 	"""
	# 	Queues sensor feet read, and return the last read values as a list
	# 	"""
	# 	self.serial.queue.put(lambda: self.serial.read_pins())
	# 	data = self.serial.input_pins
	# 	self.feet = [not ((data >> bit) & 1) for bit in range(4 - 1, -1, -1)]

	# def read_imu(self):
	# 	"""
	# 	Queues IMU read, and returns last read value from serial reader.
	# 	"""
	# 	self.serial.queue.put(lambda: self.serial.read_imu())
	# 	self.orientation = self.serial.imu
	# 	return self.serial.imu

	def move_leg_to_point(self, leg, x, y, z):
		"""
		Attempts to move 'leg' foot to position [x, y, z]
		in:
			leg - array number
			x,y,z - 3d position
		"""
		self.legs[leg].move_to_pos(x, y, z)
		time.sleep(0.0005)

	def init(self):
		"""
		"boot" function, it runs before the main loop
		:return:
		"""
		# self.serial.start()
		# for i in range(1000):
		for servo in self.servos:
			servo.reset()
			# time.sleep(0.1)
		time.sleep(3)

	# def load_legs(self):
	# 	raise NotImplementedError()

	def moveLegsToAngles(self, angles):
		"""
		Move legs to an arbitrary set of angles
		in: ??
		out: ??
		"""
		raise NotImplementedError()

	def disconnect(self):
		"""
		disconnects serial.
		"""
		# self.serial.running = False
		pass

	def finish_iteration(self):
		def angleToPWM(angle, min, max):
			servo_min = 150  # Min pulse length out of 4096
			servo_max = 600  # Max pulse length out of 4096
			m = (servo_max - servo_min) / (max - min)
			b = servo_max - m * max
			pulse = m * angle + b  # y=mx+b
			return int(pulse)

		i = 0
		for servo in self.servos:
			pulse = angleToPWM(servo.angle, servo.minAngle, servo.maxAngle)
			self.pwm.set_pwm(i, 0, pulse)
			i += 1
