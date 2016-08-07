#!/usr/bin/env python
#
# Kevin J. Walchko 11 Nov 2014
#

from __future__ import print_function
from __future__ import division
import lib.zmqclass as zmq
import multiprocessing as mp
import logging
import datetime as dt
import cv2
import argparse
import lib.Camera as Cam


class RobotCameraServer(mp.Process):
	"""
	Streams camera images as fast as possible
	"""
	def __init__(self, host="localhost", port='9100', camera_num=0):
		mp.Process.__init__(self)
		self.epoch = dt.datetime.now()
		self.host = host
		self.port = port
		self.camera_num = camera_num
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')

		self.epoch = dt.datetime.now()

	def run(self):
		self.logger.info(str(self.name) + '[' + str(self.pid) + '] started on' + str(self.host) + ':' + str(self.port) + ', Daemon: ' + str(self.daemon))

		# pub = zmq.PubBase64('tcp://' + self.host + ':' + self.port)
		pub = zmq.PubBase64((self.host, self.port))
		# camera = cv2.VideoCapture(self.camera_num)
		camera = Cam.Camera()
		camera.init(cameraNumber=self.camera_num)

		self.logger.info('Openned camera: ' + str(self.camera_num))

		try:
			while True:
				ret, frame = camera.read()
				jpeg = cv2.imencode('.jpg', frame)[1]  # jpeg compression
				pub.pub('image', jpeg)
				# print '[*] frame: %d k   jpeg: %d k'%(frame.size/1000,len(jpeg)/1000)
				# time.sleep(0.1)

		except KeyboardInterrupt:
			print('Ctl-C ... exiting')
			return


# class SaveVideo(object):
# 	"""
# 	Simple class to save frames to video (mp4v)
# 	"""
# 	def __init__(self,filename,image_size,fps=20):
# 		mpg4 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
# 		self.out = cv2.VideoWriter()
# 		self.out.open(filename,mpg4,fps, image_size)
#
# 	def write(self,image):
# 		self.out.write(image)
#
# 	def release(self):
# 		self.out.release()

# class CameraSaveClient(object):
# 	"""
# 	"""
# 	def __init__(self,host,port,filename):
# 		self.host = host
# 		self.port = port
# 		self.save = SaveVideo(filename,(640,480)) # need to fix image size
#
# 	def run(self,save):
#
# 		sub_topics = ['image']
#
# 		p = SubBase64(sub_topics,'tcp://'+self.host+':'+self.port)
#
# 		try:
# 			while True:
# 				topic,msg = p.recv()
#
# 				if not msg:
# 					pass
# 				elif 'image' in msg:
# 					im = msg['image']
# 					buf = cv2.imdecode(im,1)
#
# 					self.save.write(buf)
#
# 		except KeyboardInterrupt:
# 			self.save.release()
# 			pass


# class ImageWriter(object):
# 	"""
# 	value here?
# 	"""
# 	def __init__(self):
# 		font = cv2.FONT_HERSHEY_SIMPLEX
# 		font_scale = 1
# 		font_color = (155,0,0)
#
# 	def writeMsg(frame,msg):
# 		# font = cv2.FONT_HERSHEY_SIMPLEX
# 		# font_scale = 1
# 		# font_color = (155,0,0)
# 		cv2.putText(frame, msg,(100,100),self.font,self.font_scale,self.font_color,2)

# class LocalCamera(object):
# 	def __init__(self,args):
# 		if args['window']: size = args['window']
# 		else: size = [640,480]
#
# 		if args['file']: self.save = args['file']
# 		else: self.save = 'video.mp4'
#
# 		self.width = int(size[0])
# 		self.height = int(size[1])
# 		self.camera = int(args['camera'])
#
# 	def run(self):
#
# 		# Source: 0 - built in camera  1 - USB attached camera
# 		cap = cv2.VideoCapture(self.camera)
#
# 		ret = cap.set(3,self.width)
# 		ret = cap.set(4,self.height)
#
# 		# ret, frame = cap.read()
# 		# h,w,d = frame.shape
#
# 		# create a video writer to same images
# 		sv = 0
#
# 		print 'Press q - quit   SPACE - grab image  s - save video'
#
# 		save = False
#
# 		while(True):
# 			# Capture frame-by-frame
# 			ret, frame = cap.read()
#
# 			if ret == True:
#
# 				# Display the resulting frame
# 				cv2.imshow('frame',frame)
#
# 				if save:
# 					if sv == 0: sv = SaveVideo(self.save,(self.width,self.height))
# 					sv.write(frame)
#
# 			key = cv2.waitKey(10)
# 			if key == ord('q'):
# 				break
# 			elif key == ord(' '):
# 				print 'Grabbing picture'
# 			elif key == ord('s'):
# 				save = not save
# 				print 'Saving video: ' + str(save)
#
# 		# When everything done, release the capture
# 		cap.release()
# 		sv.release()
# 		cv2.destroyAllWindows()

# class CameraDisplayClient(object):
# 	"""
# 	"""
# 	def __init__(self,host,port):
# 		self.host = host
# 		self.port = port
# 		self.save = False
#
# 	def run(self):
#
# 		sub_topics = ['image']
#
# 		p = SubBase64(sub_topics,'tcp://'+self.host+':'+self.port)
#
# 		try:
# 			while True:
# 				topic,msg = p.recv()
#
# 				if not msg:
# 					pass
# 				elif 'image' in msg:
# 					im = msg['image']
# 					buf = cv2.imdecode(im,1)
# 					cv2.imshow('image',buf)
# 					cv2.waitKey(10)
#
# 		except KeyboardInterrupt:
# 			pass


# set up and handle command line args
def handleArgs():
	parser = argparse.ArgumentParser(description='A simple zero MQ pub/sub for a camera Example: RobotCameraServer pub 192.168.10.22 8080')
	# parser.add_argument('info', nargs=3, help='pub or sub, hostname, port; example: pub 10.1.1.1 9333', default=['pub','localhost','9000'])
	# parser.add_argument('-a', '--address', help='host address', default='localhost')
	# parser.add_argument('-p', '--port', help='port', default='9100')
	parser.add_argument('-f', '--file', help='file name to save video to')
	# parser.add_argument('-g', '--host', nargs=2, help='size of pattern, for example, -s 6 7', required=True)
	# parser.add_argument('-p', '--path', help='location of images to use', required=True)
	# parser.add_argument('-d', '--display', help='display images', default=True)
	parser.add_argument('-p', '--pub', nargs=2, help='publish images to addr:port, ex. pub 10.1.1.1 9000')
	parser.add_argument('-s', '--sub', nargs=2, help='subscribe to images at addr:port, ex. sub 10.1.1.1 9000')
	parser.add_argument('-l', '--local', help='display images to screen', action='store_true')
	parser.add_argument('-w', '--window', nargs=2, help='set window size, ex. -w 640 480')
	parser.add_argument('-c', '--camera', help='set camera number, ex. -c 1', type=int, default=0)
	# parser.add_argument('-f', '--file', help='if local, save images to file')

	args = vars(parser.parse_args())
	return args


def main():
	print('Hello cowboy!')
	# """
	# need to figure out how to cleanly handle window size, save to file for everything
	#
	# maybe pass a dict to every class and let it figure it out instead of function args
	# """
	# args = handleArgs()
	#
	# print args
	# # exit()
	#
	# if args['sub']:
	# 	sub = 0
	# 	if args['file']: sub = CameraSaveClient(args['file'])
	# 	else: sub = CameraDisplayClient(args['sub'][0],args['sub'][1])
	# 	sub.run()
	#
	# elif args['pub']:
	# 	pub = RobotCameraServer(args['pub'][0],args['pub'][1],args['camera'])
	# 	pub.run()
	#
	# elif args['local']:
	# 	local = LocalCamera(args)
	# 	local.run()
	# else:
	# 	print 'Error'


if __name__ == "__main__":
	main()
