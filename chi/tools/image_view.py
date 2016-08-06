#!/usr/bin/env python
#
#
# copyright Kevin Walchko
# 29 July 2014
#
# Just a dummy test script

# import time
# import json
import cv2
import base64
import numpy
# from multiprocessing.connection import Client as Subscriber

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import lib.zmqclass as zmq
import lib.Message as msg
import lib.Camera as Camera

# FIXME: 20160522 too many things that really do the same thing!


class CameraDisplayClient(object):
	"""
	Are these the same?
	"""
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.save = False

	def run(self):

		sub_topics = ['image']

		p = zmq.SubBase64(sub_topics, 'tcp://' + self.host + ':' + self.port)

		try:
			while True:
				topic, msg = p.recv()

				if not msg:
					pass
				elif 'image' in msg:
					im = msg['image']
					buf = cv2.imdecode(im, 1)
					cv2.imshow('image', buf)
					cv2.waitKey(10)

		except KeyboardInterrupt:
			pass


class LocalCamera(object):
	"""
	More of the same?
	"""
	def __init__(self, args):
		if args['window']: size = args['window']
		else: size = (640, 480)

		if args['file']: self.save = args['file']
		else: self.save = 'video.mp4'

		self.width = int(size[0])
		self.height = int(size[1])
		self.camera = int(args['camera'])

	def run(self):

		# Source: 0 - built in camera  1 - USB attached camera
		cap = cv2.VideoCapture(self.camera)

		ret = cap.set(3, self.width)
		ret = cap.set(4, self.height)

		# ret, frame = cap.read()
		# h,w,d = frame.shape

		# create a video writer to same images
		sv = 0

		print 'Press q - quit   SPACE - grab image  s - save video'

		save = False

		while(True):
			# Capture frame-by-frame
			ret, frame = cap.read()

			if ret is True:

				# Display the resulting frame
				cv2.imshow('frame', frame)

				if save:
					if sv == 0: sv = Camera.SaveVideo(self.save, (self.width, self.height))
					sv.write(frame)

			key = cv2.waitKey(10)
			if key == ord('q'):
				break
			elif key == ord(' '):
				print 'Grabbing picture'
			elif key == ord('s'):
				save = not save
				print 'Saving video: ' + str(save)

		# When everything done, release the capture
		cap.release()
		sv.release()
		cv2.destroyAllWindows()


if __name__ == '__main__':
	s = zmq.Subscriber(("192.168.1.22", 9100))
	while True:
		try:
			msg = s.recv()
			if not msg:
				pass
			elif 'image' in msg:
				im = msg['image']
				im = base64.b64decode(im)
				im = numpy.fromstring(im, dtype=numpy.uint8)
				buf = cv2.imdecode(im, 1)
				# buf = im
				cv2.imshow('Camera', buf)
				cv2.waitKey(10)

			elif 'sensors' in msg:
				print '[+] Time (', msg['sensors'], '):', msg['imu']
		except (IOError, EOFError):
			print '[-] Connection gone .... bye'
			break
# 		except:
# 			print '[?] pass'
# 			pass

	s.close()
