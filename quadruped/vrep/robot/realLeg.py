
from __future__ import print_function
from __future__ import division

from BaseLeg import Leg
# from math import pi


class RealLeg(Leg):
	"""
	name - name of leg
	position - location of leg in body frame
	xServo - the servos that make up the leg
	resting_position - initial/neutral position of leg
	lengths - lengths of leg segments
	"""
	def __init__(self, name, position, panServo, femurServo, tibiaServo, resting_positions, lengths):
		# super(RealLeg, self).__init__(name, position, resting_positions)
		Leg.__init__(self, name, position, resting_positions, lengths)
		self.position = position
		self.panServo = panServo
		self.tibiaServo = tibiaServo
		self.femurServo = femurServo

	def moveToAngle(self, shoulderAngle, femurAngle, tibiaAngle):
		"""
		Moves joints to specified angles
		"""
		# self.check_limits(shoulderAngle, femurAngle, tibiaAngle)  # done in servo ... why here?
		self.panServo.moveToAngle(shoulderAngle)
		self.femurServo.moveToAngle(femurAngle)
		self.tibiaServo.moveToAngle(tibiaAngle)

	def reset(self):
		self.panServo.reset()
		self.tibiaServo.reset()
		self.femurServo.reset()
