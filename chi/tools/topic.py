#!/usr/bin/env python
#
#
# copyright Kevin Walchko
#
# Basically a rostopic

import time
import os
import sys
import logging
import argparse
import json
import socket
import multiprocessing as mp
sys.path.insert(0, os.path.abspath('..'))

import lib.zmqclass as Zmq
import lib.Messages as Msg


class TopicPub(mp.Process):
	def __init__(self, topic, msg, rate=1, port=9000):
		mp.Process.__init__(self)
		self.host = socket.gethostbyname(socket.gethostname())
		self.port = port
		self.topic = topic
		self.msg = msg
		self.rate = rate

		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')

	def run(self):
		tcp = (self.host, self.port)
		pub = Zmq.Pub(tcp)
		msg = self.msg
		topic = self.topic
		dt = 1
		if self.rate != 0:
			dt = 1.0 / self.rate

		try:
			while True:
				pub.pub(topic, msg)
				print '[>]', topic, ':', msg
				time.sleep(dt)  # 1/2 second sleep

		except (IOError, EOFError):
			print '[-] Connection gone .... bye'
			return

		except KeyboardInterrupt:
			print '[-] User hit Ctrl-C keyboard .... bye'
			exit()  # not cleanly exiting


class TopicSub(mp.Process):
	def __init__(self, topic, port=9000, host=None):
		mp.Process.__init__(self)

		if host is None:
			host = socket.gethostbyname(socket.gethostname())
		self.host = host
		self.port = port
		self.topic = topic
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')

	def run(self):
		tcp = (self.host, self.port)
		sub = Zmq.Sub(self.topic, tcp)

		try:
			while True:
				# pub.pub(topic, msg)
				topic, msg = sub.recv()
				if msg: print '[<]', topic, ':', msg
				# time.sleep(0.5)  # 1/2 second sleep

		except (IOError, EOFError):
			print '[-] Connection gone .... bye'
			return


def handleArgs():
	parser = argparse.ArgumentParser(description="""
	A simple zero MQ message tool. It will either publish messages on a specified
	topic or subscribe to a topic and print the messages.

	Format:
	  topic pub port topic message -r|-once
	  topic echo port topic

	Examples:
	  topic pub 9000 vo -m "{'hi': 3000}" -r 10
	  topic pub 9000 vo -m "{'hi': 3000}" --once
	  topic echo 9000 cmd
	""")

	parser.add_argument('type', help='publish messages or echo messages being published by another node, eg: pub or echo')
	parser.add_argument('info', nargs=2, help='publish/subscribe messages to port topic, ex. 9000 "commands"')
	parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
	parser.add_argument('-r', '--rate', help='publish rate in Hz, ex. -r 10')
	parser.add_argument('-o', '--once', help='publish a message once and exit')
	parser.add_argument('-m', '--message', help='the message to publish, ex: -m "{"hi": 300, "ho": 4000}"')
	args = vars(parser.parse_args())
	return args


def main():
	args = handleArgs()
	print args
	#
	# msg = json.loads('{"hi": 100}')
	#
	# t = TopicPub('hi',msg,1,9000)
	# t.start()

	if args['type'] == 'pub':
		msg = args['message']
		rate = args['rate']
		topic = args['info'][1]
		port = args['info'][0]

		# clean up inputs
		if rate is None:
			rate = 1

		if msg is None:
			print 'You must supply a message for pub ... bye!'
			exit(1)
		try:
			msg = json.loads(msg)
		except:
			print 'Error converting your message to a dictionary for publishing ... bye'
			exit(1)

		t = TopicPub(topic, msg, rate, port)
		t.start()
	elif args['type'] == 'echo':  # FIXME 20160528 handle hosts other than localhost
		rate = args['rate']
		topic = args['info'][1]
		port = args['info'][0]

		# clean up inputs
		if rate is None:
			rate = 1

		t = TopicSub(topic, port)
		t.start()

	else:
		print 'Error: only pub or sub are support ... bye'
		exit(1)


if __name__ == '__main__':
	main()
