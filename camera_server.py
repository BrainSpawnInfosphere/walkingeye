#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import division
from __future__ import print_function
from ball_tracker import BallTracker
from face_detector import FaceDetector
from pygecko.lib import ZmqClass as zmq
from pygecko.lib import Messages as Msg
from opencvutils.video import Camera
import platform
# from time import sleep


# --- ROS topics --------------------------------------------------------------
#   image_raw - raw data from the camera driver, possibly Bayer encoded
#   image            - monochrome, distorted
#   image_color      - color, distorted
#   image_rect       - monochrome, rectified
#   image_rect_color - color, rectified

class CameraServer(object):
	"""
	Streams camera images as fast as possible
	"""
	camera = None

	def __init__(self):
		if platform.system().lower() == 'darwin':
			self.camera = Camera()
			self.camera.init(cameraNumber=0, win=(640, 480))
		elif platform.system().lower() == 'linux':
			self.camera = Camera(cam='pi')
			self.camera.init(win=(640, 480))
		else:
			print('Sorry, platform not supported')
			exit()

		self.balltracker = BallTracker()

		self.face = FaceDetector()

	def __del__(self):
		if self.camera:
			self.camera.close()

	def start(self):
		self.run()

	def join(self):
		pass

	def run(self):
		print('Publishing ball {}:{}'.format('0.0.0.0', '9000'))
		pub_ball = zmq.Pub(('0.0.0.0', 9000))
		print('Publishing image_color {}:{}'.format('0.0.0.0', '9010'))
		pub_image = zmq.Pub(('0.0.0.0', 9010))

		try:
			while True:
				ret, frame = self.camera.read()
				msg = Msg.Image()
				msg.img = frame
				pub_image.pub('image_color', msg)

				width, height = frame.shape[:2]
				center, radius = self.balltracker.find(frame)
				if center and radius > 10:
					x, y = center
					xx = x-width/2
					yy = y-height/2

					msg = Msg.Vector()
					msg.set(xx, yy, 0)
					pub_ball.pub('ball', msg)

				faces = self.face.find(frame)
				if len(faces) > 0:
					print('found a face!', faces, type(faces))
					# msg = Msg.Array()
					# msg.array = [[1,2,3,4], [4,5,6,7]]
					# msg.array = list(faces)
					# msg.array = faces
					# print('msg >>', msg, type(msg.array))
					# pub_ball.pub('faces', msg)
					# print(msg)

				# sleep(0.01)

		except KeyboardInterrupt:
			print('Ctl-C ... exiting')
			return


if __name__ == '__main__':
	bt = CameraServer()
	bt.start()
