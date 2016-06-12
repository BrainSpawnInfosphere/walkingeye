
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
	# [0, 0, 0, 0, 0, 10, 40, 40, 30, 7]
	# z_profile = [0.5,1,1,0.5,0,0,0,0,0,0,0,0]  # 12 steps, normalized leg height
	z_profile = [0,0,0,0,0,0,0,0,0,0.5,1,0.5]  # 12 steps, normalized leg height

	def __init__(self, robot):
		Gait.__init__(self, robot)
		self.robot = robot
		self.legs = [
			robot.legs["front_left"],   # 0
			robot.legs["front_right"],  # 1
			robot.legs["rear_right"],   # 2
			robot.legs["rear_left"]     # 3
		]
		self.current_step = 0
		self.legOffsets = [0,6,3,9]
		self.i = 0

		self.reset()

	def something(self, prog):
		"""
		Returns the normalized 1-D foot position for a 75% duty cycle
		|                   *
		|             *       *
		| *                      *
		+-------------------+----+-
		0                  .75  1.0
		Progress (step/gait_length)

		todo - just turn this into a lookup table ... why calculate it?
		"""
		if prog < 0.0 or prog > 1.0:
			Exception('prog too high: {}'.format(prog))
		speed = 0.0
		if prog <= 0.75: speed = 4.0/3.0*prog-0.5
		else: speed = -4.0*(prog-0.75)+0.5
		return speed

	def eachLeg(self, leg, index, delta, deltaRot):
		legnum = 3
		rest = self.legs[leg].resting_position

		indexmod = (index + self.legOffsets[leg]) % len(self.z_profile)
		z = self.z_profile[indexmod] * 40.0  # scale ???

		# if leg == 2: print 'index, indexmod, z', index, indexmod, z
		rotMove = rotateAroundCenter(rest, 'z', deltaRot[2]) - rest

		# how far through the gait are we?
		prog = float(indexmod)/float(len(self.z_profile))
		scale = 0.50*self.something(prog)
		move = scale * (numpy.array(delta) + rotMove)
		# move = rotateAroundCenter(scale * numpy.array(delta), 'z', deltaRot[2])

		move[2] = z
		newpos = self.legs[leg].resting_position + move
		# if leg == 2: print 'prog, scale', prog, scale
		# if leg == 2: print 'move, newpos:', move, newpos
		if leg == legnum: print '[{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(indexmod, move[0],move[1],move[2])
		# if leg == legnum: print '[{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(indexmod, newpos[0],newpos[1],newpos[2])

		self.legs[leg].move_to_pos(*(newpos))

	def reset(self):
		for leg in self.legs:
			leg.move_to_pos(*(leg.resting_position))
		pass

	def iterate(self, delta, deltaRot):
		gaitLength = len(self.z_profile)
		# for i in range(0, gaitLength):
		i = self.i
		for leg in [0, 2, 1, 3]:  # order them diagonally
			self.eachLeg(leg, i, delta, deltaRot)  # move each leg appropriately
		self.i = (i + 1) % gaitLength

		return self.i


########################################################################
#########################################################################


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
		diff = prog * self.z_points - index  # this diff is just allowing addition of fractional height in the next line ... waste of time
		value = self.z_profile[int(index)] + (self.z_profile[int(index + 1)] - self.z_profile[int(index)]) * diff

		prog = (prog if prog <= 0.5 else 1.0 - prog)
		speed = -0.5 + (prog * 2.0)

		# index = math.floor(prog * self.z_points)
		# diff = prog * self.z_points - index
		# value = self.z_profile[int(index)]

		# prog = (prog if prog <= 0.5 else 1.0 - prog)
		# speed = -0.5 + (prog * 2.0)

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
		self.currentDistance = (self.currentDistance + thisDistance) % self.stepDistance

		# current feet height depends on distance (maybe shoudl depend on time? )
		step_progression = self.currentDistance / self.stepDistance
		step_progression_alternate = (step_progression + 0.5) % 1.0  # because it is a 50% duty cycle and need to keep it btwn 0 and 1

		height_pair1, speed_direction_pair1 = self.height_at_progression(step_progression)
		height_pair2, speed_direction_pair2 = self.height_at_progression(step_progression_alternate)

		self.move_leg_group(self.group1, height_pair1, speed_direction_pair1, linear_speed, angular_speed)
		self.move_leg_group(self.group2, height_pair2, speed_direction_pair2, linear_speed, angular_speed)

		return 0

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
