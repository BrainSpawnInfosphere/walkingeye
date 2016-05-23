#!/usr/bin/env python
#
# not done

import time
import datetime as dt
import multiprocessing as mp
import logging
import yaml
from zmqclass import *

"""
error message {'system':'hw,camera,audio',
               'level':'info,critical,error',
               'msg':'blah',
               'output': 'save,screen,save-screen,web, ...'
               }
"""
class RobotErrorServer(mp.Process):
	def __init__(self,host="localhost",port=9000):
		mp.Process.__init__(self)
		self.host = host
		self.port = port
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')
# 		self.md = md.MotorDriver(11,12,15,16)


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


		self.sub = Sub(['errors'])

		while True:
			time.sleep(0.05) # 0.5 => 20Hz
			# get info
			msg = self.sub.recv()
			if msg:
				self.on_message( msg )
