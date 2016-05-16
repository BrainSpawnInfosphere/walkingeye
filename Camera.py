#!/usr/bin/env python


import cv2             # OpenCV camera
import time            # sleep
import logging         # logging
import platform        # determine linux or darwin (OSX)
import argparse        # command line args


if platform.system().lower() == 'linux':
	import picamera       # on linux, PiCamera
	import picamera.array # on linux, turn PiCamera images into numpy arrays


class Camera(object):
	"""
	Generic camera object that can switch between OpenCv in PiCamera.
	"""
	def __init__(self, cam=None, num=0):
		"""
		Constructor
		Sets up the camera either for OpenCV camera or PiCamera. If nothing is
		passed in, then it determines the operating system and picks which
		camera to use.
		default:
		    linux: PiCamera
			OSX: OpenCV
		in: type: cv or pi and if OpenCV, what camera number
		out: None
		"""
		self.cal = None

		if not cam:
			os = platform.system().lower() # grab OS name and make lower case
			if os == 'linux': cam = 'pi'
			else: cam = 'cv'

		if cam == 'pi':
			self.cameraType = 'pi' # picamera
			self.camera = picamera.PiCamera()
		else:
			self.cameraType = 'cv' # opencv
			self.cameraNumber = num
			self.camera = cv2.VideoCapture()
			# need to do vertical flip?

		time.sleep(1) # let camera warm-up

	def __del__(self):
		"""
		Destructor
		Closes and turns off the camera on exit (when this class goes out of scope).
		"""
		# the red light should shut off
		if self.cameraType == 'pi': self.camera.close()
		else: self.camera.release()

		print 'exiting camera ... bye!'

	def init(self,win=(640,480)):
		"""
		Initialize the camera and set the image size
		in: image size (tuple (width,height))
		out: None
		"""
		if self.cameraType == 'pi':
			self.camera.vflip = True # camera is mounted upside down
			self.camera.resolution = win
			self.bgr = picamera.array.PiRGBArray(self.camera,size=win)
		else:
			self.camera.open(self.cameraNumber)
			self.camera.set(3, win[0]);
			self.camera.set(4, win[1]);
		# self.capture.set(cv2.cv.CV_CAP_PROP_SATURATION,0.2);

	def setCalibration(self,n):
		"""
		Set the calibration data for the camera
		in: numpy array of calibration data
		out: None
		"""
		self.cal = n

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
			self.bgr.truncate(0) # clear stream
			# print 'got image'
			# return True, gray
		else:
			ret,img = self.camera.read()
			if not ret:
				return False
			# imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			# return True, gray

		if self.cal: # FIXME 2016-05-15
			print 'do calibration correction ... not done yet'

		return True, gray

	def isOpen(self):
		"""
		Determines if the camera is opened or not
		in: None
		out: True/False
		"""
		return True # FIXME 2016-05-15



def main():
	print 'Hello!'

if __name__ == "__main__":
	main()
