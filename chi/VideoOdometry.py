#! /usr/bin/env python

from __future__ import print_function
from __future__ import division
import numpy as np
import cv2
import datetime as dtm
import logging
import multiprocessing as mp
import lib.Messages as Msg
import lib.zmqclass as Zmq
import lib.Camera as Cam


save_pts = []


class VOError(Exception):
	pass


class VideoOdom(object):
	"""
	why not just fold this into the vo class instead of stand alone???
	- I am thinking I should be able to easily swap out different vo algorithms
	"""
	def __init__(self):
		self.cam = None

	def init(self, params, camera):
		"""
		params = {pp:(tuple), focallength: #}
		camera = {type=pi, size=(640,480)} or {type=cv, size=(), number=1} or {type=video, fileName=''}
		"""
		cam = camera['type']
		if cam == 'pi':
			self.cam = Cam.Camera('pi')
			self.cam.init(camera['size'])
		elif cam == 'cv':
			self.cam = Cam.Camera('cv')
			self.cam.init(camera['size'], camera['number'])
		elif cam == 'video':
			self.cam = Cam.Camera('video')
			self.cam.init(fileName=camera['fileName'])
			print(self.cam)
		else:
			raise VOError('Error: bad init parameters')
		# cam = video.Camera('floor.mp4')
		# cam.setROI((0,479,210,639))
		# cam.load('camera_params.npz')
		# cameraMat = cam.data['camera_matrix']

		# pp = (240,220)
		# focal = 200.0
		self.pp = params['pp']
		self.focal = params['focallength']

		self.R_f = np.eye(3, 3, dtype=np.float)
		self.t_f = np.array([0.0, 0, 0], dtype=np.float)
		# R = np.zeros((3,3),dtype=np.float)
		self.R = self.R_f.copy()
		self.t = np.array([0, 0, 0], dtype=np.float)
		# self.t_prev = t.copy()
		# dist = 0.0

		# cv2.IMREAD_GRAYSCALE faster?
		ret, old_im = self.cam.read()
		ret, im = self.cam.read()
		self.p0 = self.featureDetection(old_im)

		########################################################
		# remove me ... only for this test!
		# roi = (0,479,210,639)
		# self.old_im = old_im[roi[0]:roi[1],roi[2]:roi[3]]
		self.old_im = old_im
		########################################################

		# p0, p1 = featureTrack(im,old_im,p0)
		# E, mask = cv2.findEssentialMat(p0,p1,focal,pp,cv2.FM_RANSAC, 0.999, 1.0)
		# retval, R, t, mask = cv2.recoverPose(E,p0,p1,R,t,focal,pp,mask)

		# save_pts = []
		# while(cam.isOpened()):

	@staticmethod
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
		feature_params = dict(maxCorners=500,
			qualityLevel=0.3,
			minDistance=7,
			blockSize=7)
		keypoints = cv2.goodFeaturesToTrack(im, mask=None, **feature_params)
		print('goodFeaturesToTrack shape', keypoints.shape)

		return keypoints

	def cullBadPts(self, p0, p1, st, err):
		new = []
		old = []

		# print 'st',st
		# print 'err',err
		# print 'p1',p1
		# print 'p0',p0
		# exit()

		# Select good points
		for i in range(0, p1.shape[0]):
			# print 'st',st[i]
			# print 'p1',p1[i]
			if st[i][0] == 1 and p1[i][0][0] >= 0 and p1[i][0][1] >= 0:
				new.append(p1[i][0])
				old.append(p0[i][0])

		good_new = np.array([[k] for k in new], dtype=np.float32)
		good_old = np.array([[k] for k in old], dtype=np.float32)

		return good_old, good_new

	def featureTrack(self, new_gray, old_gray, p0):
		# Parameters for lucas kanade optical flow
		lk_params = dict(winSize=(10, 10),
						maxLevel=3,
						criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

		p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, new_gray, p0, None, **lk_params)

		p0, p1 = self.cullBadPts(p0, p1, st, err)

		return p0, p1

	def grab(self):

		if not self.cam:
			print('Error: camera not setup, run init() first')
			return Msg.Odom()

		try:
			# get values from last run
			pp = self.pp
			focal = self.focal
			p0 = self.p0
			R = self.R
			t = self.t
			R_f = self.R_f
			t_f = self.t_f
			# try this???
			# R = R_f.copy()
			# t = np.array([0, 0, 0], dtype=np.float)
			R = self.R
			t = self.t
			old_im = self.old_im

			ret, raw = self.cam.read()

			# end of video
			if not ret:
				print('video end')
				draw(save_pts)
				# break
				exit()

			################################################
			# only for development ... delete!
			# roi = (0,479,210,639)
			# im = raw[roi[0]:roi[1],roi[2]:roi[3]]
			im = raw
			################################################

			if ret:
				cv2.imshow('debug', im)
				cv2.waitKey(1)

			# Not enough old points, p0 ... find new ones
			if p0.shape[0] < 50:
				print('------- reset --------')
				p0 = self.featureDetection(old_im)  # old_im instead?
				if p0.shape[0] == 0:
					print('bad image')
					# continue
					return

			# p0 - old pts
			# p1 - new pts
			p0, p1 = self.featureTrack(im, old_im, p0)

			# not enough new points p1 ... bad image?
			if p1.shape[0] < 50:
				print('------- reset p1 --------')
				print('p1 size:', p1.shape)
				self.old_im = im
				self.p0 = p1
				# continue
				return

			# drawKeyPoints(im, p1)

			# since these are rectified images, fundatmental (F) = essential (E)
			# E, mask = cv2.findEssentialMat(p0,p1,focal,pp,cv2.FM_RANSAC)
			# retval, R, t, mask = cv2.recoverPose(E,p0,p1,R_f,t_f,focal,pp,mask)

			E, mask = cv2.findEssentialMat(p0, p1, focal, pp, cv2.FM_RANSAC, 0.999, 1.0)
			retval, R, t, mask = cv2.recoverPose(E, p0, p1, R, t, focal, pp, mask)
			# print retval,R

			# Now update the previous frame and previous points
			# self.old_im = im.copy()
			# p0 = p1.reshape(-1,1,2)
			# p0 = p1

			# print 'p0 size',p0.shape
			# print 'p1 size',p1.shape
			# print 't',t
			# dt = t - t_prev
			# scale = np.linalg.norm(dt)
			# print scale
			scale = 1.0

			R_f = R.dot(R_f)
			# t_f = t
			t_f = t_f + scale * R_f.dot(t)

			# t_prev = t
			# t_f = t_f/t_f[2]
			# dist += np.linalg.norm(t_f[:2])

			# num = np.array([t_f[0]/t_f[2],t_f[1]/t_f[2]])
			# num = t_f
			print('position:', t_f)
			# print 'distance:', dist
			# R_f = R*R_f
			# print 'R:',R_f,'t:',t_f
			# print t_f

			save_pts.append(t_f)

			# save all
			self.p0 = p1
			self.R_f = R_f
			self.t_f = t_f
			self.old_im = im.copy()
			self.t = t
			self.R = R

			# create message
			odom = Msg.Odom()
			odom['position']['position']['x'] = t_f[0]
			odom['position']['position']['y'] = t_f[1]
			odom['position']['position']['z'] = t_f[2]

			odom['position']['orientation']['x'] = 0.0  # FIXME: 20160529 do rotation to quaternion conversion
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
			print('captured interrupt')
			exit()
			# break

		# cam.release()


class Server(mp.Process):
	def __init__(self, host="localhost", port='9000', camera=None):
		mp.Process.__init__(self)
		self.epoch = dtm.datetime.now()
		self.host = host
		self.port = port

		self.camera = camera

		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')

	def init(self):
		pass  # do some setup here

	def run(self):
		self.logger.info(str(self.name) + '[' + str(self.pid) + '] started on' + str(self.host) + ':' + str(self.port) + ', Daemon: ' + str(self.daemon))

		pub = Zmq.Pub((self.host, self.port))

		params = {
			'pp': (240, 220),
			'focallength': 200
		}

		vo = VideoOdom()
		if self.camera is None: vo.init(params)
		else: vo.init(params, self.camera)

		try:
			while True:
				odom = vo.grab()
				# print 'Odom:', odom
				pub.pub('vo', odom)
				# time.sleep(0.1)
		except:
			# print 'Error:', e
			raise


def draw(pts):
	import matplotlib.pyplot as plt
	x = []
	y = []
	z = []
	for i in pts:
		x.append(i[0])
		y.append(i[1])
		z.append(i[2])

	# li.set_ydata(y)
	# li.set_xdata(x)
	# fig.canvas.draw()
	plt.subplot(2, 1, 1)
	plt.plot(x, y)
	# plt.axis([0, 6, 0, 20])
	plt.grid(True)
	plt.ylabel('y')
	plt.xlabel('x')
	# plt.draw()
	# plt.pause(15)

	plt.subplot(2, 1, 2)
	yy = np.linspace(0, 1, len(z))
	# plt.clf()
	plt.plot(yy, z)
	plt.grid(True)
	plt.ylabel('z')

	plt.draw()
	plt.pause(25)
	# time.sleep(5)


def main():
	cam = {
		'type': 'video',
		'fileName': 'tmp/visual-odom/floor.mp4'
	}

	srv = Server(camera=cam)
	srv.start()


if __name__ == "__main__":
	main()
