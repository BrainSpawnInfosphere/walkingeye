#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#
# log:
# 12 Oct 14 Broke out into its own file
#

import time
import json
import cv2
import base64
import datetime as dt
from multiprocessing.connection import Listener as Publisher
import multiprocessing as mp
import logging
import yaml
import socket

import mqttclass as mq

####################################################################
# RobotSensorServer streams images and sensor readings as fast as 
# possible. All information is out going.
####################################################################
class RobotSensorServer(mp.Process):
	def __init__(self,host="localhost",port=9100,camera_num=0):
		mp.Process.__init__(self)
		self.epoch = dt.datetime.now()
		self.host = host
		self.port = port
		self.camera_num = camera_num
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')
		
		self.epoch = dt.datetime.now()
	
	def getTime(self):
		ts = dt.datetime.now() - self.epoch
		return ts
		
	def pkgImage(self):		
		ret, frame = self.camera.read()
		frame = cv2.imencode('.jpg',frame)[1]
		frame = base64.b64encode( frame )
		self.logger.debug('Frame JPG size: '+str(len(frame)))
		msg = {
				'header': self.getTime(), 
				'image': frame
			}
		#time.sleep(1.0/30.0)
		return msg
		
	def pkgSensors(self):
		# get senosrs
		imu = {'ax': 1.0, 'ay': 1.0, 'az': 1.0}
		
		msg = {
			'sensors': (dt.datetime.now() - self.epoch).total_seconds(), #self.getTime(), #FIXME 
			'imu': imu
		}
		return msg
		
	def run(self):
		self.logger.info(str(self.name)+'['+str(self.pid)+'] started on'+ str(self.host) + ':' + str(self.port) +', Daemon: '+str(self.daemon))
		
		#self.camera = cv2.VideoCapture(self.camera_num)
		#self.logger.info('Openned camera: '+str(self.camera_num))
		
		
		self.pub = mq.PubSubJSON([],[])
		self.pub.start()
		
		while True:
			# send info
			self.pub.publish( 'sensors', self.pkgSensors() )
			time.sleep(0.05) # 0.5 => 20Hz
		

if __name__ == '__main__':
	s = RobotSensorServer()
	s.run()