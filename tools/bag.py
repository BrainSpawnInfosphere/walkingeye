#!/usr/bin/env python
#
#
# copyright Kevin Walchko
#
# Basically a rosbag

# import time
import os
import sys
import logging
import argparse
# import json
import socket
import gzip
import multiprocessing as mp
sys.path.insert(0, os.path.abspath('..'))

import lib.zmqclass as Zmq
import lib.Messages as Msg


class Bag(object):
	"""
	Save messages to a file based on their topic name. It also uses gzip to
	compress the file.
	in: buffer size, default is 100 messages
	"""
	def __init__(self, buffer_size=100):
		"""
		in: topic - name of topic to capture
		    path - path to save file to, default is ./
		"""
		self.buffer = []
		self.serialize = Msg.serialize
		self.fd = None
		self.buffer_size = buffer_size

	def __del__(self):
		self.close()
		print('Bag exiting')

	def flush(self):
		"""
		Write any data in the buffer to the file.
		"""
		if len(self.buffer) > 0:
			self.writeToFile()

	def open(self, topic, path='./'):
		file = path + topic + '.bag'
		self.fd = gzip.open(file, "w")
		# self.fd = open(file, "w")

	def close(self):
		self.flush()
		self.fd.close()

	def push(self, msg):
		"""
		Push another message to the buffer
		"""
		self.buffer.append(msg)

		if len(self.buffer) >= self.buffer_size:
			self.writeToFile()

	def writeToFile(self):
		if self.fd is None:
			print 'Error: please open file first'
			return

		for m in self.buffer:
			sm = self.serialize(m)
			self.fd.write(sm + '\n')
		# print 'Wrote {} files'.format(len(self.buffer))
		self.buffer = []

	def readFromFile(self, file):
		ans = []
		try:
			with gzip.open(file, 'r') as f:
			# with open(file, 'r') as f:
				for line in f:
					# print '>', line
					m = Msg.deserialize(line)
					ans.append(m)
			# print 'Read {} files from {}'.format(len(ans), file)
		except:
			print 'Could not read file: {}'.format(file)

		return ans


class BagServer(mp.Process):
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

		bag = Bag()
		bag.open(self.topic)

		try:
			while True:
				# pub.pub(topic, msg)
				topic, msg = sub.recv()
				if msg: bag.push(msg)
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
	  bag 'imu' -p '../save_stuff'
	""")

	parser.add_argument('info', nargs=3, help='address port topic, ex. 1.1.1.1 9000 imu')
	# parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
	parser.add_argument('-p', '--path', help='path to same topic bag file to', default='./')
	args = vars(parser.parse_args())
	return args


def main():
	args = handleArgs()
	print args
	info = args['info']
	srv = BagServer(info[2], info[1], info[0])
	srv.start()


def test_bag():
	import random
	import os
	bag = Bag()
	bag.open('imu')

	num_msg = 105

	for i in range(0, num_msg):
		msg = Msg.Vector()
		msg.update(x=random.uniform(-3, 3), y=random.uniform(10, 50), z=random.uniform(-20, 5))
		bag.push(msg)
	bag.close()

	filename = 'imu.bag'
	ans = bag.readFromFile('imu.bag')
	# os.remove(filename)
	# print 'Found {} messages in file {}'.format(len(ans), filename)
	# print 'type:', type(ans[0])
	# print ans[0]
	assert len(ans) == num_msg and isinstance(ans[0], dict)

if __name__ == '__main__':
	main()
	# test_bag()
