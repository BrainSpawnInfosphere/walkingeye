#!/usr/bin/env python

# this works but seems highly inefficient ... my system runs 80% w/ 2 cores
# just displaying a static web page
# although this might be the page --- canvas and two.js???

# for the webserver
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from socket import gethostname, gethostbyname
import os
import time

# for the server/client interface
import multiprocessing as mp
from zmqclass import *

class Kludge(mp.Process):
	"""
	This listens to zmq and passes into between zmq and the client webpage
	"""
	def __init__(self, topics, host="localhost",port=9000):
		mp.Process.__init__(self)
		self.host = host
		self.port = port
		
	def __del__(self):
		print 'Kludge says goodbye'

	def run(self):
		self.sub = Sub(['voice'])
		
		while True:
			time.sleep(3)
			msg = self.sub.recv()
			if msg:
				print msg


PORT=8800

# take a look at websockets:
# https://github.com/liris/websocket-client

class GetHandler(BaseHTTPRequestHandler):

	def error(self):
		return "<html><head><title>404</title></head><body><h1>404 File not Found</h1><br/>The file you requested was not found on the server</br></body></html>"

	def page(self):
		fd = open('node/head/face.htm','r')
		results = fd.read()
		fd.close()
		return results

	def do_GET(self):
		print 'Processing request: %s' % self.path
		if self.path == '/':
			response = self.page()
			self.send_response(200)
			self.end_headers()
			self.wfile.write(response)
		else:
			print "GetHandler doesn't support %s" % self.path
			response = self.error()
			self.send_response(404)
			self.end_headers()
			self.wfile.write(response)
			


if __name__ == '__main__':

	ipaddr = gethostbyname(gethostname())
	
	k = Kludge()
	k.start()

	print 'Starting server on '+str(ipaddr)+':'+str(PORT)+', use <Ctrl-C> to stop'
	server = HTTPServer(('0.0.0.0', PORT), GetHandler)
	server.serve_forever()
	
	k.join()