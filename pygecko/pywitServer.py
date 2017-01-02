#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
from pygecko.lib import pyWit
from pygecko.lib import TTS
from pygecko.lib import ZmqClass as zmq
import random
import time
import multiprocessing as mp		# multiprocessProcess

# maybe switch to this???
# import random
# class Plugin(object):
# 	def handle(self):
# 		return False
#
#
# class Greeting(Plugin):
# 	def __init__(self):
# 		self.tts = TTS()
# 		self.answer = ['hi', 'hello', 'good day']
#
# 	def handle(self):
# 		self.tts.say(random.choice(self.answer))
# 		return True


class pyWitServer(mp.Process):
	wit = None

	def __init__(self):
		mp.Process.__init__(self)

	def init(self, topics, port, actions, confidence_level=0.6):
		self.actions = actions
		self.confidence_level = confidence_level

		self.wit = pyWit()

		self.sub = zmq.Sub(topics=topics, connect_to=('0.0.0.0', port))
		print('[>] {} subscribed to {} on {}:{}'.format('pywitServer', topics, 'localhost', port))

	def run(self):
		if not self.wit:
			Exception('You must call pyWitServer::init() first!')
		# sub = zmq.Sub(topics=self.topics, connect_to=('0.0.0.0', self.port))
		# print('[>] {} subscribed to {} on {}:{}'.format('pywitServer', self.topics, 'localhost', self.port))

		try:
			# tts = TTS()
			while True:
				topic, msg = self.sub.recv()  # this blocks

				# msg = {'message': 'hello'}  # debug
				# msg = {'message': 'what is the time'}  # debug

				if msg:
					intent = None
					confidence = 0.0
					if 'message' in msg:
						intent, confidence, ent = self.wit.message(msg['message'])
						# print('wit intent', intent, confidence)

					elif 'wav' in msg:
						intent, confidence, ent = self.wit.speech(msg['wav'])

					if intent and (confidence >= self.confidence_level):
						if intent in self.actions:
							func = self.actions[intent]
							func()

				time.sleep(2)

		except KeyboardInterrupt:
			print('{} exiting now'.format('pywitServer'))
			raise


tts = TTS()


def greeting():
	answer = [
		'hi',
		'hello',
		'good day',
		'yo yo yo',
		'ola'
	]
	tts.say(random.choice(answer))


def movie_sounds():
	print('I like them too')


def get_time():
	t = time.localtime()
	hrs = t[3]
	if hrs > 12:
		hrs = hrs - 12
		ampm = 'pm'
	else:
		ampm = 'am'
	mins = t[4]
	resp = 'The current time is {0:d} {1:d} {2!s}'.format(hrs, mins, ampm)

	tts.say(resp)


act = {
	'greeting': greeting,
	'tv_movie_sounds': movie_sounds,
	'time': get_time
}


def main():
	# tts.say('here we go')
	pw = pyWitServer()
	pw.init(topics=['keyboard', 'audio'], port=9010, actions=act)
	pw.start()
	# pw.join()


if __name__ == '__main__':
	main()
