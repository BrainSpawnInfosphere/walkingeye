#!/usr/bin/env python
#
#
# copyright Kevin Walchko
# 29 July 2014
#
# Just a dummy test script

import time
import json
from multiprocessing.connection import Client as Subscriber


if __name__ == '__main__':
	s = Subscriber(("192.168.1.12",9000))
	
	while True:
		try:
			time.sleep(3)
			cmd = {'cmd': {'m': {'x': 2.3, 'y': 5.33}, 'speed': 50} }
			s.send(cmd)
		except (IOError, EOFError):
			print '[-] Connection gone .... bye'
			break
		
	s.close()
	
    