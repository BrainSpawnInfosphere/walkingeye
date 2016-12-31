#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from __future__ import division
import os              # check we are not on travis.ci
import platform        # determine linux or darwin (OSX)
from math import cos, sin, pi, atan2, asin, sqrt
from quaternions import Quaternion
import pygecko.lib.ZmqClass as zmq
import pygecko.lib.Messages as Msg
import multiprocessing as mp
from time import sleep

if platform.system().lower() == 'linux' and 'TRAVISCI' not in os.environ:
	# pip install adafruit-lsm303
	from Adafruit_LSM303 import LSM303
else:
	import random

	class LSM303(object):
		"""
		Dummy interface for testing outside of linux/RPi where I don't have
		access to I2C and the real sensor.
		"""
		def __init__(self):
			random.seed()  # init for random data

		def read(self):
			"""
			Since there isn't a real sensor connected, read() creates random
			data.
			"""
			data = []
			for i in range(6):
				data.append(random.uniform(-1.0, 1.0))
			accel = AHRS.normalize(*data[:3])
			mag = AHRS.normalize(*data[3:])
			return accel, mag


class AHRS(object):
	def __init__(self):
		# MinIMU-9 (L3G4200D and LSM303DLM carrier)
		# http://www.pololu.com/catalog/product/1265
		# accel and mag are measured at 12b
		self.lsm303 = LSM303(accel_address=0x18, mag_address=0x1e)

	@staticmethod
	def normalize(a, b, c):
		m = sqrt(a**2 + b**2 + c**2)

		if m < 1e-6:
			raise Exception('normalize: div by zero')

		a /= m
		b /= m
		c /= m

		return a, b, c

	def quaterion(self):
		r, p, y = self.read()
		return Quaternion.from_eluer(r, p, y)

	@staticmethod
	def grav(x, y, z):
		# default is 2 g's
		div = 2048/2.0
		x /= div
		y /= div
		z /= div
		return x, y, z

	@staticmethod
	def mag(x, y, z):
		# default is 1.3 gauss
		div = 2048/1.3
		x /= div
		y /= div
		z /= div
		return x, y, z

	def read(self, deg=False):
		accel, mag = self.lsm303.read()
		mag = self.mag(*mag)
		# accel = self.normalize(*accel)
		accel = self.grav(*accel)
		# accel = self.normalize(*accel)
		ax, ay, az = accel
		mx, my, mz = mag
		# print('accel {:.4f} {:.4f} {:.4f}\t\tmag {:.4f} {:.4f} {:.4f}'.format(ax,ay,az,mx,my,mz))
		ax, ay, az = accel
		# ax, ay, az = self.normalize(*accel)

		pitch = asin(-ax)

		if abs(pitch) >= pi/2:
			roll = 0.0
		else:
			roll = asin(ay/cos(pitch))
		# pitch = roll = 0.0

		mx, my, mz = mag
		x = mx*cos(pitch)+mz*sin(pitch)
		y = mx*sin(roll)*sin(pitch)+my*cos(roll)-mz*sin(roll)*cos(pitch)
		heading = atan2(y, x)

		# wrap heading between 0 and 360 degrees
		if heading > 2*pi:
			heading -= 2*pi
		elif heading < 0:
			heading += 2*pi

		if deg:
			roll    *= 180/pi
			pitch   *= 180/pi
			heading *= 180/pi

		return roll, pitch, heading


class I2C(mp.Process):
	def __init__(self, port):
		"""
		"""
		mp.Process.__init__(self)
		self.port = port

	def run(self):
		ahrs = AHRS()
		pub = zmq.Pub(bind_to=('0.0.0.0', self.port))

		while True:
			msg = Msg.Compass()
			r, p, h = ahrs.read(deg=True)
			print('{:.4f} {:.4f} {:.4f}'.format(r, p, h))

			pub.pub('compass', msg)
			sleep(1)


if __name__ == "__main__":
	ahrs = AHRS()
	print('Heading [deg]: {:.2f} {:.2f} {:.2f}'.format(*ahrs.read(deg=True)))
