
import math
import time
import numpy
from robot.tranforms import rotateAroundCenter, distance


class Gait(object):
	"""
	Base class
	"""
	def __init__(self, robot):
		self.lasttime = time.time()

	def height_at_progression(self, prog):
		pass

	def reset(self):
		pass

	def iterate(self, delta, deltaRot):
		pass

class CrawlGait(Gait):
	"""
	Slow stable, 3 legs on the ground at all times
	"""
	def __init__(self, robot):
		Gait.__init__(self, robot)

	def reset(self):
		pass

	def iterate(self, delta, deltaRot):
		pass

class TrotGait(Gait):
	"""
	faster unstable, 2 legs on the ground at all times
	"""
	z_profile = [0, 0, 0, 0, 0, 10, 40, 40, 30, 7]  # leg height x time

	z_points = len(z_profile)
	startTime = 0
	stepDistance = 5000
	lastDelta = numpy.array([0, 0, 0])
	currentDistance = 0

	def __init__(self, robot):
		Gait.__init__(self, robot)
		self.z_profile.append(self.z_profile[0])
		self.robot = robot
		self.legs = robot.legs
		self.group1 = [self.legs["front_left"], self.legs["rear_right"]]
		self.group2 = [self.legs["front_right"], self.legs["rear_left"]]

		# print self.robot.legs_resting_positions

	def height_at_progression(self, prog):
		"""
		returns the foot height at prog[0-1] of the foot movement overall
		"""
		index = math.floor(prog * self.z_points)
		diff = prog * self.z_points - index
		value = self.z_profile[int(index)] + (self.z_profile[int(index + 1)] - self.z_profile[int(index)]) * diff

		prog = (prog if prog <= 0.5 else 1 - prog)
		speed = -0.5 + (prog * 2)

		return value, speed

	def iterate(self, linear_speed, angular_speed):  # FIXME: 20160610 rename this to step
		"""
		This is really a step - do the calculation to move feet to next location
		"""
		rests = self.robot.legs_resting_positions
		rotationalDistance = distance(rests[0], rotateAroundCenter(rests[0], 'z', angular_speed[2]))  # calc the distance travelled by a leg from rest
		thisDistance = distance(linear_speed, linear_speed) + rotationalDistance
		# print thisDistance
		self.currentDistance = (self.currentDistance + thisDistance) % self.stepDistance

		# current feet height depends on distance (maybe shoudl depend on time? )
		step_progression = self.currentDistance / self.stepDistance
		step_progression_alternate = (step_progression + 0.5) % 1.0

		height_pair1, speed_direction_pair1 = self.height_at_progression(step_progression)
		height_pair2, speed_direction_pair2 = self.height_at_progression(step_progression_alternate)

		# print linear_speed, angular_speed

		self.move_leg_group(self.group1, height_pair1, speed_direction_pair1, linear_speed, angular_speed)
		self.move_leg_group(self.group2, height_pair2, speed_direction_pair2, linear_speed, angular_speed)

	def move_leg_group(self, group, height_pair, speed_direction_pair, linear_speed, angular_speed):
		"""
		this moves the opposite 2 legs, e.g., left-front and right-back
		"""
		for leg in group:
			angular_offset = rotateAroundCenter(leg.resting_position, 'z', angular_speed[2]) - leg.resting_position
			total_offset = angular_offset - linear_speed
			offset = speed_direction_pair * total_offset
			offset[2] = height_pair
			rotated_position = self.get_rotated_leg_resting_positions(leg, angular_speed)
			leg.move_to_pos(*(rotated_position + offset))

	def get_rotated_leg_resting_positions(self, leg, drot):
		rotx = rotateAroundCenter(leg.resting_position, "x", drot[0])
		return rotateAroundCenter(rotx, "y", drot[1])
