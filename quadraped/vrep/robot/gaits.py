
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
	z_profile = [0.5,1,1,0.5,0,0,0,0,0,0,0,0]  # 12 steps, normalized leg height

	def __init__(self, robot):
		Gait.__init__(self, robot)
		self.robot = robot
		self.legs = robot.legs
		self.current_step = 0
		self.legOffsets = [0,6,3,9]

	def eachLeg(self, index):
		z = self.z_profile[index]*10.0  # scale


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
		# index = math.floor(prog * self.z_points)
		# diff = prog * self.z_points - index  # this diff is just allowing addition of fractional height in the next line ... waste of time
		# value = self.z_profile[int(index)] + (self.z_profile[int(index + 1)] - self.z_profile[int(index)]) * diff
		#
		# prog = (prog if prog <= 0.5 else 1 - prog)
		# speed = -0.5 + (prog * 2)

		index = math.floor(prog * self.z_points)
		# diff = prog * self.z_points - index
		value = self.z_profile[int(index)]

		prog = (prog if prog <= 0.5 else 1.0 - prog)
		speed = -0.5 + (prog * 2.0)

		# print 'v, s:', value, speed

		return value, speed

	def iterate(self, linear_speed, angular_speed):  # FIXME: 20160610 rename this to step
		"""
		This is really a step - do the calculation to move feet to next location
		"""
		# print 'linear, angular speed:', linear_speed, angular_speed

		rests = self.robot.legs_resting_positions
		rotationalDistance = distance(rests[0], rotateAroundCenter(rests[0], 'z', angular_speed[2]))  # calc the distance travelled by a leg from rest
		thisDistance = distance(linear_speed, linear_speed) + rotationalDistance
		# print thisDistance
		self.stepDistance = 7.0
		# self.currentDistance = (self.currentDistance + thisDistance) % self.stepDistance
		self.currentDistance += 1.0
		self.currentDistance %= self.stepDistance

		# print 'current, this, rot dist:', self.currentDistance, thisDistance, rotationalDistance

		# current feet height depends on distance (maybe shoudl depend on time? )
		step_progression = self.currentDistance / self.stepDistance
		step_progression_alternate = (step_progression + 0.5) % 1.0

		# print 'step prog, alt:', step_progression, step_progression_alternate

		height_pair1, speed_direction_pair1 = self.height_at_progression(step_progression)
		# print 'height, speed dir:', height_pair1, speed_direction_pair1
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
			# total_offset = angular_offset - linear_speed
			total_offset = angular_offset + linear_speed

			print 'rest:', leg.resting_position

			# mag = 40.0
			# speed_direction_pair = (mag if speed_direction_pair >= 0.0 else -mag)

			# offset = speed_direction_pair * total_offset
			offset = speed_direction_pair * numpy.array(linear_speed)
			print 'offset', offset
			# offset[2] = height_pair

			# print 'speed dir:', speed_direction_pair
			# print 'angular off, lin speed:', angular_offset, linear_speed
			# print 'offset, total offset:', offset, total_offset

			# account for desired roll pitch of body?
			# rotated_position = self.get_rotated_leg_resting_positions(leg, angular_speed)
			# print 'rotated pos:', rotated_position
			# leg.move_to_pos(*(rotated_position + offset))
			# print offset
			# print 'rotated pos:', rotated_position
			leg.move_to_pos(*(leg.resting_position + 100.0*offset))

	def get_rotated_leg_resting_positions(self, leg, drot):
		rotx = rotateAroundCenter(leg.resting_position, "x", drot[0])
		return rotateAroundCenter(rotx, "y", drot[1])
