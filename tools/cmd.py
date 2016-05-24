#!/usr/bin/env python
#
#
# copyright Kevin Walchko
# 29 July 2014
#
# Just a dummy test script

import time
#from multiprocessing.connection import Client as Subscriber

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import lib.zmqclass as zmq
import lib.Message as msg

if __name__ == '__main__':
	# this points to the computer running the subscriber
	p = zmq.Pub(("192.168.1.12",9000))

	while True:
		try:
			time.sleep(3)
			#cmd = {'cmd': {'m': {'x': 2.3, 'y': 5.33}, 'speed': 50} }
			cmd = new Twist()
			p.pub('motor',cmd)
		except (IOError, EOFError):
			print '[-] Connection gone .... bye'
			break

	s.close()
