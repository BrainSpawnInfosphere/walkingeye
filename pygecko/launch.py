#!/usr/bin/env python


from __future__ import print_function
from pygecko.servers.Vision import RobotCameraServer as CameraServer
# from pygecko.Navigation import NavigationServer
# from pygecko.Speech import SoundServer
from Robot import pyGeckoQuadruped
from ball_tracker import Command_BT


"""
This is an example of a ROS like launch file

sometimes OpenCV doesn't like multiprocessing and crashes, the move to macOS
Sierra has broken cv and mp.
"""


def robot():
	test = {
		# 'serialPort': '/dev/tty.usbserial-A5004Flb',  # original debug
		# 'serialPort': '/dev/tty.usbserial-A700h2xE',  # robot
		'legLengths': {
			'coxaLength': 45,
			'femurLength': 55,
			'tibiaLength': 104
		},
		'legAngleLimits': [[-90, 90], [-90, 90], [-150, 0]],
		'legOffset': [150, 150, 150+90],
		'port': 9020
	}

	quad = pyGeckoQuadruped(test)
	cmd = Command_BT(9300)
	# cmd.init(9300)
	cs = CameraServer('localhost', 9000)  # not MP ... start last

	print('start processes -----------------------------')
	# nav.start()
	# aud.start()
	cmd.start()
	quad.start()
	cs.start()

	print('join processes ------------------------------')
	cs.join()
	cmd.join()
	quad.join()
	# aud.join()


if __name__ == "__main__":
	robot()
