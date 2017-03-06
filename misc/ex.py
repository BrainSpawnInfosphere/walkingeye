#!/usr/bin/env python

from __future__ import print_function
from pygecko.servers.Vision import RobotCameraServer as CameraServer

"""
sometimes OpenCV doesn't like multiprocessing and crashes, the move to macOS
Sierra has broken cv and mp.
"""


def main():
	cs = CameraServer('localhost', 9000)

	print('start processes')
	cs.start()

	print('join processes')
	cs.join()


if __name__ == "__main__":
	main()
