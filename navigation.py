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
import numpy as np


def fillMatrix(a,b,m,n,i=0,j=0):
	"""
	Set a(i:m,j:n) = b
	Why numpy doesn't support something this useful already I don't know ... idiots!
	"""
	for y in range(j,j+n):
		for x in range(i,i+m):
			a[x,y] = b[x-i,y-j]
	

wie = 5
oe_ie = np.array([(0,-wie,0),(wie,0,0),(0,0,0)])
A = np.arange(9*9).reshape(9,9)
fillMatrix(A,oe_ie,3,3)
fillMatrix(A,-oe_ie*oe_ie,3,3,3,0)
fillMatrix(A,np.eye(3,3),3,3,?,?)

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
