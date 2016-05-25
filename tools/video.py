#!/usr/bin/env python
#
# Author: Kevin J. Walchko
# Date: 11 May 2014
# Version: 0.2
# -------------------------------
# Updates:
# - none
#
# To do:
# - add camera calibration matrix
#

import numpy as np
import cv2
import yaml
import argparse

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# import lib.zmqclass as zmq
import lib.Messages as msg
import lib.Camera as Camera


def create_capture(source, size=(0, 0)):  # FIXME: 20160525 Need to handle picamera
	# cap = cv2.VideoCapture(source)
	#
	# if cap is None or not cap.isOpened():
	# 	print 'Warning: unable to open video source: ', source
	# 	exit(-1)
	# else:
	# 	print '[/] openned video source',source
	#
	# # set size if necessary
	# if size != (0,0):
	# 	w, h = size
	# 	cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, w)
	# 	cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, h)
	# 	print '[>] set camera image size:',w,'x',h

	camera = Camera.Camera()
	if size != (0, 0): camera.init(size)
	else: camera.init()
	return camera


def read(matrix_name):
	"""
	read camera calibration file in
	"""
	fd = open(matrix_name, "r")
	data = yaml.load(fd)
	return data

if __name__ == '__main__':

	parser = argparse.ArgumentParser('A simple program to capture images from a camera. You can capture a single frame using the space bar or a video by using \'v\'')
	parser.add_argument('-c', '--camera', help='which camera to use', default=0)
	parser.add_argument('-p', '--path', help='location to grab images', default='.')
	parser.add_argument('-v', '--video_name', help='video file name', default='out')
	parser.add_argument('-n', '--numpy', type=str, help='numpy camera calibration matrix')
	parser.add_argument('-s', '--size', type=int, nargs=2, help='size of image capture, e.g., 640 480')

	args = vars(parser.parse_args())

	print args

	source = args['camera']
	shotdir = args['path']
	file = args['video_name']

	# image size
	if args['size'] is not None:
		size = (args['size'][0], args['size'][1])
		print 1
	else:
		size = (0, 0)

	# calibration matrix
	if args['numpy'] is not None:
		cam_cal = args['numpy']
		d = read(cam_cal)
		m = d['camera_matrix']
		k = d['dist_coeff']

	# print size
	# print cam_cal

	# open camera
	cap = create_capture(source, size)

	print '---------------------------------'
	print ' ESC/q to quit'
	print ' v to start/stop video capture'
	print ' f to grab a frame'
	print '---------------------------------'

	shot_idx = 0
	video_idx = 0
	video = False
	vfn = ' '

	# Main loop ---------------------------------------------
	while True:
		ret, img = cap.read()

		# print img.shape

		if args['numpy'] is not None:
			img = cv2.undistort(img, m, k)

		cv2.imshow('capture', img)
		ch = cv2.waitKey(20)

		# Quit program using ESC or q
		if ch == 27 or ch == ord('q'):
			exit(0)

		# Start/Stop capturing video
		elif ch == ord('v'):
			if video is False:  # FIXME: 20160525 Change to Camera.VideoSave (or whatever)
				# setup video output
				mpg4 = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
				out = cv2.VideoWriter()
				vfn = '%s_%d.mp4v' % (file, video_idx)
				h, w = img.shape[:2]
				out.open(vfn, mpg4, 20.0, (w, h))
				print '[+] start capture', vfn
			else:
				out.release()
				video_idx += 1
				print '[-] stop capture', vfn
			video = not video

		# Capture a single frame
		elif ch == ord('f'):
			fn = '%s/shot_%03d.png' % (shotdir, shot_idx)
			cv2.imwrite(fn, img)
			print '[*] saved image to', fn
			shot_idx += 1

		if video:
			out.write(img)

	cv2.destroyAllWindows()
