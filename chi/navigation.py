#!/usr/bin/env python
#
# Kevin J. Walchko 3 April 2016
#

from __future__ import print_function
from __future__ import division
import time
import multiprocessing as mp
import logging
import datetime as dt
# import argparse
import numpy as np
from math import sin, cos, sqrt, pow
from pyrk.pyrk import RK4
import lib.zmqclass as zmq
import lib.Messages as msg
# import lib.FileStorage as fs


def ecef(lat, lon, H):
	# phi = lat
	# lambda = lon
	e = 1
	re = 6378137.0  # m
	rm = re * (1.0 - e**2) / pow(1.0 - e**2 * sin(lat)**2, 3.0 / 2.0)
	rn = re / sqrt(1.0 - e**2 * sin(lat)**2)
	x = (rn + H) * cos(lat) * cos(lon)
	y = (rn + H) * cos(lat) * sin(lon)
	z = (rm + H) * sin(lat)
	return x, y, z

def normalizeQuaternion(w, x, y, z):
	m = sqrt(w**2 + x**2 + y**2 + z**2)
	return w/m, x/m, y/m, z/m

class EOM(object):
	"""
	EoM for navigation
	"""
	def __init__(self):
		# move these to init()?
		# wie = 7.292115E-15		  # earth rotation
		# oe_ie = np.array([(0, -wie, 0), (wie, 0, 0), (0, 0, 0)])
		# Q = updateQ(10, 10, 10)	   # Attitude
		# A = np.zeros([10, 10])	   # state transition matrix
		# fillMatrix(A, oe_ie, 3, 3)
		# fillMatrix(A, -oe_ie * oe_ie, 3, 3, 0, 3)
		# fillMatrix(A, np.eye(3, 3), 3, 3, 3, 0)
		# fillMatrix(A, Q, 4, 4, 6, 6)
		# g = np.array([(0, 0, 9.78, 0, 0, 0)])  # gravity model

		# self.A = A
		# self.B = B
		# self.dt = dt
		self.t = 0.0
		self.rk = RK4(self.eom)
		self.epoch = dt.datetime.now()

	@staticmethod
	def eom(t, X, u):
		"""
		X = [vx vy vz px py pz qw qx qy qz]
		v - velocity
		p - position
		q - quaternion (orientation)

		u = [fx fy fz wx wy wz]
		f - force
		w - angular velocity
		"""
		q = X[6:]
		f = u[0:3]
		wx, wy, wz = u[3:]
		p = X[3:6]
		v = X[0:3]
		wie = np.array([0, 0, 7.292115E-15])
		Ceb = np.eye(3)
		W = np.array([
			(0, wz, -wy, wx),
			(-wz, 0, wz, -wy),
			(wy, -wx, 0, wz),
			(-wx, -wy, -wz, 0)
		])
		vd = -2.0*np.cross(wie, np.cross(wie, v))-np.cross(wie, np.cross(wie, p)) + Ceb.dot(f)
		pd = v
		qd = 0.5 * W.dot(q)

		# print('vd', vd)
		# print('pd', pd)
		# print('qd', qd)

		XX = np.hstack((vd, pd, qd))
		return XX

	def step(self, X, u):
		delta = (dt.datetime.now() - self.epoch).total_seconds()
		# t = self.epoch.total_seconds()
		t = self.t
		# X = self.X
		# dt = self.dt
		X = self.rk.step(X, u, t, delta)

		# fix q
		w,x,y,z = normalizeQuaternion(*X[6:])
		X[6] = w
		X[7] = x
		X[8] = y
		X[9] = z

		self.t += delta
		self.epoch = dt.datetime.now()
		return X


# class KF(object):
# 	"""
# 	Kalman filter correction
# 	"""
# 	def __init__(self):
# 		nQ = np.diag([1, 2, 3, 4, 5, 6])  # process noise
# 		nR = np.diag([1, 2, 3, 4, 5, 6])  # measurement noise
# 		self.kalman = cv2.KalmanFilter(4, 2)
# 		# self.kalman.measurementMatrix = C  # np.array([[1,0,0,0],[0,1,0,0]],np.float32)
# 		self.kalman.transitionMatrix = A   # np.array([[1,0,1,0],[0,1,0,1],[0,0,1,0],[0,0,0,1]],np.float32)
# 		self.kalman.processNoiseCov = Q   # np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]],np.float32) * 0.03
# 		# self.epoch = dt.datetime.now()
#
# 	def step(self, z):
# 		self.kalman.correct(z)
# 		xhat = self.kalman.predict()
# 		return xhat

class Navigation(mp.Process):
	"""
	Still needs lots of work!
	"""
	def __init__(self, host="localhost", port='9000'):
		mp.Process.__init__(self)
		# self.epoch = dt.datetime.now()
		self.host = host
		self.port = port
		# self.sub = Sub('/cmd','tcp://%s:%s'%(host,port))
		# logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger(__name__)
		# self.kf = KF()
		self.eom = EOM()

	def run(self):
		self.logger.info(str(self.name) + '[' + str(self.pid) + '] started on' + str(self.host) + ':' + str(self.port) + ', Daemon: ' + str(self.daemon))
		sub_imu = zmq.Sub('imu', (self.host, self.port))
		sub_vo = zmq.Sub('vo', (self.host, self.port))
		pub = zmq.Pub(('localhost', '9100'))
		# self.logger.info('Openned camera: '+str(self.camera_num))
		v = np.array([0., 0., 0.])
		gps = ecef(39.0, 104.7, 1000.0)
		x = np.array(gps)
		q = np.array([1.0, 0., 0., 0.0])
		X = np.hstack((v, x, q))
		w = np.array([0, 0, 0])

		self.epoch = dt.datetime.now()

		def printX(x,q):
			print('------------------------------------------------')
			print('pos: {:.2f} {:.2f} {:.2f}'.format(*x[0:3]))
			print('vel: {:.2f} {:.2f} {:.2f}'.format(*x[3:6]))
			print('qua: {:.2f} {:.2f} {:.2f} {:.2f}'.format(*x[6:]))
			print('qu2: {:.2f} {:.2f} {:.2f} {:.2f}'.format(*q))

		try:
			ans = {}
			while True:
				topic, imu = sub_imu.recv()
				if imu:
					# print(imu)
					# get this from imu
					x = imu['linear_acceleration']['x']
					y = imu['linear_acceleration']['y']
					z = imu['linear_acceleration']['z']
					f = np.array([x,y,z])

					x = imu['angular_velocity']['x']
					y = imu['angular_velocity']['y']
					z = imu['angular_velocity']['z']
					w = np.array([x,y,z])

					qw = imu['orientation']['w']
					qx = imu['orientation']['x']
					qy = imu['orientation']['y']
					qz = imu['orientation']['z']

					u = np.hstack((f, w))
					X = self.eom.step(X, u)
					printX(X, [qw,qx,qy,qz])

				topic, vo = sub_vo.recv()
				if vo:
					# self.kf.predict()
					# self.kf.??
					print('wtf ... not implemented yet')

				# xar.append(X[3])
				# yar.append(X[4])
				# plot(fig, li, xx, yy)

				# [odom]-----------------------------------------------------
				# pose(position[vector], orientation[quaternion])
				# twist(linear[vector], angular[vector])
				odom = msg.Odom()
				odom['position']['position']['x'] = X[3]
				odom['position']['position']['y'] = X[4]
				odom['position']['position']['z'] = X[5]
				odom['position']['orientation']['x'] = X[6]
				odom['position']['orientation']['y'] = X[7]
				odom['position']['orientation']['z'] = X[8]
				odom['position']['orientation']['z'] = X[9]
				odom['velocity']['linear']['x'] = X[0]
				odom['velocity']['linear']['y'] = X[1]
				odom['velocity']['linear']['z'] = X[2]
				odom['velocity']['angular']['x'] = w[0]
				odom['velocity']['angular']['y'] = w[1]
				odom['velocity']['angular']['z'] = w[2]

				# print(odom)

				pub.pub('/nav', odom)
				# time.sleep(0.05)

		except KeyboardInterrupt:
			print('Navigation: shutting down ...')
			# pass


def main():
	nav = Navigation()
	nav.run()


if __name__ == '__main__':
	main()
