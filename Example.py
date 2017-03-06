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
# import os
# import sys
import time
from pygecko.lib.ZmqClass import Sub as zmqSub
from pygecko.lib.ZmqClass import Pub as zmqPub
from pygecko.lib import Messages as Msg
from quadruped import Engine
from quadruped import DiscreteRippleGait
from quadruped import AHRS  # attitude and heading reference system
import multiprocessing as mp

##########################


class pyGeckoQuadruped(mp.Process):
	sub_js   = ('0.0.0.0', 9100)
	sub_cmd  = ('0.0.0.0', 9110)
	pub_ahrs = ('0.0.0.0', 9120)
	pub_ir   = ('0.0.0.0', 9130)

	def __init__(self, data):
		mp.Process.__init__(self)
		self.ahrs = AHRS()  # compass sensor
		self.robot = Engine(data)
		leg = self.robot.getFoot0(0)
		self.crawl = DiscreteRippleGait(45.0, leg, self.robot.moveFoot)

	def handleMsg(self, topic, msg):
		cmd = (0, 0, 0)

		if topic is 'cmd':
			# twist message
			x, y, _ = msg.linear
			_, _, z = msg.angular
			cmd = (x, y, z)

		elif topic is 'js':
			ps4 = msg
			x, y = ps4.axes.leftStick
			rz = ps4.axes.rightStick[1]
			cmd = (x, y, rz)
			stop = ps4.buttons.share

			if stop:
				print('You hit <share> ... bye!')
				exit()

		return cmd

	def run(self):
		# setup subscriptions ---------
		cmd_sub = zmqSub(['cmd'], self.sub_cmd)
		js_sub = zmqSub(['js'], self.sub_js)
		ahrs_pub = zmqPub(self.pub_ahrs)
		# ir_pub = zmqPub(self.pub_ir)

		sub = [cmd_sub, js_sub]

		while True:
			for s in sub:
				topic, msg = s.recv()
				if msg:
					cmd = self.handleMsg(topic, msg)
					self.crawl.command(cmd)

			# read ahrs ---------
			d = self.ahrs.read(deg=True)

			roll, pitch, heading = d

			msg = Msg.Compass(units=Msg.Compass.COMPASS_DEGREES)
			msg.roll = roll
			msg.pitch = pitch
			msg.heading = heading
			ahrs_pub.pub('ahrs', msg)
			# print('ahrs', msg)

			if (-90.0 > roll > 90.0) or (-90.0 > pitch > 90.0):
				print('Crap we flipped!!!', msg)

			# read IR ----------
			# msg = Msg.Range()
			# msg.range = [1, 2, 3, 4, 5, 6]
			# ir_pub.pub('ir', msg)

			time.sleep(0.01)


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
		# 'legOffset': [150, 150, 150+90],
		# 'port': 9020
	}

	robot = pyGeckoQuadruped(test)
	# robot.daemon = True
	robot.start()
	print('pid', robot.pid)
	robot.join()
	print('Nothing to see here ... move along, move along')


if __name__ == "__main__":
	run()
