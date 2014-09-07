#!/usr/bin/env python
#
#
# copyright Kevin Walchko
# 29 July 2014
#
# Just a dummy test script

import time
import json
import cv2
import base64
import numpy
from multiprocessing.connection import Client as Subscriber


if __name__ == '__main__':
	s = Subscriber(("192.168.1.22",9100))
	while True:
		try:
			msg = s.recv()
			if not msg:
				pass
			elif 'image' in msg:
				im = msg['image']
				im = base64.b64decode(im)
				im = numpy.fromstring(im,dtype=numpy.uint8)
				buf = cv2.imdecode(im,1)
				#buf = im
				cv2.imshow('girl',buf)
				cv2.waitKey(10)
		
			elif 'sensors' in msg:
				print '[+] Time (',msg['sensors'],'):',msg['imu']
		except (IOError, EOFError):
			print '[-] Connection gone .... bye'
			break
# 		except:
# 			print '[?] pass'
# 			pass
			
		
	s.close()
	
    