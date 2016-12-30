#!/usr/bin/env python

from __future__ import print_function
from pygecko.servers.Vision import RobotCameraServer as CameraServer
# from pygecko.Navigation import NavigationServer
# from pygecko.Speech import SoundServer

"""
This is an example of a ROS like launch file

sometimes OpenCV doesn't like multiprocessing and crashes, the move to macOS
Sierra has broken cv and mp.
"""


def main():
	cs = CameraServer('localhost', 9000)
	# nav = NavigationServer('localhost', 9001)
	# aud = SoundServer('localhost', 9002)

	print('start processes')
	# nav.start()
	# aud.start()
	cs.start()

	print('join processes')
	cs.join()
	# nav.join()
	# aud.join()


if __name__ == "__main__":
	main()
