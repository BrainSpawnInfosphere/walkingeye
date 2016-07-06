
from __future__ import print_function
from __future__ import division
import math
import time
import numpy
from tranforms import rotateAroundCenter, distance


class Gait(object):
	"""
	Base class for how to move the legs
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
	z_profile = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 1, 0.5]  # 12 steps, normalized leg height

	def __init__(self, robot):
		Gait.__init__(self, robot)
		self.robot = robot
		self.legs = robot.legs  # why redefine?

		self.current_step = 0
		self.legOffsets = [0, 6, 3, 9]
		self.i = 0

		self.reset()

	def height_at_progression(self, prog):
	# def something(self, prog):
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
		# if prog < 0.0 or prog > 1.0:
		if 0.0 < prog < 1.0:
			Exception('prog too high: {}'.format(prog))
		speed = 0.0
		if prog <= 0.75: speed = 4.0 / 3.0 * prog - 0.5
		else: speed = -4.0 * (prog - 0.75) + 0.5
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
		scale = 0.50 * self.height_at_progression(prog)
		move = scale * (numpy.array(delta) + rotMove)
		# move = rotateAroundCenter(scale * numpy.array(delta), 'z', deltaRot[2])

		move[2] = z
		newpos = self.legs[leg].resting_position + move
		# if leg == 2: print 'prog, scale', prog, scale
		# if leg == 2: print 'move, newpos:', move, newpos
		# if leg == legnum: print('[{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(indexmod, move[0],move[1],move[2]))
		if leg == legnum: print('[{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(indexmod, newpos[0],newpos[1],newpos[2]))

		self.legs[leg].move_to_pos(*(newpos))

	def reset(self):
		for leg in self.legs:
			leg.reset()
		# pass

	def iterate(self, delta, deltaRot):
		gaitLength = len(self.z_profile)
		i = self.i
		for legNum in [0, 2, 1, 3]:  # order them diagonally
			self.eachLeg(legNum, i, delta, deltaRot)  # move each leg appropriately
		self.i = (i + 1) % gaitLength

		return self.i
