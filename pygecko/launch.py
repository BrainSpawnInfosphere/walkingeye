#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
import platform
from Robot import pyGeckoQuadruped
from ball_tracker import Command_BT
import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from I2C import I2C
# import os



# from __future__ import print_function
# from __future__ import division
import pygecko.lib.ZmqClass as zmq
from pygecko.lib import Messages as Msg
import multiprocessing as mp
# import logging
import datetime as dt
import cv2
# import argparse
from opencvutils.video import Camera
import time

# --- topics --------------------------------------------------------------
#   image_raw - raw data from the camera driver, possibly Bayer encoded
#   image            - monochrome, distorted
#   image_color      - color, distorted
#   image_rect       - monochrome, rectified
#   image_rect_color - color, rectified


class CameraServer(mp.Process):
	"""
	Streams camera images as fast as possible
	"""
	def __init__(self, port='9100', camera_num=0, camera_type='cv'):
		mp.Process.__init__(self)
		self.epoch = dt.datetime.now()
		# self.host = host
		self.port = port
		self.camera_num = camera_num
		self.camera_type = camera_type
		# logging.basicConfig(level=logging.INFO)
		# self.logger = logging.getLogger('robot')

		# self.epoch = dt.datetime.now()

	def run(self):
		pub = zmq.Pub(('0.0.0.0', self.port))
		if self.camera_type is 'cv':
			camera = Camera()
			camera.init(cameraNumber=self.camera_num, win=(640, 480))
		else:
			camera = Camera(cam='pi')
			camera.init(win=(640, 480))

		# self.logger.info('Openned camera: ' + str(self.camera_num))

		try:
			while True:
				ret, frame = camera.read()
				jpeg = cv2.imencode('.jpg', frame)[1]  # jpeg compression
				msg = Msg.Image(jpeg)
				pub.pubB64('image_color', msg)
				# print '[*] frame: %d k   jpeg: %d k'%(frame.size/1000,len(jpeg)/1000)
				time.sleep(0.01)

		except KeyboardInterrupt:
			print('Ctl-C ... exiting')
			return


"""
This is an example of a ROS like launch file

sometimes OpenCV doesn't like multiprocessing and crashes, the move to macOS
Sierra has broken cv and mp.
"""


def robot():
	image_color = 9000
	command = 9100
	ahrs = 9200

	test = {
		# 'serialPort': '/dev/tty.usbserial-A5004Flb',  # original debug
		# 'serialPort': '/dev/tty.usbserial-A700h2xE',  # robot
		'legLengths': {
			'coxaLength': 45,
			'femurLength': 55,
			'tibiaLength': 104
		},
		'legAngleLimits': [[-90, 90], [-90, 90], [-150, 0]],
		'legOffset': [150, 150, 150+90],
		'port': command
	}

	quad = pyGeckoQuadruped(test)

	cmd = Command_BT()
	cmd.init(command, image_color)

	if platform.system().lower() == 'linux':
		cs = CameraServer(port=image_color, camera_type='pi')
	else:
		cs = CameraServer(port=image_color, camera_type='cv')

	i2c = I2C(ahrs)

	print('start processes -----------------------------')
	# aud.start()
	cmd.start()
	quad.start()
	i2c.start()
	cs.start()

	print('join processes ------------------------------')
	cs.join()
	cmd.join()
	quad.join()
	i2c.join()
	# aud.join()


if __name__ == "__main__":
	robot()
