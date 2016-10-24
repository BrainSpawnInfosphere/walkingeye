#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import time
import numpy as np
from math import radians as d2r
from pygecko.lib.ZmqClass import Sub as zmqSub
from Quadruped import Quadruped, CrawlGait
# from kinematics import DH

##########################


class TestQuadruped(Quadruped):
	def __init__(self, data, serialPort):
		Quadruped.__init__(self, data, serialPort)

		robot = Quadruped(data)
		self.crawl = CrawlGait(robot)

	def run(self):
		sub = zmqSub('js', ('localhost', '9000'))

		print('Press <share> on PS4 controller to exit')

		while True:
			topic, ps4 = sub.recv()

			# msg values range between (-1, 1)
			if ps4 and topic == 'js':
				x, y = ps4['axes']['leftStick']
				mm, rz = ps4['axes']['rightStick']

				if ps4['buttons']['share']:
					print('You hit <share> ... bye!')
					exit()

				cmd = [100*x, 100*y, 40*rz]
				print('***********************************')
				print('* xyz {:.2f} {:.2f} {:.2f} *'.format(x, y, rz))
				print('* cmd {:.2f} {:.2f} {:.2f} *'.format(*cmd))
				print('***********************************')
				self.crawl.command(cmd)
			time.sleep(0.01)


class Test2Quadruped(Quadruped):
	def __init__(self, data):
		Quadruped.__init__(self, data)

		robot = Quadruped(data)
		self.crawl = CrawlGait(robot)

	def run(self):
		while True:
			x, y = 1, 0
			rz = 0

			cmd = [100*x, 100*y, 40*rz]
			print('***********************************')
			print('* xyz {:.2f} {:.2f} {:.2f} *'.format(x, y, rz))
			print('* cmd {:.2f} {:.2f} {:.2f} *'.format(*cmd))
			print('***********************************')
			# self.crawl.command(cmd)
			time.sleep(0.01)


def run():
	# angles are always [min, max]
	# xl-320
	test = {
		# 'serialPort': '/dev/tty.usbserial-A5004Flb',
		'legLengths': {
			'coxaLength': 26,
			'femurLength': 42,
			'tibiaLength': 63
		},
		'legAngleLimits': [[-90, 90], [-90, 90], [-180, 0]],
		'legOffset': [150, 150, 150+90]
	}

	robot = Test2Quadruped(test)
	robot.run()


if __name__ == "__main__":
	run()
