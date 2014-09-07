#!/usr/bin/env python

# import cv2
# 
# #	cv2.imshow('frame',gray)
# #	if cv2.waitKey(10) & 0xFF == ord('q'):
# #		break
# 
# # When everything done, release the capture
# #cv2.destroyAllWindows() 
# 
# #import urllib2
# import socket
# 
# #r = urllib2.Request("localhost:8080")
# #u = urllib2.urlopen(r)
# #data = u.read()
# 
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(("localhost",8080))
# 
# #while True:
# data = s.recv(50)
# print data

import socket
import json
import time
import cv2
import base64
#from collections import namedtuple

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost",9000))

img = cv2.imread('Bender.png')
#cap = cv2.VideoCapture(0)

for i in range(0,10):
	imu = {'x':23.1, 'y':34.2,'z':45.3}
	data = dict({'big': 1.44, 'bob':-450, 'imu': imu})
	
	data['big'] += i
	data['bob'] += i
	jdata = json.dumps(data)
	
	
	#msg = json.loads(jdata)
	#print 'decoded: ',msg
	
	s.send(jdata)
	time.sleep(0.010)

for i in range(0,100):
	#ret, img = cap.read() 
	img_jpg = cv2.imencode('.jpg',img)[1]
	print img_jpg.shape
	img64 = base64.b64encode( img_jpg )
	print 'base64 string size:',len(img64)
	s.send( json.dumps( dict({'image': img64}) ) )
	#time.sleep(2)
	cv2.waitKey(10)

s.send( json.dumps({'quit': True}) )
s.close()