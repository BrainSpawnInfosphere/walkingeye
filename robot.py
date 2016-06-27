#!/usr/bin/env python
#

from __future__ import division
from __future__ import print_function
import multiprocessing as mp
import logging
import socket

import lib.FileStorage as fs

import Audio
import Navigation as Nav
import Vision
import VideoOdometry as VO
import Hardware


class Robot:
	"""
	"""
	def __init__(self):
		logging.basicConfig(level=logging.INFO)
		self.log = logging.getself.log('robot')

		# is this going to work?
		f = fs.FileStorage()
		f.readYaml('./config/robot.yaml')
		conf = f.db

		# Save logs to file
		handler = logging.FileHandler(conf['logfile'])
		handler.setLevel(logging.INFO)
		formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		self.log.addHandler(handler)

		self.log.info("Create RobotSensorServer and RobotCmdServer")

		mp.log_to_stderr(logging.DEBUG)

		# grab localhosts IP address
		ip = socket.gethostbyname(socket.gethostname())

		# create processes using IP and yaml config
		self.sensors = Vision.Vision(
			ip,
			conf['servers']['sensor']['port'],
			conf['servers']['sensor']['camera'])

		self.cmds = Hardware.Hardware(
			ip,
			conf['servers']['cmd']['port'])

# 		newstdin = os.fdopen(os.dup(sys.stdin.fileno()))
		self.speech = Audio.Audio(
			ip,
			conf['servers']['sound']['port'])

		self.vo = VO.VideoOdometry()
		self.nav = Nav.Navigation()

	def run(self):
		try:
			self.sensors.start()
			self.cmds.start()
			self.speech.start()

			self.sensors.join()
			self.cmds.join()
			self.speech.join()

		except Exception, e:
			self.log.error('Error:', e, exc_info=True)  # exc_info should dump traceback info log


def main():
	robot = Robot()
	robot.run()


if __name__ == '__main__':
	main()
