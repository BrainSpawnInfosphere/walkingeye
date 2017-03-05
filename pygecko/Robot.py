#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

"""
http://www.howtogeek.com/225487/what-is-the-difference-between-127.0.0.1-and-0.0.0.0/

What is the Difference Between 127.0.0.1 and 0.0.0.0?

* 127.0.0.1 is the loopback address (also known as localhost).
* 0.0.0.0 is a non-routable meta-address used to designate an invalid, unknown,
or non-applicable target (a no particular address place holder).

In the context of a route entry, it usually means the default route.

In the context of servers, 0.0.0.0 means all IPv4 addresses on the local
machine. If a host has two IP addresses, 192.168.1.1 and 10.1.2.1, and a server
running on the host listens on 0.0.0.0, it will be reachable at both of those
IPs.
"""


from __future__ import print_function
from __future__ import division
import os
import sys
import time
from pygecko.lib.ZmqClass import Sub as zmqSub
from pygecko.lib import Messages as Msg
sys.path.insert(0, os.path.abspath('..'))
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
		self.port = data['port']

	def run(self):
		# sub = zmqSub(['js', 'led', 'compass'], ('0.0.0.0', self.port))

		# print('Press <share> on PS4 controller to exit')

		while True:
			# topic, msg = sub.recv()
			stop = False
			msg = 1
			topic = 'js'

			# msg values range between (-1, 1)
			if msg and topic is 'js':
				print('loop')
				x, y, rz = (1, 0, 0)
				# ps4 = msg
				# x, y = ps4['axes']['leftStick']
				# rz = ps4['axes']['rightStick'][1]

				# x, y = ps4.axes.leftStick
				# rz = ps4.axes.rightStick[1]

				# stop = ps4.buttons.share

				if stop:
					print('You hit <share> ... bye!')
					exit()

				cmd = [100*x, 100*y, 40*rz]
				print('***********************************')
				print('* xyz {:.2f} {:.2f} {:.2f} *'.format(x, y, rz))
				print('* cmd {:.2f} {:.2f} {:.2f} *'.format(*cmd))
				print('***********************************')
				self.crawl.command(cmd, self.robot.moveFoot)

			elif topic is 'led':
				print(msg)

			elif topic is 'compass':
				print(msg)

			time.sleep(0.01)


def run():
	# angles are always [min, max]
	# xl-320
	# test = {
	# 	# 'serialPort': '/dev/tty.usbserial-A5004Flb',  # original debug
	# 	# 'serialPort': '/dev/tty.usbserial-A700h2xE',  # robot
	# 	'legLengths': {
	# 		'coxaLength': 45,
	# 		'femurLength': 55,
	# 		'tibiaLength': 104
	# 	},
	# 	'legAngleLimits': [[-90, 90], [-90, 90], [-150, 0]],
	# 	'legOffset': [150, 150, 150+90],
	# 	'port': 9020
	# }
	#
	# print('Starting {} on port {}', 'pyGeckoQuadruped', test['port'])
	#
	# robot = pyGeckoQuadruped(test)
	# robot.start()
	# robot.join()
	print('Nothing to see here ... move along, move along')


if __name__ == "__main__":
	run()
