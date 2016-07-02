#!/usr/bin/env python


import cv2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from socket import gethostname, gethostbyname
# import BaseHTTPServer
# import StringIO
import time
# import logging
import platform
import argparse

if platform.system().lower() == 'linux':
	import picamera
	import picamera.array


class Camera(object):
	"""
	Generic camera object that can switch between OpenCv in PiCamera.
	"""
	def __init__(self, cam=None, num=0):
		self.cal = None

		if not cam:
			os = platform.system().lower()  # grab OS name and make lower case
			if os == 'linux': cam = 'pi'
			else: cam = 'cv'

		if cam == 'pi':
			self.cameraType = 'pi'  # picamera
			self.camera = picamera.PiCamera()
		else:
			self.cameraType = 'cv'  # opencv
			self.cameraNumber = num
			self.camera = cv2.VideoCapture()
			# need to do vertical flip?

		time.sleep(1)  # let camera warm-up

	def __del__(self):
		# the red light should shut off
		if self.cameraType == 'pi': self.camera.close()
		else: self.camera.release()

		print 'exiting camera ... bye!'

	def init(self, win=(640, 480)):
		if self.cameraType == 'pi':
			self.camera.vflip = True  # camera is mounted upside down
			self.camera.resolution = win
			self.bgr = picamera.array.PiRGBArray(self.camera, size=win)
		else:
			self.camera.open(self.cameraNumber)
			self.camera.set(3, win[0])
			self.camera.set(4, win[1])
		# self.capture.set(cv2.cv.CV_CAP_PROP_SATURATION,0.2);

	def setCalibration(self, n):
		self.cal = n

	def read(self):
		gray = 0

		if self.cameraType == 'pi':
			self.camera.capture(self.bgr, format='bgr', use_video_port=True)
			gray = cv2.cvtColor(self.bgr.array, cv2.COLOR_BGR2GRAY)
			self.bgr.truncate(0)  # clear stream
			# print 'got image'
			# return True, gray
		else:
			ret, img = self.camera.read()
			if not ret:
				return False
			# imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			# return True, gray

		if self.cal:  # FIXME 2016-05-15
			print 'do calibration correction ... not done yet'

		return True, gray

	def isOpen(self):
		return True  # FIXME 2016-05-15


def compress(orig, comp):
	return float(orig) / float(comp)


class mjpgServer(BaseHTTPRequestHandler):
	cam = None

	def do_GET(self):
		print 'connection from:', self.address_string()
		if self.path.find('.mjpg') > 0:
			self.send_response(200)
			self.send_header(
				'Content-type',
				'multipart/x-mixed-replace; boundary=--jpgboundary'
			)
			self.end_headers()

			if self.cam is None:
				print 'Error, you need to initialize the camera first'
				return

			capture = self.cam

			if not capture.isOpen():
				capture.init((320, 240))
			# tmpFile = StringIO.StringIO()
			while True:
				# try:

				ret, img = capture.read()
				if not ret:
					continue
				# jpg = Image.fromarray(img)
				# tmpFile = StringIO.StringIO()
				# jpg.save(tmpFile,'JPEG')
				# print 'image',img.shape
				ret, jpg = cv2.imencode('.jpg', img)
				# print 'Compression ratio: %d4.0:1'%(compress(img.size,jpg.size))
				self.wfile.write("--jpgboundary")
				self.send_header('Content-type', 'image/jpeg')
				# self.send_header('Content-length',str(tmpFile.len))
				self.send_header('Content-length', str(jpg.size))
				self.end_headers()
				# self.wfile.write(tmpFile.getvalue())
				self.wfile.write(jpg.tostring())
				time.sleep(0.05)
				# tmpFile.close()
			return

		if self.path == '/':
			# hn = self.server.server_address[0]
			# pt = self.server.server_address[1]
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<h1>http://{0!s}:{1!s}/cam.html</h1>'.format(*self.server.server_address))
			self.wfile.write('<img src="http://{0!s}:{1!s}/camera.mjpg"/>'.format(*self.server.server_address))
			self.wfile.write('<p>{0!s}</p>'.format((self.version_string())))
			self.wfile.write('</body></html>')
			return

		else:
			print 'error', self.path
			self.send_response(404)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('<html><head></head><body>')
			self.wfile.write('<h1>{0!s} not found</h1>'.format(self.path))
			self.wfile.write('</body></html>')


def handleArgs():
	parser = argparse.ArgumentParser(description='A simple mjpeg server Example: mjpeg-server -p 8080 --camera 4')
	parser.add_argument('-p', '--port', help='port, default is 9000', type=int, default=9000)
	parser.add_argument('-c', '--camera', help='set opencv camera number, ex. -c 1', type=int, default=0)
	parser.add_argument('-t', '--type', help='set type of camera: cv or pi, ex. -t pi', default='cv')
	parser.add_argument('-s', '--size', help='set size', nargs=2, type=int, default=(320, 240))

	args = vars(parser.parse_args())
	args['size'] = (args['size'][0], args['size'][1])
	return args


def main():
	args = handleArgs()
	print args['size']
	# exit()

	try:
		camera = Camera()  # need to figure a clean way to pass this ... move switching logic here?
		camera.init(args['size'])
		mjpgServer.cam = camera

		server = HTTPServer((gethostname(), args['port']), mjpgServer)
		print "server started"
		server.serve_forever()

	except KeyboardInterrupt:
		print 'main interrupt'
		server.socket.close()

if __name__ == '__main__':
	main()
	
