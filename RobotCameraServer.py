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

####################################################################
# RobotCameraServer streams camera images as fast as 
# possible.
####################################################################
class RobotCameraServer(mp.Process):
	def __init__(self,host="localhost",port=9100,camera_num=0):
		mp.Process.__init__(self)
		self.epoch = dt.datetime.now()
		self.host = host
		self.port = port
		self.camera_num = camera_num
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')
		
		self.epoch = dt.datetime.now()
		
	def run(self):
		self.logger.info(str(self.name)+'['+str(self.pid)+'] started on'+ str(self.host) + ':' + str(self.port) +', Daemon: '+str(self.daemon))
		
		pub = PubBase64()
		camera = cv2.VideoCapture(self.camera_num)
		self.logger.info('Openned camera: '+str(self.camera_num))
		
		try:
			while True:
				ret, frame = camera.read()
				jpeg = cv2.imencode('.jpg',frame)[1]
				pub.pub('image',jpeg)
				#print '[*] frame: %d k   jpeg: %d k'%(frame.size/1000,len(jpeg)/1000)
				#time.sleep(0.1)
			
		except KeyboardInterrupt:
			pass


def sub():
	sub_topics = ['image']
	
	p = SubBase64(sub_topics,'tcp://192.168.1.22:9000')
	
	try:
		while True:
			topic,msg = p.recv()
			
			if not msg:
				pass
			elif 'image' in msg:
				im = msg['image']
				buf = cv2.imdecode(im,1)
				cv2.imshow('image',buf)
				cv2.waitKey(10)
	
	except KeyboardInterrupt:
		pass

def cli():
	print 'usage: pubsub.py "pub"|"sub" '
	sys.exit(1)

def main():
	if len(sys.argv) < 2:
		cli()
		
	func = sys.argv[1]
	if func == 'sub':
		sub()
	elif func == 'pub':
		pub = RobotCameraServer()
		pub.run()
	else:
		cli()
		

if __name__ == "__main__":
	main()