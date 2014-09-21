#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
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

####################################################################
# RobotCmdServer handles incoming commands streamed from somewhere else.
# All information is in coming.
####################################################################
class RobotCmdServer(mp.Process):
	def __init__(self,host="localhost",port=9000):
		mp.Process.__init__(self)
		self.host = host
		self.port = port
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger(__name__)
	
	def motorCmd(self,cmd):
		print cmd
	
	def soundCmd(self,cmd):
		print cmd
		
	def parseMsg(self, msg):
		if 'quit' in msg:
			self.shutdown()
		elif 'cmd' in msg:
			cmd = msg['cmd']
			if 'm' in cmd:
				self.motorCmd( cmd )
			elif 's' in cmd:
				self.soundCmd( cmd )
	
	def shutdown(self):
		self.pub.close()
		exit()
		
	def run(self):
		self.logger.info(str(self.name)+'['+str(self.pid)+'] started on'+ 
			str(self.host) + ':' + str(self.port) +', Daemon: '+str(self.daemon))
		p = Publisher((self.host,self.port))
		self.pub = p.accept()
		self.logger.info('Accepted connection: ')
		
		while True:
			# get info
			msg = self.pub.recv()
			if msg:
				self.parseMsg( msg )


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
		self.logger = logging.getLogger(__name__)
	
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
			'sensors': self.getTime(), 
			'imu': imu
		}
		return msg
		
	def run(self):
		self.logger.info(str(self.name)+'['+str(self.pid)+'] started on'+ str(self.host) + ':' + str(self.port) +', Daemon: '+str(self.daemon))
		p = Publisher((self.host,self.port))
		self.pub = p.accept()
		self.logger.info('Accepted connection: ')
		
		self.camera = cv2.VideoCapture(self.camera_num)
		self.logger.info('Openned camera: '+str(self.camera_num))
		
		while True:
			# send info
			self.pub.send( self.pkgImage() )
			self.pub.send( self.pkgSensors() )
				


####################################################################
# This is the main class that runs on the robot. It spawns all of the
# processes which control the robot.
####################################################################
class Robot:
	def __init__(self):
		logging.basicConfig(level=logging.INFO)
		logger = logging.getLogger(__name__)
		
		f = open('robot.yaml')
		conf = yaml.safe_load(f)
		f.close()
		
		# Save logs to file
		handler = logging.FileHandler( conf['logfile'] )
		handler.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		logger.addHandler(handler)
		
		
		logger.info("Create RobotSensorServer and RobotCmdServer")
		
		
		mp.log_to_stderr(logging.DEBUG)
		
		# grab localhosts IP address
		ip = socket.gethostbyname(socket.gethostname())
		
		# create processes using IP and yaml config
		self.sensors = RobotSensorServer( 
				ip, 
				conf['servers']['sensor']['port'],
				conf['servers']['sensor']['camera'] )
		self.cmds = RobotCmdServer( 
				ip, 
				conf['servers']['cmd']['port'])
	
	def run(self):
		try:
			self.sensors.start()
			self.cmds.start()
			
			self.sensors.join()
			self.cmds.join()
		
		except Exception, e:
			logger.error('Error: ', exc_info=True) # exc_info should dump traceback info log
		

def main():
	robot = Robot()
	robot.run()


if __name__ == '__main__':
	main()