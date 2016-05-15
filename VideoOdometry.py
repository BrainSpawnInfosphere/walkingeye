#! /usr/bin/env python

import numpy as np
import cv2
import argparse
import video
import time
import math

import Messages as messages

from zmqclass import *
import multiprocessing as mp

class VideoOdom(object):
	def __init__(self):
		a=0

	def init(self,params):
		"""
		params = {pp:(tuple), focallength: #}
		"""
		self.cam = ???
		# cam = video.Camera('floor.mp4')
		# cam.setROI((0,479,210,639))
		# cam.load('camera_params.npz')
		# cameraMat = cam.data['camera_matrix']


		# pp = (240,220)
		# focal = 200.0
		self.pp = params['pp']
		self.focal = params['focallength']

		R_f = np.eye(3,3,dtype=np.float)
		t_f = np.array([0,0,0],dtype=np.float)
		# R = np.zeros((3,3),dtype=np.float)
		R = R_f.copy()
		t = np.array([0,0,0],dtype=np.float)
		t_prev = t.copy()
		dist = 0.0

		# cv2.IMREAD_GRAYSCALE faster?
		ret, old_im = cam.read(True)
		ret, im = cam.read(True)
		p0 = featureDetection(old_im)
		# p0, p1 = featureTrack(im,old_im,p0)
		# E, mask = cv2.findEssentialMat(p0,p1,focal,pp,cv2.FM_RANSAC, 0.999, 1.0)
		# retval, R, t, mask = cv2.recoverPose(E,p0,p1,R,t,focal,pp,mask)

		# save_pts = []
		# while(cam.isOpened()):

	def featureDetection(im):
		# Initiate FAST object with default values
		# fast = cv2.FastFeatureDetector_create(20,True)
		# fast = cv2.FastFeatureDetector_create()
		# fast.setNonmaxSuppression(True)
		# fast.setThreshold(20)
		# # find and draw the keypoints
		# keypoints = fast.detect(im)
		# keypoints=np.array([[k.pt] for k in keypoints],dtype='f4')
		# print 'fast keypoints',keypoints.shape

		# orb = cv2.ORB_create()
		# keypoints = orb.detect(im,None)
		# keypoints=np.array([[k.pt] for k in keypoints],dtype='f4')
		# print 'orb shape',keypoints.shape

		# params for ShiTomasi corner detection
		feature_params = dict( maxCorners = 500,
			qualityLevel = 0.3,
			minDistance = 7,
			blockSize = 7 )
		keypoints = cv2.goodFeaturesToTrack(im, mask = None, **feature_params)
		print 'goodFeaturesToTrack shape',keypoints.shape

		return keypoints

	def cullBadPts(p0,p1,st,err):
		new = []
		old = []

		# print 'st',st
		# print 'err',err
		# print 'p1',p1
		# print 'p0',p0
		# exit()

		# Select good points
		for i in range(0,p1.shape[0]):
			# print 'st',st[i]
			# print 'p1',p1[i]
			if st[i][0] == 1 and p1[i][0][0] >= 0 and p1[i][0][1] >= 0:
				new.append(p1[i][0])
				old.append(p0[i][0])

		good_new = np.array([[k] for k in new],dtype=np.float32)
		good_old = np.array([[k] for k in old],dtype=np.float32)

		return good_old, good_new


	def featureTrack(new_gray,old_gray,p0):
		# Parameters for lucas kanade optical flow
		lk_params = dict( winSize  = (10,10),
					  maxLevel = 3,
					  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

		p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, new_gray, p0, None, **lk_params)

		p0,p1 = cullBadPts(p0,p1,st,err)

		return p0, p1


	def grab(self, params):

		try:
			ret, im = cam.read(True)

			# end of video
			if not ret:
				print 'video end'
				draw(save_pts)
				break

			# Not enough old points, p0
			if p0.shape[0] < 50:
				print '------- reset --------'
				p0 = featureDetection(im)
				if p0.shape[0] == 0:
					print 'bad image'
					continue

			# p0 - old pts
			# p1 - new pts
			p0, p1 = featureTrack(im,old_im,p0)

			# not enough new points p1
			if p1.shape[0] < 50:
				print '------- reset p1 --------'
				continue

			drawKeyPoints(im,p1)

			# since these are rectified images, fundatmental (F) = essential (E)
			# E, mask = cv2.findEssentialMat(p0,p1,focal,pp,cv2.FM_RANSAC)
			# retval, R, t, mask = cv2.recoverPose(E,p0,p1,R_f,t_f,focal,pp,mask)

			E, mask = cv2.findEssentialMat(p0,p1,focal,pp,cv2.FM_RANSAC, 0.999, 1.0)
			retval, R, t, mask = cv2.recoverPose(E,p0,p1,R,t,focal,pp,mask)
			# print retval,R

			# Now update the previous frame and previous points
			old_im = im.copy()
			# p0 = p1.reshape(-1,1,2)
			p0 = p1

			# print 'p0 size',p0.shape
			# print 'p1 size',p1.shape
			# print 't',t
			# dt = t - t_prev
			# scale = np.linalg.norm(dt)
			# print scale
			scale = 1.0

			R_f = R.dot(R_f)
			# t_f = t
			t_f = t_f + scale*R_f.dot(t)

			# t_prev = t
			# t_f = t_f/t_f[2]
			# dist += np.linalg.norm(t_f[:2])

			# num = np.array([t_f[0]/t_f[2],t_f[1]/t_f[2]])
			# num = t_f
			# print 'position:', t_f
			# print 'distance:', dist
			# R_f = R*R_f
			# print 'R:',R_f,'t:',t_f
			# print t_f

			save_pts.append(t_f)
			# save_pts.append(t_f[:2])

			# create message
			odom = new message.Odom()
			odom['position']['position']['x'] = 0.0
			odom['position']['position']['y'] = 0.0
			odom['position']['position']['z'] = 0.0

			odom['position']['orientation']['x'] = 0.0
			odom['position']['orientation']['y'] = 0.0
			odom['position']['orientation']['z'] = 0.0
			odom['position']['orientation']['w'] = 1.0

			odom['velocity']['linear']['x'] = 0.0
			odom['velocity']['linear']['y'] = 0.0
			odom['velocity']['linear']['z'] = 0.0

			odom['velocity']['angular']['x'] = 0.0
			odom['velocity']['angular']['y'] = 0.0
			odom['velocity']['angular']['z'] = 0.0

			return odom

			except KeyboardInterrupt:
				print 'captured interrupt'
				break

		# cam.release()


class Server(mp.Process):
	def __init__(self,host="localhost",port='9100'):
		mp.Process.__init__(self)
		self.epoch = dt.datetime.now()
		self.host = host
		self.port = port

		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')

	def run(self):
		self.logger.info(str(self.name)+'['+str(self.pid)+'] started on'+ str(self.host) + ':' + str(self.port) +', Daemon: '+str(self.daemon))

		pub = Pub('tcp://'+self.host+':'+self.port)

		# camera = cv2.VideoCapture(self.camera_num)
		# self.logger.info('Openned camera: '+str(self.camera_num))

		vo = VideoOdom()

		try:
			while True:
				# ret, frame = camera.read()
				# jpeg = cv2.imencode('.jpg',frame)[1]
				# pub.pub('image',jpeg)
				#print '[*] frame: %d k   jpeg: %d k'%(frame.size/1000,len(jpeg)/1000)
				#time.sleep(0.1)
				odom = vo.loop()
				pub.pub('vo', odom)
