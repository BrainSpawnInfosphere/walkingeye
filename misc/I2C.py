#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
# import os              # check we are not on travis.ci
# import platform        # determine linux or darwin (OSX)
# from math import cos, sin, pi, atan2, asin, sqrt
# from quaternions import Quaternion
import pygecko.lib.ZmqClass as zmq
import pygecko.lib.Messages as Msg
import multiprocessing as mp
from time import sleep
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from ahrs import AHRS


# maybe have every i2c sensor like this and then the i2c server can be
# generic and run through an array of them
class I2Ccomponent(object):
	def __init__(self):
		# do somethign to setup
		self.sampletime = 0.010  # seconds
		self.topic = 'my_topic'
		pass

	def __del__(self):
		# cleanup?
		pass

	def read(self):
		# get delta from last time

		# is it time yet to read yet? if not return None

		# read sensor and create zmq pub packet
		pkt = {
			'sensor': 'name',
			'data': [1, 2]
		}

		return (pkt, self.topic)


class I2C(mp.Process):
	"""
	You could throw this into pyGeckoQuadruped if you wanted
	"""
	def __init__(self, port):
		mp.Process.__init__(self)
		self.port = port

	def run(self):
		ahrs = AHRS()
		pub = zmq.Pub(bind_to=('0.0.0.0', self.port))

		while True:
			msg = Msg.Compass()
			r, p, h = ahrs.read(deg=True)
			# print('{:.4f} {:.4f} {:.4f}'.format(r, p, h))

			pub.pub('compass', msg)
			sleep(1)
