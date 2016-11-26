#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import time
# import numpy as np
# from math import radians as d2r
from math import pi
from pygecko.lib.ZmqClass import Sub as zmqSub
from Quadruped import Quadruped
from Gait import DiscreteRippleGait
# import time
# from kinematics import DH

##########################


class TestQuadruped(Quadruped):
	def __init__(self, data, serialPort):
		Quadruped.__init__(self, data, serialPort)

		self.robot = Quadruped(data)
		# self.crawl = CrawlGait(robot)
		# self.crawl = TimeCrawlGait(robot)
		leg = self.robot.legs[0].foot0
		self.crawl = DiscreteRippleGait(25.0, leg)

	def run(self):
		sub = zmqSub('js', ('localhost', '9000'))

		print('Press <share> on PS4 controller to exit')

		while True:
			topic, ps4 = sub.recv()

			# msg values range between (-1, 1)
			if ps4 and topic == 'js':
				x, y = ps4['axes']['leftStick']
				rz = ps4['axes']['rightStick'][1]

				if ps4['buttons']['share']:
					print('You hit <share> ... bye!')
					exit()

				cmd = [100*x, 100*y, 40*rz]
				print('***********************************')
				print('* xyz {:.2f} {:.2f} {:.2f} *'.format(x, y, rz))
				print('* cmd {:.2f} {:.2f} {:.2f} *'.format(*cmd))
				print('***********************************')
				self.crawl.command(cmd, self.robot.moveFoot)
			time.sleep(0.01)


class Test2Quadruped(Quadruped):
	def __init__(self, data):
		Quadruped.__init__(self, data)

		self.robot = Quadruped(data)
		leg = self.robot.legs[0].foot0
		self.crawl = DiscreteRippleGait(25.0, leg)
		# self.crawl = ContinousRippleGait(5.0, leg)
		# self.crawl.alpha = 0.5

	def run(self):
		run = True
		while run:
			x, y = 50, 0
			rz = 0 #pi/4  # FIXME: 20161123 CM falling outstide the stability triangle
			leg = self.robot.legs[0].foot0
			cmd = [x, y, rz]
			print('***********************************')
			print('* rest {:.2f} {:.2f} {:.2f}'.format(*leg))
			print('* cmd {:.2f} {:.2f} {:.2f}'.format(*cmd))
			print('***********************************')
			self.crawl.command(cmd, self.robot.moveFoot, steps=12)
			# time.sleep(1)
			# run = False


def run():
	# angles are always [min, max]
	# xl-320
	test = {
		# 'serialPort': '/dev/tty.usbserial-A5004Flb',  # original debug
		'serialPort': '/dev/tty.usbserial-A700h2xE',  # robot
		'legLengths': {
			'coxaLength': 45,
			'femurLength': 55,
			'tibiaLength': 104
		},
		'legAngleLimits': [[-90, 90], [-90, 90], [-150, 0]],
		'legOffset': [150, 150, 150+90]
	}

	robot = Test2Quadruped(test)
	robot.run()


if __name__ == "__main__":
	run()
