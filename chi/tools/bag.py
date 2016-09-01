#!/usr/bin/env python
#
#
# copyright Kevin Walchko
#
# Basically a rosbag library

from __future__ import print_function
import os
import sys
import logging
# import argparse
import gzip  # compression
import multiprocessing as mp
import time  # filename date/time
import six  # Py2/3 is a string

sys.path.insert(0, os.path.abspath('..'))
import lib.zmqclass as Zmq
import lib.Messages as Msg  # deserialize topics

# useful to turn off for debugging
use_compression = True


class Bag(object):
	"""
	Save messages to a file based on their topic name. It also uses gzip to
	compress the file.
	in: buffer size, default is 100 messages
	"""
	def __init__(self, buffer_size=100):
		"""
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
		if topic.rfind('.bag') > 0: filen = path + topic
		else: filen = path + topic + '.bag'

		if use_compression: self.fd = gzip.open(filen, "w")
		else: self.fd = open(filen, "w")

	def close(self):
		self.flush()
		self.fd.close()

	def push(self, msg):
		"""
		Push another message to the buffer and grab time stamp for play back
		"""
		dmsg = {'ts': time.time(), 'msg': msg}
		self.buffer.append(dmsg)

		if len(self.buffer) >= self.buffer_size:
			self.writeToFile()

	def writeToFile(self):
		if self.fd is None:
			print('Error: please open file first')
			return

		for m in self.buffer:
			sm = self.serialize(m)
			self.fd.write(sm + '\n')
		# print 'Wrote {} files'.format(len(self.buffer))
		self.buffer = []

	@staticmethod
	def readFromFile(file):
		ans = []
		try:
			if use_compression:
				with gzip.open(file, 'r') as f:
					for line in f:
						# print('>', line)
						m = Msg.deserialize(line)
						ans.append(m)
			else:
				with open(file, 'r') as f:
					for line in f:
						# print('>', line)
						m = Msg.deserialize(line)
						ans.append(m)
			# print 'Read {} files from {}'.format(len(ans), file)
		except:
			print('Could not read file: {}'.format(file))
			raise

		return ans


# not sure if these should be object or mp.Process
class Record(object):
	def __init__(self):
		# mp.Process.__init__(self)

		# if host is None:
			# host = socket.gethostbyname(socket.gethostname())
		# self.host = host
		# self.port = port
		# self.topic = topic
		# logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger(__name__).addHandler(logging.NullHandler())

	def run(self, topic, port=9000, host='localhost', path=None):
		tcp = (host, port)
		sub = Zmq.Sub(topic, tcp)

		# make sure path is a good file name ending in .bag
		if not path or not isinstance(path, six.string_types):
			t = time.ctime().replace(' ', '_')
			filename = './' + topic + t + '.bag'
		elif path.rfind('.bag') == -1 and isinstance(path, six.string_types):
			filename = path + '.bag'
		else:
			filename = path

		bag = Bag()
		bag.open(filename)
		count = 0

		try:
			while True:
				topic, msg = sub.recv()
				if msg:
					bag.push(msg)
					count += 1
					if count % 100 == 0:
						print('Recorded {} message'.format(count))

		except (IOError, EOFError):
			print('[-] Connection gone .... bye')
			return


class Play(object):
	def __init__(self):
		# mp.Process.__init__(self)

		# self.tcp = ('localhost', self.port)
		# self.topic = topic
		# self.bag = bag
		# logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger(__name__).addHandler(logging.NullHandler())

	def run(self, filename, topic, port=9000, loop=True):
		tcp = ('localhost', port)
		pub = Zmq.Pub(tcp)

		msgs = []
		bag = Bag()
		try:
			msgs = bag.readFromFile(filename)
		except Exception as e:
			self.logger.error('[-] Could not open file {}'.format(filename))
			raise

		try:
			length = len(msgs)
			print('Found {} msgs in {}'.format(length, filename))

			# set it up to run
			save_msg = msgs[0]
			old_time = save_msg['ts']
			msg_time = old_time
			msg = save_msg['msg']
			index = 1

			# FIXME: 20160827 - this doesn't loop correctly, it crashes when it gets to the end
			while True:
				time.sleep(msg_time - old_time)

				# fix time stamp in message
				if 'stamp' in msg:
					msg['stamp'] = time.time()

				pub.pub(topic, msg)
				# print('pub:', msg)
				# print('msgs[0]:', msgs[0])
				save_msg = msgs[index]

				# setup times for sleep
				old_time = msg_time
				msg_time = save_msg['ts']
				msg = save_msg['msg']

				index += 1
				if index == length:
					if loop:
						print("Loop!!")
						index = 0
					else:
						self.logger.info('End of File')
						return

		except Exception as e:
			self.logger.error(e)
			bag.close()
			raise


if __name__ == '__main__':
	print('hello cowboy')
