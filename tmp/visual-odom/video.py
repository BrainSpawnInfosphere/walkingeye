#! /usr/bin/env python

import numpy as np
import cv2
import argparse

#  brew install opencv3 --without-numpy --with-contrib --with-ffmpeg --with-tbb --with-qt5 --with-vtk --with-opengl --with-jasper

# ./video.py -m camera_params.npz

class SaveVideo(object):
	"""
	Simple class to save frames to video (mp4v)
	"""
	def __init__(self,fn,image_size,fps=30):
		mpg4 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
		self.out = cv2.VideoWriter()
		self.out.open(fn,mpg4,fps,image_size)

	def write(self,image):
		self.out.write(image)

	def release(self):
		self.out.release()

class Camera(object):
	"""
	A simple class to grab images from a camera.
	"""
	def __init__(self,input):
		"""
		"""
		self.cap = cv2.VideoCapture(input)
		self.useROI = False

	def size(self,width,height):
		self.width = width
		ret = self.cap.set(3,width)
		if not ret: print 'WARNiNG: Could not set image width to',width

		self.height = height
		ret = self.cap.set(4,height)
		if not ret: print 'WARNiNG: Could not set image height to',height

	def undistort(self,image):

		# undistort
		dst = cv2.undistort(image, self.data['camera_matrix'],self.data['dist_coeff'],None,self.data['newcameramtx'])
		return dst

	def load(self,matrix_name):
		fd = open(matrix_name,"r")
		p = np.load(fd)
		print p['camera_matrix']
		print p['dist_coeff']
		print p['newcameramtx']
		# put these into seperate matricies?
		self.data = {'camera_matrix': p['camera_matrix'], 'dist_coeff': p['dist_coeff'], 'newcameramtx': p['newcameramtx']}

	def isOpened(self):
		return self.cap.isOpened()

	def setROI(self,roi):
		self.roi = roi
		self.useROI = True

	def read(self, isBnW=False):
		ret, image = self.cap.read()

		if self.useROI and ret:
			roi = self.roi
			image = image[roi[0]:roi[1],roi[2]:roi[3]]

		if isBnW and ret:
			image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		return ret, image

	def release(self):
		self.cap.release()


def handleArgs():
	parser = argparse.ArgumentParser('A simple program to grab camera images')
	# parser.add_argument('-m', '--matrix', help='save calibration values', default='calibration.npy')
	# parser.add_argument('-t', '--target', help='target type: chessboard or circles', default='chessboard')
	# parser.add_argument('-s', '--target_size', type=int, nargs=2, help='size of pattern, for example, -s 6 7', default=(11,4))
	# parser.add_argument('-p', '--path', help='location of images to use', required=True)
	parser.add_argument('-g', '--grayscale', help='display images as gray scale, default is False', action='store_true')
	parser.add_argument('-d', '--display', help='display images', action='store_true')
	parser.add_argument('-i', '--input', type=int, help='camera input, default is 0', default=0)
	parser.add_argument('-f', '--file', help='camera input, ex: --input my_movie.mp4')
	parser.add_argument('-m', '--matrix', help='use calibration matrix to rectify image, ex. --matrix my_matrix.npz')
	parser.add_argument('-s', '--save', help='save video to mp4, default is False', action='store_true')
	parser.add_argument('-w','--window', type=int, nargs=2, help='image width and height, ex: --window 640 480')

	args = vars(parser.parse_args())
	return args

def main():
	args = handleArgs()
	print args

	if args['save']:
		sv = SaveVideo('output.mp4',(640,480))

	if args['file']: cam = Camera(args['file'])
	else: cam = Camera(args['input'])

	if args['window']:
		cam.size(args['window'][0],args['window'][1])

	# cam.load('camera_params.npz')
	if args['matrix'] is not None:
		cam.load(args['matrix'])

	while(cam.isOpened()):
		im = cam.read(args['grayscale'])

		if args['matrix']:
			im = cam.undistort(im)

		if args['save']:
			sv.write(im)

		if args['display']:
			cv2.imshow('camera image',im)

		key = cv2.waitKey(10)
		if key == ord('q'):
			break
		elif (key & 0xFF) == 27: #Esc
			break

	if args['save']: sv.release()
	cam.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	main()
