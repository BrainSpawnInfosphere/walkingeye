#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#
# Log:
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
# RobotCmdServer handles incoming commands streamed from somewhere else.
# All information is in coming.
####################################################################
class RobotCmdServer(mp.Process):
	def __init__(self,host="localhost",port=9000):
		mp.Process.__init__(self)
		self.host = host
		self.port = port
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')
	
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
	
	def on_message(self,client, userdata, msg):
		print(msg.topic+' '+str(msg.payload))
	
	def shutdown(self):
		self.pub.close()
		exit()
		
	def run(self):
		self.logger.info(str(self.name)+'['+str(self.pid)+'] started on'+ 
			str(self.host) + ':' + str(self.port) +', Daemon: '+str(self.daemon))
		#p = Publisher((self.host,self.port))
		#self.pub = p.accept()
		#self.logger.info('Accepted connection: ')
		
		
		self.sub = mq.PubSubJSON([('cmds',0)],[self.on_message])
		self.sub.start()
		
		while True:
			time.sleep(0.05) # 0.5 => 20Hz
			# get info
			#msg = self.pub.recv()
			#if msg:
			#	self.parseMsg( msg )




if __name__ == '__main__':
	c = RobotCmdServer()
	c.run()