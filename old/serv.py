#!/usr/bin/env python

import cv2

#cap = cv2.VideoCapture(1)
#ret = cap.set(3,320)
#ret = cap.set(4,240)

#while(True):
	# Capture frame-by-frame 
	#ret, frame = cap.read()
	# Our operations on the frame come here
	#gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	# Display the resulting frame
	#cv2.imshow('frame',gray)
	#if cv2.waitKey(10) & 0xFF == ord('q'):
	#	break

# When everything done, release the capture
#cap.release()
#cv2.destroyAllWindows() 

# import SocketServer
# import time
# 
# class Hello(SocketServer.BaseRequestHandler):
# 	def handle(self):
# 		self.request.sendall(time.ctime())
# 	
# serv = SocketServer.ThreadingTCPServer(("",8080),Hello)
# serv.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# serv.serve_forever()

import socket
import time
import json
import cv2
import base64
import numpy

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("localhost",9000))
s.listen(500)
c,addr = s.accept()
print 'Connect',addr

while True:
#	try:
		jmsg = c.recv(1000000)
		print len(jmsg)
		
		#print 'jmsg',jmsg
		msg = json.loads(jmsg)
		
		if 'quit' in msg:
			print 'Exiting now ...'
			break
		
		elif 'image' in msg:
			img64 = msg['image']
			print 'image len:',len(img64)
			img_jpg = base64.b64decode(img64)
			img_jpg = numpy.fromstring(img_jpg,dtype=numpy.uint8)
			img = cv2.imdecode(img_jpg,1)
			
			#img = numpy.fromstring(img,dtype=numpy.uint8)
			#img = img.reshape((256,256,3))
			
			cv2.imshow('bender',img)
			#time.sleep(2)
		
		else:	
			#print 'bob:',msg['bob'],'big:',msg['big']
			imu = msg['imu']
			#print imu
		
#  	except:
#  		print "Error"
#  		break
s.close()