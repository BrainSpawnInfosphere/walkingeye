#!/usr/bin/env python
#
# Ultimately I want this to be all (or most of) the high level logic for the
# robot.
#
from __future__ import print_function
from __future__ import division
# from pygecko.ZmqClass import Sub as zmqSub
# from pygecko.ZmqClass import Pub as zmqPub
# from pygecko import Messages as Msg
# import multiprocessing as mp
# from time import sleep
# from opencvutils.video import Camera
# import platform
# from quadruped import MCP3208, SPI
# from quadruped import AHRS


class Brain(object):
	"""

	"""
	states = ['normal', 'bored', 'sit', 'stand']
	curr_state = 'normal'
	next_state = 'normal'

	def __init__(self):
		# mp.Process.__init__(self)
		# self.range = []
		pass

	def findBall(self, img):
		pass

	def update(self, cmd, ir, compass):
		if self.curr_state is 'normal':
			self.curr_state = 'normal'
		return cmd

	def run(self):
		pass


# class pyGeckoQuadruped(mp.Process):
# 	def __init__(self):
# 		mp.Process.__init__(self)
# 		self.mind = Brain()
#
# 	def __del__(self):
# 		print('pyGeckoQuadruped exiting ... bye!')
#
# 	def read_compass(self):
# 		rph = self.ahrs.read(deg=True)
# 		msg = Msg.Compass()
# 		msg.units = Msg.Compass.COMPASS_DEGREES
# 		msg.set(*rph)
# 		return msg
#
# 	def read_adc(self):
# 		# this might eventually become ADC
# 		# read ir
# 		# if danger -> move away
# 		mcp = self.mcp
# 		adc = [0] * 8
# 		for i in range(8):
# 			adc[i] = mcp.read_adc(i)
#
# 		msg = Msg.Range()
# 		msg.fov = 20.0
# 		msg.type = Msg.Range.IR
# 		msg.range = adc
# 		return msg
#
# 	# def read_camera(self):
# 	# 	# read camera
# 	# 	# do something? maybe in another thread and just access the current image
# 	# 	# pipline?
# 	# 	msg = None
# 	# 	ret, frame = self.camera.read()
# 	# 	# print('read_camera:', ret, frame.shape)
# 	# 	if ret:
# 	# 		msg = Msg.Image()
# 	# 		msg.img = frame
# 	# 	return msg
#
# 	def read_power(self):
# 		# read current and battery voltage
# 		pass
#
# 	def run(self):
# 		# ADC ----------------------------------------------
# 		# Hardware SPI configuration:
# 		SPI_PORT   = 0
# 		SPI_DEVICE = 0
# 		# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
# 		self.mcp = MCP3208(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))
#
# 		# Compass ------------------------------------------
# 		self.ahrs = AHRS()
#
# 		# camera -------------------------------------------
# 		# self.camera = None
# 		# if platform.system().lower() == 'darwin':
# 		# 	self.camera = Camera()
# 		# 	self.camera.init(cameraNumber=0, win=(640, 480))
# 		# elif platform.system().lower() == 'linux':
# 		# 	self.camera = Camera(cam='pi')
# 		# 	self.camera.init(win=(640, 480))
# 		# else:
# 		# 	print('Sorry, platform not supported')
#
# 		# pubs ---------------------------------------------
# 		print('>> Publishing telemetry on {}:{}'.format('0.0.0.0', '8120'))
# 		pub_telemetry = zmqPub(('0.0.0.0', 8120))
#
# 		# subs ----------------------------------------------
# 		# these most likely will be another computer
# 		sub_cmd = zmqSub(['cmd'], ('0.0.0.0', 8200))
# 		sub_ball = zmqSub(['ball'], ('0.0.0.0', 8300))
#
# 		while True:
# 			cmd = Msg.Twist()
#
# 			topic, msg = sub_cmd.recv()
# 			if msg:
# 				if topic is 'cmd':
# 					print('>> got a command', msg)
#
# 			topic, msg = sub_ball.recv()
# 			if msg:
# 				if topic is 'ball':
# 					print('>> got a ball notification', msg)
#
# 			ir_msg = self.read_adc()
# 			pub_telemetry.pub('ir', ir_msg)
#
# 			# camera_msg = self.read_camera()
# 			# if camera_msg is not None:
# 			# 	pub_camera.pub('image_color', camera_msg)
# 			# how do I do mjpeg stream too (efficiently)?
#
# 			compass_msg = self.read_compass()
# 			pub_telemetry.pub('compass', compass_msg)
#
# 			self.mind.update(cmd, ir_msg, compass_msg)
#
# 			sleep(0.1)
#
#
# if __name__ == "__main__":
# 	robot = pyGeckoQuadruped()
# 	# robot.run()
# 	robot.start()
