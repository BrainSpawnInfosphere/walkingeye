#!/usr/bin/env python


import cv2
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
# import BaseHTTPServer
# import StringIO
import time
import logging
import platform
import picamera
import picamera.array

class Camera(object):
	def __init__(self, cam=None):
		if not cam:
			os = platform.system().lower() # grab OS name and make lower case
			if os == 'linux': cam = 'pi'
			else: cam = 'cv'
			
		if cam == 'pi':
			self.cameraType = 'pi' # picamera
			self.camera = picamera.PiCamera()
		else:
			self.cameraType = 'cv' # opencv
			self.camera = cv2.VideoCapture()
			# need to do vertical flip?

		time.sleep(1) # let camera warm-up

	def __del__(self):
		# the red light should shut off
		if self.cameraType == 'pi': self.camera.close()
		else: self.camera.release()

		print 'exiting camera ... bye!'
		# exit()

	def init(self, cam=0, win=(640,480)):
		if self.cameraType == 'pi':
			self.camera.vflip = True # camera is mounted upside down
			self.camera.resolution = win
			self.bgr = picamera.array.PiRGBArray(self.camera,size=win)
		else:
			self.camera.open(0)
			self.camera.set(3, win[0]);
			self.camera.set(4, win[1]);
		# self.capture.set(cv2.cv.CV_CAP_PROP_SATURATION,0.2);

	def read(self):
		if self.cameraType == 'pi':
			self.camera.capture(self.bgr, format='bgr', use_video_port=True)
			gray = cv2.cvtColor(self.bgr.array, cv2.COLOR_BGR2GRAY)
			self.bgr.truncate(0) # clear stream
			print 'got image'
			return True, gray
		else:
			ret,img = self.camera.read()
			if not ret:
				return False
			# imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			return True, gray

def compress(orig,comp):
	return float(orig)/float(comp)

class mjpgServer(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path.endswith('.mjpg'):
			# self.wfile.write('pic')
			# return


			self.send_response(200)
			self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
			self.end_headers()
			capture = Camera()
			capture.init(0,(320,240))
			# tmpFile = StringIO.StringIO()
			while True:
				# try:

				ret,img = capture.read()
				if not ret:
					continue
				# jpg = Image.fromarray(img)
				# tmpFile = StringIO.StringIO()
				# jpg.save(tmpFile,'JPEG')
				# print 'image',img.shape
				ret, jpg = cv2.imencode('.jpg',img)
				# print 'jpeg',jpg.shape
				# cv2.imshow('tt',jpg)
				# print len(jpg)
				# print dir(jpg)
				# print type(jpg)
				# print jpg
				print 'Compression ratio: %d4.0:1'%(compress(img.size,jpg.size))
				# tmpFile.write(jpg.tostring())
				self.wfile.write("--jpgboundary")
				self.send_header('Content-type','image/jpeg')
				# self.send_header('Content-length',str(tmpFile.len))
				self.send_header('Content-length',str(jpg.size))
				self.end_headers()
				# self.wfile.write(tmpFile.getvalue())
				self.wfile.write(jpg.tostring())
				time.sleep(0.05)
				# tmpFile.close()

				# except KeyboardInterrupt:
				# 	print 'Press Ctrl-C to exit or reload your browser to start again'
				# 	# tmpFile.close()
				# 	break
			return

		if self.path.endswith('.html'):
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<h1>http://127.0.0.1:8080/cam.html</h1>')
			self.wfile.write('<img src="http://192.168.1.71:9000/camera.mjpg"/>')
			self.wfile.write('</body></html>')
			return

		else:
			self.send_response(404)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<h1>File not found</h1>')
			self.wfile.write('</body></html>')

def main():
	try:
		server = HTTPServer(('192.168.1.71',9000),mjpgServer)
		# server = ThreadedHTTPServer(('localhost',8080),mjpgServer)
		# BaseHTTPServer.test(mjpgServer, ThreadedHTTPServer)
		print "server started"
		server.serve_forever()
		# while run():
		# 	server.handle_request()
		# 	print run
	except KeyboardInterrupt:
		print 'main interrupt'
		server.socket.close()

if __name__ == '__main__':
	main()
