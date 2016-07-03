#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
# from __future__ import division
import cv2             # OpenCV camera
import time            # sleep
import numpy as np
# import logging         # logging
import platform        # determine linux or darwin (OSX)
# import argparse        # command line args


if platform.system().lower() == 'linux':
	import picamera        # on linux, PiCamera
	import picamera.array  # on linux, turn PiCamera images into numpy arrays


class VideoError(Exception):
	pass


class SaveVideo(object):
	"""
	Simple class to save frames to video (mp4v)
	"""
	def __init__(self, filename, image_size, fps=20):
		mpg4 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
		self.out = cv2.VideoWriter()
		self.out.open(filename, mpg4, fps, image_size)

	def write(self, image):
		self.out.write(image)

	def release(self):
		self.out.release()


class VideoPublisher(object):
	"""
	"""
	def __init__(self):
		pass


"""
There are a lot of switch here, maybe figure out a better way, maybe:

classes for:
	pi - picamera
	cv - cvcamera
	video - video clip
	topic - ????

Now have one wrapper around all of these

Camera:
	self.camera = pi|cv|video
	__init__
	__del__
	init()
	read()
	isOpen()
"""


class Camera(object):
	"""
	Generic camera object that can switch between OpenCv in PiCamera.
	"""
	def __init__(self, cam=None):
		"""
		Constructor
		Sets up the camera either for OpenCV camera or PiCamera. If nothing is
		passed in, then it determines the operating system and picks which
		camera to use.
		types:
			pi - PiCamera
			cv - an OpenCV camera
			video - an mjpeg video clip to read from
		default:
			linux: PiCamera
			OSX: OpenCV
		in: type: cv video, or pi
		out: None
		"""
		self.cal = None

		if not cam:
			os = platform.system().lower()  # grab OS name and make lower case
			if os == 'linux':
				cam = 'pi'
			else:
				cam = 'cv'

		if cam == 'pi':
			self.cameraType = 'pi'  # picamera
			self.camera = picamera.PiCamera()
		elif cam == 'cv':
			self.cameraType = 'cv'  # opencv
			self.camera = cv2.VideoCapture()
			# need to do vertical flip?
		elif cam == 'video':
			self.cameraType = 'video'  # opencv
			self.camera = cv2.VideoCapture()
		else:
			raise VideoError('Error, {0!s} not supported'.format((cam)))

		time.sleep(1)  # let camera warm-up

	def __del__(self):
		"""
		Destructor
		Closes and turns off the camera on exit (when this class goes out of scope).
		"""
		# the red light should shut off
		if self.cameraType == 'pi': self.camera.close()
		else: self.camera.release()

		print('exiting camera ... bye!')

	def init(self, win=(640, 480), cameraNumber=0, fileName=None, calibration=None):
		"""
		Initialize the camera and set the image size
		in: image size (tuple (width,height), cameraNumber, calibration)
		out: None
		"""
		if self.cameraType == 'pi':
			self.camera.vflip = True  # camera is mounted upside down
			self.camera.resolution = win
			self.bgr = picamera.array.PiRGBArray(self.camera, size=win)
		elif self.cameraType == 'cv':
			self.camera.open(cameraNumber)
			self.camera.set(3, win[0])
			self.camera.set(4, win[1])
		# self.capture.set(cv2.cv.CV_CAP_PROP_SATURATION,0.2);
		elif self.cameraType == 'video':
			if fileName is None:
				VideoError('Error: video filename is not set')
			self.camera.open(fileName)

		if calibration is not None:
			self.cal = calibration

	# def setCalibration(self, n):
	# 	"""
	# 	Set the calibration data for the camera
	# 	in: numpy array of calibration data
	# 	out: None
	# 	"""
	# 	self.cal = n

	def read(self):
		"""
		Reads a gray scale image
		in: None
		out: cv image (numpy array) in grayscale
		"""
		gray = 0

		if self.cameraType == 'pi':
			self.camera.capture(self.bgr, format='bgr', use_video_port=True)
			gray = cv2.cvtColor(self.bgr.array, cv2.COLOR_BGR2GRAY)
			self.bgr.truncate(0)  # clear stream
			# print 'got image'
			# return True, gray
		else:
			ret, img = self.camera.read()
			if not ret:
				return False, np.array([0])
			# imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			# return True, gray

		if self.cal:  # FIXME 2016-05-15
			print('do calibration correction ... not done yet')

		return True, gray

	def isOpen(self):
		"""
		Determines if the camera is opened or not
		in: None
		out: True/False
		"""
		return True  # FIXME 2016-05-15


def main():
	print('Hello!')

if __name__ == "__main__":
	main()
