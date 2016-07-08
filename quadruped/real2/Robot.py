#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
from Leg import Leg
import time
import numpy
from tranforms import rotateAroundCenter, distance

##########################


class CrawlGait(object):
	"""
	Slow stable, 3 legs on the ground at all times

	This solution works but only allows 1 gait ... need to have multiple gaits
	"""
	z_profile = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.5, 1, 0.5]  # 12 steps, normalized leg height
	scale_profile = [-0.5, -0.39, -0.28, -0.17, -0.06, 0.06, 0.17, 0.28, 0.39, 0.5, 0.17, -0.17]  # FIXME: wrong??

	def __init__(self, robot):
		self.current_step = 0
		self.legOffsets = [0, 6, 3, 9]
		self.i = 0
		self.robot = robot
		# self.reset()

	# def setFoot(self, foot0):
	# 	self.foot0 = foot0

	# def height_at_progression(self, prog):
	# 	"""
	# 	Returns the normalized 1-D foot position for a 75% duty cycle
	# 	|                   *
	# 	|             *       *
	# 	| *                      *
	# 	+-------------------+----+-
	# 	0                  .75  1.0
	# 	Progress (step/gait_length)
	#
	# 	todo - just turn this into a lookup table ... why calculate it?
	# 	"""
	# 	# if prog < 0.0 or prog > 1.0:
	# 	if 0.0 <= prog <= 1.0:
	# 		Exception('prog out of bounds (0-1.0): {}'.format(prog))
	# 	speed = 0.0
	# 	if prog <= 0.75: speed = 4.0 / 3.0 * prog - 0.5
	# 	else: speed = -4.0 * (prog - 0.75) + 0.5  # don't think this is right???
	# 	return speed

	def eachLeg(self, legNum, index, cmd):
		"""
		legNum - which leg to move
		index - the index of the gait: 0-n
		cmd - [x,y,z_rot]
		"""
		legnum = 2
		delta = list(cmd)  # need to make a copy
		zrot = float(delta[2])
		delta[2] = 0
		rest = self.robot.getFoot0(legNum)
		# print('2 zrot', zrot)
		# rest = self.legs[leg].resting_position
		# print('rest', rest)

		# hangle rotation
		# rotMove = rotateAroundCenter(rest, 'z', zrot) - rest

		# get correct index for this leg and get height
		indexmod = (index + self.legOffsets[legNum]) % len(self.z_profile)
		# z = self.z_profile[indexmod]

		# how far through the gait are we?
		# prog = indexmod/len(self.z_profile)

		# now scale (?) and handle translational/rotational movement
		# scale = self.height_at_progression(prog)
		# move = scale * (numpy.array(delta) + rotMove)
		# move = rotateAroundCenter(scale * numpy.array(delta), 'z', deltaRot[2])

		# move[2] = z

		# newpos = self.legs[leg].resting_position + move
		# newpos = rest + move

		# I think this can be done better!!!!!
		# I subtract off rest then add it back in ... why?
		scale = self.scale_profile[indexmod]
		newpos = rest + scale * (numpy.array(delta) + rotateAroundCenter(rest, 'z', zrot) - rest)
		newpos[2] += self.z_profile[indexmod]*25.0

		if legNum == legnum:
			# dr = rotateAroundCenter(rest, 'z', 0.5)
			# print('rest: {:3f}, {:3f}, {:3f}'.format(rest[0], rest[1], rest[2]))
			# print('rotate: {:3f}, {:3f}, {:3f}'.format(dr[0], dr[1], dr[2]))
			# print('scale:', scale)
			# print('[{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(indexmod, move[0], move[1], move[2]))
			print('[{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(indexmod, newpos[0], newpos[1], newpos[2]))

		# now move leg/servos
		# self.legs[legNum].move(*(newpos))
		self.robot.moveFoot(legNum, newpos)

	# def reset(self):
	# 	for leg in self.legs:
	# 		leg.reset()
		# pass
	def command(self, cmd):
		for i in range(0, len(self.z_profile)):
			self.step(i, cmd)

	def step(self, i, cmd):
		"""
		"""
		for legNum in [0, 2, 1, 3]:  # order them diagonally
			self.eachLeg(legNum, i, cmd)  # move each leg appropriately
			time.sleep(0.01)  # need some time to wait for servos to move

##########################


class Quadruped(object):
	"""
	"""
	def __init__(self, data):
		self.legs = []
		for i in range(0, 4):
			channel = i*4
			# print('channel:', channel)
			self.legs.append(
				Leg(
					data['legLengths'],
					[channel, channel+1, channel+2],
					data['legLimits']
				)
			)

		# only do this once
		self.legs[0].servos[0].set_freq(60)
		self.gait = None

	def getFoot0(self, i):
		return self.legs[i].foot0

	def moveFoot(self, i, pos):
		self.legs[i].move(*pos)


def quantize():
	"""
	turn this into table ... double check eqns
	"""
	def eqn(prog):
		speed = 0.0
		if prog <= 0.75: speed = 4.0 / 3.0 * prog - 0.5
		else: speed = -4.0 * (prog - 0.75) + 0.5
		return speed
	for i in range(0, 13):
		print('qantize {} -> {:.2f}'.format(i, eqn(i/12)))


if __name__ == "__main__":
	# quantize()
	# exit()

	test = {
		'legLengths': {
			'coxaLength': 10,
			'tibiaLength': 50,
			'femurLength': 100
		},
		'legLimits': [[-45, 45], [-45, 45], [-90, 0]]
	}
	robot = Quadruped(test)
	# robot.setGait(CrawlGait())
	crawl = CrawlGait(robot)
	i = 1
	while i:
		print('step:', i)
		crawl.command([0, 0.0, 0.50])
		i -= 1
