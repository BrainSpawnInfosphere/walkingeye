#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import time
import sys
import os
from gaits import CrawlGait
from realRobot import QuadrupedRobot
sys.path.insert(0, os.path.abspath('../..'))
import lib.zmqclass as Zmq
import lib.FileStorage as Fs


class RobotController(object):
	"""
	"""
	# desired position
	dx = 0.0
	dy = 0.0
	dz = 0.0
	drot = [0.0, 0.0, 0.0]  # roll pitch yaw deltas?

	def __init__(self, robot):
		"""
		in: robot - either a real or virtual robot
		"""
		self.robot = robot

		self.startTime = time.time()
		# self.trotgait = TrotGait(self.robot)
		self.gait = CrawlGait(self.robot)
		self.gait.reset()

	def init(self):
		"""
		setup everything before main loop.
		"""
		self.robot.init()
		# self.sub = Zmq.Sub('ctlr')

	def move(self):
		"""
		executes a step of the gait.
		"""
		return self.gait.iterate([self.dx, self.dy, self.dz], self.drot)

	def step(self):
		"""
		runs one iteration
		"""
		self.dx = 0.5
		self.dy = 0.0
		self.dz = 0.0
		self.drot[2] = 0.0  # -0.50 i think these are rates not positions

		ret = 1

		# topic, msg = self.sub.recv()
		# if msg:
		# 	print('msg:', msg)
			# self.dx = msg['linear']['x']
		# 	self.dy = msg['linear']['y']
		# 	self.dz = msg['linear']['z']

		# if commands = 0: return

		while ret != 0:  # complete one full gait and be stable
			# if not msg: break  # don't move if no command
			ret = self.move()
			# self.robot.finish_iteration()
			time.sleep(1)


def run():
	robotData = []
	fsj = Fs.FileStorage()
	ret, robotData = fsj.readJson('realRobotData.json')
	# robotData = fsj.db
	print(robotData)
	robot = QuadrupedRobot(robotData)
	cntlr = RobotController(robot)
	cntlr.init()

	while True:
		cntlr.step()


if __name__ == "__main__":
	run()
