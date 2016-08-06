#!/usr/bin/env python
#
# Kevin J. Walchko 3 April 2016
#

from __future__ import print_function
from __future__ import division
# import sys
import time
# import json
import multiprocessing as mp
import logging
# import datetime as dt
import cv2
# import argparse
import numpy as np
import math

import lib.zmqclass as zmq
import lib.Messages as msg
# import lib.FileStorage as fs


def ecef(lat, lon, H):
	# phi = lat
	# lambda = lon
	e = 1
	re = 6378137.0  # m
	rm = re * (1.0 - e**2) / math.pow(1.0 - e**2 * math.sin(lat)**2, 3.0 / 2.0)
	rn = re / math.sqrt(1.0 - e**2 * math.sin(lat)**2)
	x = (rn + H) * math.cos(lat) * math.cos(lon)
	y = (rn + H) * math.cos(lat) * math.sin(lon)
	z = (rm + H) * math.sin(lat)
	return x, y, z


def fillMatrix(a, b, m, n, i=0, j=0):
	"""
	Set a(i:m,j:n) = b
	Why numpy doesn't support something this useful already I don't know ... idiots!
	"""
	# j=j-1
	# i=i-1
	for y in range(j, j + n):
		for x in range(i, i + m):
			a[x, y] = b[x - i, y - j]
			# print x,y,a[x,y]


def updateQ(wx, wy, wz):
	Q = 0.5 * np.array([(0, wz, -wy, wx),
					(-wz, 0, wz, -wy),
					(wy, -wx, 0, wz),
					(-wx, -wy, -wz, 0)])
	return Q

# move these to init()?
wie = 7.292115E-15          # earth rotation
oe_ie = np.array([(0, -wie, 0), (wie, 0, 0), (0, 0, 0)])
Q = updateQ(10, 10, 10)       # Attitude
A = np.zeros([10, 10])       # state transition matrix
fillMatrix(A, oe_ie, 3, 3)
fillMatrix(A, -oe_ie * oe_ie, 3, 3, 0, 3)
fillMatrix(A, np.eye(3, 3), 3, 3, 3, 0)
fillMatrix(A, Q, 4, 4, 6, 6)
nQ = np.diag([1, 2, 3, 4, 5, 6])  # process noise
nR = np.diag([1, 2, 3, 4, 5, 6])  # measurement noise
g = np.array([(0, 0, 9.78, 0, 0, 0)])  # gravity model


class Navigation(mp.Process):
	"""
	Still needs lots of work!
	"""
	def __init__(self, host="localhost", port='9110'):
		mp.Process.__init__(self)
		# self.epoch = dt.datetime.now()
		self.host = host
		self.port = port
		# self.sub = Sub('/cmd','tcp://%s:%s'%(host,port))
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('navigation')

		self.kalman = cv2.KalmanFilter(4, 2)
		# self.kalman.measurementMatrix = C  # np.array([[1,0,0,0],[0,1,0,0]],np.float32)
		self.kalman.transitionMatrix = A   # np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],np.float32)
		self.kalman.processNoiseCov = nQ   # np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],np.float32) * 0.03

		# self.epoch = dt.datetime.now()
	def process(self, z):
		self.kalman.correct(z)
		xhat = self.kalman.predict()
		return xhat

	def run(self):
		self.logger.info(str(self.name) + '[' + str(self.pid) + '] started on' + str(self.host) + ':' + str(self.port) + ', Daemon: ' + str(self.daemon))
		sub = zmq.Sub((self.host, self.port))
		pub = zmq.Pub()
		# self.logger.info('Openned camera: '+str(self.camera_num))

		try:
			while True:
				ans = {}
				ans = sub.recv()
				if ans:
					x = self.process(1)  # FIXME: what is z
					odom = msg.Odom()
					pub.pub('/nav', odom)
				time.sleep(0.05)

		except KeyboardInterrupt:
			pass


def main():
	print(A)


if __name__ == '__main__':
	main()
