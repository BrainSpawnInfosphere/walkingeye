#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import multiprocessing as mp
from math import pi
from Engine import Engine
from Gait import DiscreteRippleGait
from ahrs import AHRS  # attitude and heading reference system

##########################

"""
This is a simple demo that walks in a pre-defined path
"""


class SimpleQuadruped(mp.Process):
	def __init__(self, data):
		mp.Process.__init__(self)
		self.ahrs = AHRS()  # compass sensor
		self.body = Engine(data)  # legs/servos
		leg = self.body.getFoot0(0)
		self.crawl = DiscreteRippleGait(45.0, leg, self.body.moveFoot)  # walking motion

		# predefined walking path
		self.path = [  # x,y,rot
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[0, 0, pi/4],
			[0, 0, pi/4],
			[0, 0, pi/4],
			[0, 0, -pi/4],
			[0, 0, -pi/4],
			[0, 0, -pi/4],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
		]

	def run(self):
		for pose in self.path:
			x, y, rz = pose
			# leg = self.body.getFoot0
			cmd = (x, y, rz)

			# read ahrs
			d = self.ahrs.read(deg=True)
			roll, pitch, heading = d
			if (-90.0 > roll > 90.0) or (-90.0 > pitch > 90.0):
				print('Crap we flipped!!!')
				cmd = (0, 0, 0)

			print('***********************************')
			# print('* rest {:.2f} {:.2f} {:.2f}'.format(*leg))
			print('ahrs[deg]: roll {:.2f} pitch: {:.2f} yaw: {:.2f}'.format(d[0], d[1], d[2]))
			print('* cmd {:.2f} {:.2f} {:.2f}'.format(*cmd))
			print('***********************************')
			self.crawl.command(cmd)


def run():
	# angles are always [min, max]
	# xl-320
	test = {
		# 'serialPort': '/dev/serial0',  # real robot
		# 'legLengths': {
		# 	'coxaLength': 45,
		# 	'femurLength': 55,
		# 	'tibiaLength': 104
		# },
		# 'legAngleLimits': [[-90, 90], [-90, 90], [-150, 0]],
		# 'legOffset': [150, 150, 150+90]
	}

	robot = SimpleQuadruped(test)
	robot.start()
	robot.join()


if __name__ == "__main__":
	run()
