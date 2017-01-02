#!/usr/bin/env python

from __future__ import division
from __future__ import print_function
import cv2
import pygecko.lib.ZmqClass as zmq
import pygecko.lib.Messages as Msg
import multiprocessing as mp
from time import sleep


class BallTracker(object):
	# hsv colors to threshold on
	greenLower = (29, 86, 6)
	greenUpper = (64, 255, 255)
	diameter = 6.7  # diameter of average tennis ball in cm

	def __init__(self, lower=(29, 86, 6), upper=(64, 255, 255), diameter=6.7):
		"""
		Tracks a ball in an image.
		"""
		self.greenLower = lower
		self.greenUpper = upper
		self.diameter = diameter

	def distance(self, radius):
		return self.diameter

	def find(self, frame):
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# threshold and find the tennis ball
		mask = cv2.inRange(hsv, self.greenLower, self.greenUpper)

		# do some morphological operators to fill in mask gaps and remove
		# outliers (false positives)
		mask = cv2.erode(mask, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=2)

		# find contours in the mask
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None
		radius = 0

		# did we find something?
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)

			# only proceed if the radius meets a minimum size
			if radius > 10:
				# find moments -----------
				# M = cv2.moments(c)
				# center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
				# cv2.circle(frame, center, 5, (0, 0, 255), -1)

				# set center and radius of ball
				center = (int(x), int(y))
				radius = int(radius)

		return center, radius


class Command_BT(mp.Process):
	pubport = None
	subport = None

	def __init__(self):
		"""
		"""
		mp.Process.__init__(self)

	def init(self, pport, sport):
		self.pubport = pport
		self.subport = sport

	def run(self):
		bt = BallTracker()

		sub = zmq.Sub(topics='image_color', connect_to=('0.0.0.0', self.subport))
		pub = zmq.Pub(bind_to=('0.0.0.0', self.pubport))

		print('Started {} on ports: pub {} sub {}'.format('Command_BT', self.pubport, self.subport))

		while True:
			_, msg = sub.recvB64()
			if msg:
				im = msg['image']
				width, height = im.shape[:2]
				center, radius = bt.find(im)
				if center and radius > 10:
					x, y = center
					xx = x-width/2
					yy = y-height/2
					# print('adjust:', xx, yy)

					t = Msg.Twist()
					pub.pub('command', t)
					# print im.shape
			sleep(0.01)


if __name__ == '__main__':
	bt = Command_BT()
	bt.init(9000, 9001)
	bt.start()
