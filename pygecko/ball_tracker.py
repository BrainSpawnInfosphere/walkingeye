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
	diameter = 6.7  # cm

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
	def __init__(self, port):
		"""
		"""
		mp.Process.__init__(self)
		self.port = port

	# def init(self, port):
	# 	self.port = port

	def run(self):
		bt = BallTracker()

		sub = zmq.Sub(topics='image_color', connect_to=('0.0.0.0', self.port))
		pub = zmq.Pub(bind_to=('0.0.0.0', self.port+1))

		print('Started {} on ports: {} {}'.format('Command_BT', self.port, self.port+1))

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
					print('adjust:', xx, yy)

					t = Msg.Twist()
					pub.pub(t)
					# print im.shape
			sleep(0.01)


if __name__ == '__main__':
	s = zmq.Sub(topics='image_color', connect_to=('localhost', 9000))
	while True:
		bt = BallTracker()
		try:
			_, msg = s.recvB64()
			if not msg:
				# print tp, 'no message:', msg_miss
				# msg_miss += 1
				pass
			elif 'image' in msg:
				im = msg['image']
				width, height, depth = im.shape
				center, radius = bt.find(im)
				if center:
					cv2.circle(im, center, radius, (0, 255, 255), 2)
					cv2.circle(im, center, 5, (0, 0, 255), -1)
					cv2.line(im, (0, height/2), (width, height/2), (255, 255, 255), 1)
					cv2.line(im, (320, 0), (320, 480), (255, 255, 255), 1)
					x, y = center
					print('adjust:', x-640/2, y-480/2)
					print(im.shape)

				cv2.imshow('Camera', im)
				key = cv2.waitKey(10)
				if key == ord('q'):
					break

		except (IOError, EOFError):
			print('[-] Connection gone .... bye')
			break

	s.close()
