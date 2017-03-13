#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################
from __future__ import division
from __future__ import print_function
import cv2


class FaceDetector(object):
	def __init__(self):
		self.faceCascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

	def __del__(self):
		pass

	def find(self, image):
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		faces = self.faceCascade.detectMultiScale(
			gray,
			scaleFactor=2,
			minNeighbors=2,
			minSize=(30, 30)
			# flags = cv2.CV_HAAR_SCALE_IMAGE
		)

		ret = []
		if faces is not None:
			# w = [0]*4
			# d = {'x': 0, 'y': 0, 'w': 0, 'h': 0}
			for face in faces:
				# w[0], w[1], w[2], w[3] = face
				# d['x'], d['y'], d['w'], d['h'] = face
				x, y, w, h = face
				d = (x, y, w, h)
				ret.append(d)

		return ret
