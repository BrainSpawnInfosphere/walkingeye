#!/usr/bin/env python
# --------------------------------------------------------------------
# Kevin J. Walchko
# 4 May 2014
#
# To do:
# - command line args is still shoddy
# x pass image list from command line
# x pass checkerboard or circles from command line
# x pass save file name from command line
# - remove getOptimalNewCameraMatrix()? not sure of its value
# --------------------------------------------------------------------

# A good resource:
# http://docs.opencv.org/3.1.0/dc/dbb/tutorial_py_calibration.html

# storing numpy arrays
# http://robotfantastic.org/serializing-python-data-to-json-some-edge-cases.html
# >>> a = np.array_equal(data, json.loads(json.dumps(data.tolist())))
# >>> np.array(a)

import numpy as np
import cv2
import glob
import yaml
import json
import argparse
# import os
# import sys

# sys.path.insert(0, os.path.abspath('..'))
# import lib.zmqclass as zmq
# import lib.Message as msg
# import lib.Camera as Camera


class CameraCalibration(object):
	'''
	Simple calibration class.
	'''
	def __init__(self):
		self.save_file = 'calibration.npy'
		self.calibration_images = '.'
		self.marker_size = (0, 0)
		self.marker_checkerboard = True

	# # write camera calibration file out
	def save(self):
		fd = open(self.save_file, "w")
		yaml.dump(self.data, fd)
		fd.close()
		# with open(self.save_file, 'w') as f:
		# 	json.dump(self.data, f)

	# read camera calibration file in
	def read(self, matrix_name):
		fd = open(matrix_name, "r")
		self.data = yaml.load(fd)
		fd.close()
		# with open(matrix_name, 'r') as f:
		# 	self.data = json.load(f)

	# print the estimated camera parameters
	def printMat(self):
		# self.data = {'camera_matrix': mtx, 'dist_coeff': dist, 'newcameramtx': newcameramtx}
		# print 'mtx:',self.data['camera_matrix']
		# print 'dist:',self.data['dist_coeff']
		# print 'newcameramtx:',self.data['newcameramtx']
		m = self.data['camera_matrix']
		k = self.data['dist_coeff']
		print 'focal length {0:3.1f} {1:3.1f}'.format(m[0][0], m[1][1])
		print 'image center {0:3.1f} {1:3.1f}'.format(m[0][2], m[1][2])
		print 'radial distortion {0:3.3f} {1:3.3f}'.format(k[0][0], k[0][1])
		print 'tangental distortion {0:3.3f} {1:3.3f}'.format(k[0][2], k[0][3])

	# Pass a gray scale image and find the markers (i.e., checkerboard, circles)
	def findMarkers(self, gray, objpoints, imgpoints):
		# objp = np.zeros((self.marker_size[0]*self.marker_size[1],3), np.float32)
		# objp[:,:2] = np.mgrid[0:self.marker_size[0],0:self.marker_size[1]].T.reshape(-1,2)
		objp = np.zeros((np.prod(self.marker_size), 3), np.float32)
		objp[:, :2] = np.indices(self.marker_size).T.reshape(-1, 2) # make a grid of points

		# Find the chess board corners or circle centers
		if self.marker_checkerboard is True:
			ret, corners = cv2.findChessboardCorners(gray, self.marker_size)
			if ret: print '[+] chess - found corners: ', corners.size / 2
		else:
			ret, corners = cv2.findCirclesGrid(gray, self.marker_size, flags=cv2.CALIB_CB_ASYMMETRIC_GRID)
			# ret, corners = cv2.findCirclesGrid(gray, self.marker_size, flags=cv2.CALIB_CB_CLUSTERING)
			# print '[+] circles - found corners: ', corners.size / 2, 'ret:', ret
			# print 'corners:', corners
			if ret: print '[+] circles - found corners: ', corners.size / 2

		# If found, add object points, image points (after refining them)
		if ret is True:
			term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
			cv2.cornerSubPix(gray, corners, (5, 5), (-1, -1), term)
			imgpoints.append(corners.reshape(-1, 2))
			objpoints.append(objp)
		else:
			print '[-] Couldn\'t find markers'

		# Draw the corners
		self.draw(gray, corners)

		return ret, objpoints, imgpoints

	# draw the detected corners on the image for display
	def draw(self, image, corners):
		# Draw and display the corners
		if corners is not None: cv2.drawChessboardCorners(image, self.marker_size, corners, True)
		cv2.imshow('camera', image)
		cv2.waitKey(500)
		return image

	# use a calibration matrix to undistort an image
	def undistort(self, image):
		# undistort
		dst = cv2.undistort(image, self.data['camera_matrix'], self.data['dist_coeff'], None, self.data['newcameramtx'])
		return dst

	# run the calibration process on a series of images
	def calibrate(self, images):
		# Arrays to store object points and image points from all the images.
		objpoints = []  # 3d point in real world space
		imgpoints = []  # 2d points in image plane.
		w, h = 0, 0

		for fname in images:
			gray = cv2.imread(fname, 0)
			ret, objpoints, imgpoints = self.findMarkers(gray, objpoints, imgpoints)
			h, w = gray.shape[:2]
			# print(fname,h,w)

		# print len(objpoints),len(imgpoints),w,h

		rms, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (w, h), None, None)

		# Adjust the calibrations matrix
		# alpha=0: returns undistored image with minimum unwanted pixels (image pixels at corners/edges could be missing)
		# alpha=1: retains all image pixels but there will be black to make up for warped image correction
		# returns new cal matrix and an ROI to crop out the black edges
		alpha = 0.5
		newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), alpha)
		self.data = {'camera_matrix': mtx, 'dist_coeff': dist, 'newcameramtx': newcameramtx, 'rms': rms, 'rvecs': rvecs, 'tvecs': tvecs}


# set up and handle command line args
def handleArgs():
	parser = argparse.ArgumentParser('A simple program to calibrate a camera')
	parser.add_argument('-m', '--matrix', help='save calibration values', default='calibration.npy')
	parser.add_argument('-t', '--target', help='target type: chessboard or circles', default='chessboard')
	parser.add_argument('-s', '--target_size', type=int, nargs=2, help='size of pattern, for example, (6,7)', default=(11, 4))
	parser.add_argument('-p', '--path', help='location of images to use', required=True)
	parser.add_argument('-d', '--display', help='display images', default=True)

	args = vars(parser.parse_args())
	return args


# main function
def main():
	args = handleArgs()
	imgs_folder = args['path']

	print('Searching {0!s} for images'.format(imgs_folder))

	# calibration_images = '%s/left*.jpg' % (imgs_folder)
	calibration_images = '{0!s}/shot_*.png'.format((imgs_folder))
	images = []
	images = glob.glob(calibration_images)

	print('Number images found: {0:d}'.format(len(images)))
	# print(images)

	cal = CameraCalibration()
	cal.save_file = args['matrix']
	cal.marker_size = (args['target_size'][0], args['target_size'][1])

	print 'Marker size:', cal.marker_size

	if args['target'] == 'chessboard': cal.marker_checkerboard = True
	else: cal.marker_checkerboard = False
	cal.calibrate(images)

	cal.printMat()

	# save data to file
	cal.save()

	# -----------------------------------------------------------------

	# read back in
	cal.read('calibration.npy')

	# crop the image
	# x,y,w,h = roi
	# crop the distorted edges off
	# # dst = dst[y:y+h, x:x+w]
	# cv2.imwrite('calibresult.png',dst)

	image = cv2.imread(images[0], 0)
	dst = cal.undistort(image)
	cv2.imshow('calibrated image', dst)
	# cv2.imshow('original image', image)
	cv2.waitKey(0)

	cv2.destroyAllWindows()

if __name__ == "__main__":
	# print('Here we go!')
	# print('OpenCV', cv2.__version__)
	# while True:
	# 	a=1
	# exit()
	main()
