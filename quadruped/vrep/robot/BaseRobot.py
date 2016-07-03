from __future__ import division
from __future__ import print_function
import sys
import os
import numpy as np
sys.path.insert(0, os.path.abspath('../..'))
import lib.FileStorage as Fs


class Robot(object):
	legs = []
	width = 0.0
	length = 0.0
	heigth = 0.0
	orientation = [0.0, 0.0, 0.0]

	def __init__(self, config):
		# print 'working directiry: {}'.format(os.getcwd())

		# read in config file
		fs = Fs.FileStorage()
		fs.readJson(config)
		params = fs.db

		self.femurLength = params['femurLength']
		self.tibiaLength = params['tibiaLength']
		self.width = params['width']
		self.length = params['length']
		self.height = params['height']
		totalDistance = self.femurLength + self.tibiaLength
		front = self.length / 2.0
		back = - self.length / 2.0
		left = self.width / 2.0
		right = - self.width / 2.0
		offset = totalDistance / 2.0

		"""
		foot positions, where the direction of travel is in the x-dir (forward)
		and y-axis to the left. The foot locaitons are marked 1-4.
		         x
                 ^
		      1  |  2
		  y <----+
		      4     3

		[
			[ 144,  119, -50],  foot 1
			[ 144, -119, -50],  foot 2
			[-144,  119, -50],  foot 3
			[-144,  119, -50]   foot 4
		]
		"""
		legs_resting_positions = [(front+offset - params['cg_offet_x'], left+offset, params['resting_heigth']),
		                          (front+offset - params['cg_offet_x'], right-offset, params['resting_heigth']),
		                          (back-offset - params['cg_offet_x'], right-offset, params['resting_heigth']),
		                          (back-offset - params['cg_offet_x'], left+offset, params['resting_heigth'])]    ### front left, front right, back right, back left

		# these are the foot positions
		self.legs_resting_positions = np.array(legs_resting_positions)

	# def load_legs(self):
	# 	"""
	# 	Start the legs, init code
	# 	"""
	# 
	# def read_feet(self):
	# 	"""
	# 	return array of feet sensor values
	# 	:return:
	# 	"""
	#
	# def read_imu(self):
	# 	"""
	# 	returns orientation array
	# 	:return:
	# 	"""

	def move_legs_to_angles(self, angles):
		pass

	def move_leg_to_point(self, leg, x, y, z):
		"""
		move legs to absolute point
		:param leg: leg name
		:param x: body relative x pos
		:param y: body relative y pos
		:param z: body relative z pos
		:return:
		"""

	def finish_iteration(self):
		pass

	def start(self):
		pass
