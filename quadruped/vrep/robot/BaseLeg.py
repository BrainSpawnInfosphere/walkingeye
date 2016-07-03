from __future__ import print_function
from __future__ import division
import numpy
from math import *
# import Servo
# from math import radians as d2r
# from math import degrees as r2d


class Leg(object):
	"""
	This should be an abstract leg, it's responsible for moving and locating each leg.
	"""

	# panServo = None
	# tibiaServo = None
	# femurServo = None
	position = None
	orientation = None
	ydirection = 1
	footPosition = [0.0, 0.0, 0.0]
	angles = [0.0, 0.0, 0.0]

	# def __init__(self, name, position, panServo, femurServo, tibiaServo, resting_position, lengths):
	def __init__(self, name, position, resting_position, lengths):
		"""
		:param name: leg name, used to get it's pointing difection in some implementations
		:param position: body-relative leg position
		:param resting_position: feet resting position
		:return:
		"""
		self.name = name
		self.position = position
		self.resting_position = resting_position
		self.tibiaLength = lengths['tibiaLength']
		self.femurLength = lengths['femurLength']
		self.position = position
		# self.panServo = panServo
		# self.tibiaServo = tibiaServo
		# self.femurServo = femurServo

		if "right" in self.name:
			self.ydirection = -1

	def ik_to(self, x0, y0, z0):
		"""
		Calculates each joint angle to get the leg to coordinates x0,y0,z0
		:return: the correct angles.
		"""

		# math adapted from http://arduin0.blogspot.fi/2012/01/inverse-kinematics-ik-implementation.html
		# after I thought I had problems with my own
		dx = x0 - self.position[0]
		dy = y0 - self.position[1]
		dz = z0 - self.position[2]
		COXA_LENGTH = 20
		FEMUR_LENGTH = self.femurLength
		TIBIA_LENGTH = self.tibiaLength

		x, y, z = dy * self.ydirection, -dz, -dx * self.ydirection

		# tibiaAngle = acos(((sqrt(
		# 	((sqrt(x ** 2 + z ** 2)) - COXA_LENGTH) ** 2 + y ** 2)) ** 2 - TIBIA_LENGTH ** 2 - FEMUR_LENGTH ** 2) / (-2 * FEMUR_LENGTH * TIBIA_LENGTH)) * 180 / pi
		# coxaAngle = atan2(z, x) * 180 / pi
		# femurAngle = (((atan(((sqrt(x ** 2 + z ** 2)) - COXA_LENGTH) / y)) + (acos((
		# 	TIBIA_LENGTH ** 2 - FEMUR_LENGTH ** 2 - (
		# 	sqrt(((sqrt(
		# 		x ** 2 + z ** 2)) - COXA_LENGTH) ** 2 + y ** 2)) ** 2) / (
		# 		-2 * FEMUR_LENGTH * (sqrt(((sqrt(
		# 			x ** 2 + z ** 2)) - COXA_LENGTH) ** 2 + y ** 2)))))) * 180 / pi) - 90
		tibiaAngle = acos(((sqrt(
			((sqrt(x ** 2.0 + z ** 2.0)) - COXA_LENGTH) ** 2.0 + y ** 2.0)) ** 2.0 - TIBIA_LENGTH ** 2.0 - FEMUR_LENGTH ** 2.0) / (-2.0 * FEMUR_LENGTH * TIBIA_LENGTH))
		coxaAngle = atan2(z, x)
		femurAngle = (((atan(((sqrt(x ** 2.0 + z ** 2.0)) - COXA_LENGTH) / y)) + (acos((
			TIBIA_LENGTH ** 2.0 - FEMUR_LENGTH ** 2.0 - (
			sqrt(((sqrt(
				x ** 2.0 + z ** 2.0)) - COXA_LENGTH) ** 2.0 + y ** 2.0)) ** 2.0) / (
				-2.0 * FEMUR_LENGTH * (sqrt(((sqrt(
					x ** 2.0 + z ** 2.0)) - COXA_LENGTH) ** 2.0 + y ** 2.0))))))) - pi/2.0
		# print 'cft:', coxaAngle, femurAngle, tibiaAngle
		return coxaAngle, femurAngle, tibiaAngle - pi/2.0

	# change def setFoot(self, x, y, z):
	def move_to_pos(self, x, y, z):
		"""
		Attempts to move it's foot to coordinates [x,y,z]
		"""
		try:
			angles = self.ik_to(x, y, z)  # inverse kinematics
			# print "ik result:", angles
			# self.moveToAngle(*angles)  # displays in vrep when virtual

			self.footPosition = numpy.array([x, y, z])
			self.angles = angles
		except Exception as e:
			print (e)
			raise

	# def moveToAngle(self, shoulderAngle, femurAngle, tibiaAngle):
	# 	"""
	# 	Moves joints to specified angles
	# 	"""
	# 	# self.check_limits(shoulderAngle, femurAngle, tibiaAngle)  # done in servo ... why here?
	# 	self.panServo.moveToAngle(shoulderAngle)
	# 	self.femurServo.moveToAngle(femurAngle)
	# 	self.tibiaServo.moveToAngle(tibiaAngle)

	def reset(self):
		self.angles = [0.0, 0.0, 0.0]
		# self.panServo.reset()
		# self.tibiaServo.reset()
		# self.femurServo.reset()
