#!/usr/bin/python
#
# This is a simple little server that displays a webpage. Note it only delivers
# one webpage or any css or any js files you need.
#
# copyright Kevin Walchko
# 29 July 2014
#

import time
import json
import cv2
import base64
from multiprocessing.connection import Listener as Publisher



# 	pub = Publisher(("",8080))
# 	c = pub.accept()
# 	#pkg = json.dumps( {'bob': 1, 'tom': 44} )
# 	
# 	#frame = cv2.imread("bikini-girl.jpg")
# 	cap = cv2.VideoCapture(0)
# 	
# 	while True:
#		try:
# 			ret, frame = cap.read()
# 			print 'Frame Raw size:',frame.size
# 			frame = cv2.imencode('.jpg',frame)[1]
# 			frame = base64.b64encode( frame )
# 			print 'Frame JPG size:',len(frame)
# 			c.send(frame)
# 			time.sleep(1.0/30.0)
			#pkg = c.recv()
			#print pkg
			#time.sleep(1)
# 		except IOError as e:
# 			print "[-] ERROR({0}): {1}".format(e.errno,e.strerror) 
# 			break
# 		except:
# 			print "[-] ERROR"
# 			break
#	
#	c.close()
#	cap.release()
    