#!/usr/bin/env python

from quadruped import Engine
from quadruped import DiscreteRippleGait
from math import pi
# import time


class Test(object):
	def __init__(self, data):
		self.robot = Engine(data)
		leg = self.robot.getFoot0(0)
		self.crawl = DiscreteRippleGait(45.0, leg, self.robot.moveFoot, self.robot.legs[0].servos[0].write)

	def run(self):
		# predefined walking path
		path = [  # x,y,rot
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[1.0, 0, 0],
			[0, 0, pi/4],
			[0, 0, pi/4],
			[0, 0, pi/4],
			[0, 0, -pi/4],
			[0, 0, -pi/4],
			[0, 0, -pi/4],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
			[-1.0, 0, 0],
		]

		# leg = self.robot.getFoot0(0)
		# print('test_walk wait')
		# time.sleep(5)
		# print('test_walk bye')
		# exit(0)

		# while True:
		for cmd in path:

			# read ahrs
			# d = self.ahrs.read(deg=True)
			# roll, pitch, heading = d
			# if (-90.0 > roll > 90.0) or (-90.0 > pitch > 90.0):
			# 	print('Crap we flipped!!!')
			# 	cmd = (0, 0, 0)

			print('***********************************')
			# print(' rest {:.2f} {:.2f} {:.2f}'.format(*leg))
			# print('ahrs[deg]: roll {:.2f} pitch: {:.2f} yaw: {:.2f}'.format(d[0], d[1], d[2]))
			print(' cmd {:.2f} {:.2f} {:.2f}'.format(*cmd))
			# print('***********************************')
			self.crawl.command(cmd)


def main():
	data = {
		'serialPort': '/dev/tty.usbserial-AL034G2K',  # sparkfun usb-serial
		'write': 'bulk'
	}

	test = Test(data)

	try:
		test.run()
	except KeyboardInterrupt:
		print('bye ...')


if __name__ == '__main__':
	main()
