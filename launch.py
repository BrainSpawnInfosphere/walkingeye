#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import division
from __future__ import print_function
from Example import pyGeckoQuadruped
from camera_server import CameraServer


def run():
	# test = {
	# 	'serialPort': '/dev/serial0',  # new robot
	# }

	# robot = pyGeckoQuadruped(test)
	robot = pyGeckoQuadruped()
	vision = CameraServer()  # not a process because of opencv issue
	# speech =

	print('start processes -----------------------------')
	# speech.start()
	robot.start()
	vision.start()  # not a process - will hang here

	print('join processes ------------------------------')
	# speech.join()
	robot.join()


if __name__ == "__main__":
	run()
