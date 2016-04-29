#!/usr/bin/env python
#
# Kevin J. Walchko 11 Nov 2014
#

import sys
import time
import json
from zmqclass import *
import multiprocessing as mp
import logging
import datetime as dt
import cv2
import argparse

class Navigation(mp.Process):
	def __init__(self,host="localhost",port='9110'):
		mp.Process.__init__(self)
		# self.epoch = dt.datetime.now()
		self.host = host
		self.port = port
		# self.sub = Sub('/cmd','tcp://%s:%s'%(host,port))
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('navigation')

		self.kalman = cv2.KalmanFilter(4,2)
		self.kalman.measurementMatrix = np.array([[1,0,0,0],[0,1,0,0]],np.float32)
		self.kalman.transitionMatrix = np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],np.float32)
		self.kalman.processNoiseCov = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],np.float32) * 0.03

		# self.epoch = dt.datetime.now()
	def process(self,z):
		kalman.correct(z)
		xhat = kalman.predict()
		return xhat

	def run(self):
		self.logger.info(str(self.name)+'['+str(self.pid)+'] started on'+ str(self.host) + ':' + str(self.port) +', Daemon: '+str(self.daemon))
		self.sub = Sub('/cmd','tcp://%s:%s'%(self.host,self.port))

		# self.logger.info('Openned camera: '+str(self.camera_num))

		try:
			while True:
				msg = {}
				msg = self.sub.recv()
				if msg:
					x = self.process()
					
					pub.pub(x)
				time.sleep(0.05)


		except KeyboardInterrupt:
			pass
