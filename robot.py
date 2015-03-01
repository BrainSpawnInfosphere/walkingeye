#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#

#import time
#import json
#import cv2
#import base64
#import datetime as dt
#from multiprocessing.connection import Listener as Publisher
import multiprocessing as mp
import logging
import yaml
#import socket

from RobotCmdServer import *
from RobotSensorServer import *
from RobotSoundServer import *

####################################################################
# This is the main class that runs on the robot. It spawns all of the
# processes which control the robot.
####################################################################
class Robot:
	def __init__(self):
		logging.basicConfig(level=logging.INFO)
		logger = logging.getLogger('robot')
		
		f = open('./config/robot.yaml')
		conf = yaml.safe_load(f)
		f.close()
		
		# Save logs to file
		handler = logging.FileHandler( conf['logfile'] )
		handler.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
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
				
		newstdin = os.fdopen(os.dup(sys.stdin.fileno()))
		self.sounds = RobotSoundServer(
				newstdin,
				ip, 
				conf['servers']['sound']['port'])
	
	def run(self):
		try:
			self.sensors.start()
			self.cmds.start()
			self.sounds.start()
			
			self.sensors.join()
			self.cmds.join()
			self.sounds.join()
		
		except Exception, e:
			logger.error('Error: ', exc_info=True) # exc_info should dump traceback info log
		

def main():
	robot = Robot()
	robot.run()


if __name__ == '__main__':
	main()