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
# from math import pi
from pygecko.lib.ZmqClass import Sub as zmqSub
from pygecko.Vision import RobotCameraServer as CameraServer
from Quadruped import Quadruped
from Gait import DiscreteRippleGait

##########################


class pyGeckoQuadruped(Quadruped):
	def __init__(self, data):
		Quadruped.__init__(self, data)

		self.robot = Quadruped(data)
		leg = self.robot.legs[0].foot0
		self.crawl = DiscreteRippleGait(45.0, leg)
		# self.crawl = ContinousRippleGait(5.0, leg)
		self.hostinfo = data['hostinfo']

	def run(self):
		sub = zmqSub('js', self.hostinfo)

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
		'legOffset': [150, 150, 150+90],
		'hostinfo': ('localhost', 9100)
	}

	robot = pyGeckoQuadruped(test)
	robot.start()

	cs = CameraServer('localhost', 9000)
	cs.start()

	robot.join()
	cs.join()


if __name__ == "__main__":
	run()
