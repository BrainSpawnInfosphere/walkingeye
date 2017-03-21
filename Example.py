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
import time
from pygecko.ZmqClass import Sub as zmqSub
from pygecko.ZmqClass import Pub as zmqPub
from pygecko import Messages as Msg
from quadruped import Engine
from quadruped import DiscreteRippleGait
from quadruped import AHRS  # attitude and heading reference system
import multiprocessing as mp
from quadruped import MCP3208, SPI

##########################


class pyGeckoQuadruped(mp.Process):
	sub_js        = ('0.0.0.0', 9100)
	sub_cmd       = ('0.0.0.0', 9110)
	telemetry_pub = ('0.0.0.0', 9120)

	def __init__(self, data):
		mp.Process.__init__(self)
		# self.ahrs = AHRS()  # compass sensor
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
			print('>> got a command', cmd)

		elif topic is 'js':
			ps4 = msg
			x, y = ps4.axes.leftStick
			rz = ps4.axes.rightStick[1]
			cmd = (x, y, rz)
			print('>> got a command', cmd)

			stop = ps4.buttons.share
			if stop:
				print('You hit <share> ... bye!')
				exit()

		return cmd

	def read_ir(self):
		mcp = self.mcp
		adc = [0] * 8
		for i in range(8):
			adc[i] = mcp.read_adc(i)

		msg = Msg.Range()
		msg.fov = 20.0
		msg.range = adc
		return msg

	def read_compass(self):
		# read ahrs ---------
		roll, pitch, heading = self.ahrs.read(deg=True)

		msg = Msg.Compass(units=Msg.Compass.COMPASS_DEGREES)
		msg.roll = roll
		msg.pitch = pitch
		msg.heading = heading

		if (-90.0 > roll > 90.0) or (-90.0 > pitch > 90.0):
			print('Crap we flipped!!!', msg)

		return msg

	def run(self):
		# pubs ---------------------------------------------
		print('>> Subscribe to cmd on {}:{}'.format(*self.sub_cmd))
		print('>> Subscribe to js on {}:{}'.format(*self.sub_js))
		print('>> Publishing telemetry on {}:{}'.format(*self.telemetry_pub))
		cmd_sub = zmqSub(['cmd'], self.sub_cmd)  # twist
		js_sub = zmqSub(['js'], self.sub_js)  # ps4 ... why? just make all cmd/twist?
		telemetry_pub = zmqPub(self.telemetry_pub)

		# ADC ----------------------------------------------
		# Hardware SPI configuration:
		SPI_PORT   = 0
		SPI_DEVICE = 0
		self.mcp = MCP3208(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

		# Compass ------------------------------------------
		self.ahrs = AHRS()

		sub = [cmd_sub, js_sub]

		while True:
			for s in sub:
				topic, msg = s.recv()
				if msg:
					cmd = self.handleMsg(topic, msg)
					self.crawl.command(cmd)

			# read Compass -----
			msg = self.read_compass()
			# print('ahrs', msg)
			telemetry_pub.pub('ahrs', msg)

			# read IR ----------
			msg = self.read_ir()
			telemetry_pub.pub('ir', msg)
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
