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

####################################################################
# RobotCameraServer streams camera images as fast as
# possible.
####################################################################
class RobotCameraServer(mp.Process):
	def __init__(self,host="localhost",port='9100',camera_num=0):
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

		pub = PubBase64('tcp://'+self.host+':'+self.port)
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


class SaveVideo(object):
	"""
	Simple class to save frames to video (mp4v)
	"""
	def __init__(self,filename,image_size,fps=20):
		mpg4 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
		self.out = cv2.VideoWriter()
		self.out.open(filename,mpg4,fps, image_size)

	def write(self,image):
		self.out.write(image)

	def release(self):
		self.out.release()

class CameraSaveClient(object):
	"""
	"""
	def __init__(self,host,port,filename):
		self.host = host
		self.port = port
		self.save = SaveVideo(filename,(640,480)) # need to fix image size

	def run(self,save):

		sub_topics = ['image']

		p = SubBase64(sub_topics,'tcp://'+self.host+':'+self.port)

		try:
			while True:
				topic,msg = p.recv()

				if not msg:
					pass
				elif 'image' in msg:
					im = msg['image']
					buf = cv2.imdecode(im,1)

					self.save.write(buf)

		except KeyboardInterrupt:
			self.save.release()
			pass


class ImageWriter(object):
	"""
	value here?
	"""
	def __init__(self):
		font = cv2.FONT_HERSHEY_SIMPLEX
		font_scale = 1
		font_color = (155,0,0)

	def writeMsg(frame,msg):
		# font = cv2.FONT_HERSHEY_SIMPLEX
		# font_scale = 1
		# font_color = (155,0,0)
		cv2.putText(frame, msg,(100,100),self.font,self.font_scale,self.font_color,2)

class CameraDisplayClient(object):
	"""
	"""
	def __init__(self,host,port):
		self.host = host
		self.port = port

	def run(self,save):

		sub_topics = ['image']

		p = SubBase64(sub_topics,'tcp://'+self.host+':'+self.port)

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


# set up and handle command line args
def handleArgs():
	parser = argparse.ArgumentParser(description='A simple zero MQ pub/sub for a camera Example: RobotCameraServer pub 192.168.10.22 8080')
	parser.add_argument('info', nargs=3, help='pub or sub, hostname, port; example: pub 10.1.1.1 9333')
	# parser.add_argument('-a', '--address', help='host address', default='localhost')
	# parser.add_argument('-p', '--port', help='port', default='9100')
	parser.add_argument('-f', '--file', help='file name to save video to')
	# parser.add_argument('-g', '--host', nargs=2, help='size of pattern, for example, -s 6 7', required=True)
	# parser.add_argument('-p', '--path', help='location of images to use', required=True)
	# parser.add_argument('-d', '--display', help='display images', default=True)

	args = vars(parser.parse_args())
	return args

def main():
	args = handleArgs()
	func = args['info'][0]
	addr = args['info'][1]
	port = args['info'][2]

	print args
	exit()

	if func == 'sub':
		sub = 0
		if args['file']: sub = CameraSaveClient(args['file'])
		else: sub = CameraDisplayClient(addr,port)
		sub.run()

	elif func == 'pub':
		pub = RobotCameraServer(addr,port)
		pub.run()

	else:
		print 'Error'


if __name__ == "__main__":
	main()
