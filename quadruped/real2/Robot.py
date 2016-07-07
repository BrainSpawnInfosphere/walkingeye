#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from Leg import Leg
# import time
import numpy
from tranforms import rotateAroundCenter, distance

##########################
class CrawlGait(object):
	"""
	Slow stable, 3 legs on the ground at all times
	"""
	# [0, 0, 0, 0, 0, 10, 40, 40, 30, 7]
	# z_profile = [0.5,1,1,0.5,0,0,0,0,0,0,0,0]  # 12 steps, normalized leg height
	z_profile = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 1, 0.5]  # 12 steps, normalized leg height

	def __init__(self, foot0):
		# Gait.__init__(self)
		# self.robot = robot
		# self.legs = robot.legs  # why redefine?

		self.current_step = 0
		self.legOffsets = [0, 6, 3, 9]
		self.i = 0
		self.foot0 = foot0

		# self.reset()

	def height_at_progression(self, prog):
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

	def eachLeg(self, legNum, index, cmd):
		legnum = 0
		delta = cmd
		delta[2] = 0
		zrot = cmd[2]
		rest = self.foot0[legNum]
		# rest = self.legs[leg].resting_position
		# print('rest', rest)

		# hangle rotation
		rotMove = rotateAroundCenter(rest, 'z', zrot) - rest

		# get correct index for this leg and get height
		indexmod = (index + self.legOffsets[legNum]) % len(self.z_profile)
		z = self.z_profile[indexmod]

		# how far through the gait are we?
		prog = indexmod/len(self.z_profile)

		# now scale (?) and handle translational/rotational movement
		scale = 0.50 * self.height_at_progression(prog)  # why?
		move = scale * (numpy.array(delta) + rotMove)
		# move = rotateAroundCenter(scale * numpy.array(delta), 'z', deltaRot[2])

		move[2] = z

		# newpos = self.legs[leg].resting_position + move
		newpos = rest + move

		# I think this can be done better!!!!!
		# I subtract off rest then add it back in ... why?
		# newpos = scale * (numpy.array(delta) + rotateAroundCenter(rest, 'z', zrot))

		# if leg == legnum: print('[{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(indexmod, move[0],move[1],move[2]))
		if legNum == legnum:
			print('[{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(indexmod, newpos[0], newpos[1], newpos[2]))

		# now move leg/servos
		self.legs[legNum].move(*(newpos))

	# def reset(self):
	# 	for leg in self.legs:
	# 		leg.reset()
		# pass

	def step(self, cmd):
		"""
		"""
		gaitLength = len(self.z_profile)
		i = self.i
		for legNum in [0, 2, 1, 3]:  # order them diagonally
			self.eachLeg(legNum, i, cmd)  # move each leg appropriately

		self.i = (i + 1) % gaitLength

		return self.i

##########################


class Quadruped(object):
	"""
	"""
	def __init__(self, data):
		legs = []
		for i in range(0, 4):
			channel = i*4
			print('channel:', channel)
			legs.append(
				Leg(
					data['legLengths'],
					[channel, channel+1, channel+2],
					data['legLimits']
				)
			)

		# only do this once
		legs[0].servos[0].set_freq(60)

	def setGait(self, gait):
		"""
		"""
		self.gait = gait

	def command(self, cmd):
		"""
		"""
		# cmd = [10, 0, 0]  # x, y, z_rotation
		self.gait.step(cmd)


if __name__ == "__main__":
	test = {
		'legLengths': {
			'coxaLength': 10,
			'tibiaLength': 50,
			'femurLength': 100
		},
		'legLimits': [[-45, 45], [-45, 45], [-90, 0]]
	}
	robot = Quadruped(test)
