#!/usr/bin/env python
##############################################
# The MIT License (MIT)
# Copyright (c) 2016 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function
# import pygecko.lib.ZmqClass as zmq
from pygecko.lib import pyWit
from pygecko.lib import TTS

import random


# maybe switch to this???
class Plugin(object):
	def handle(self):
		return False


class Greeting(Plugin):
	def __init__(self):
		self.tts = TTS()
		self.answer = ['hi', 'hello', 'good day']

	def handle(self):
		self.tts.say(random.choice(self.answer))
		return True


def greeting():
	tts = TTS()
	tts.say('hello')


def movie_sounds():
	print('I like them too')


act = {
	'greeting': greeting,
	'tv_movie_sounds': movie_sounds
}


def main():
	pw = pyWit()

	try:
		pw.run(topics=['keyboard', 'audio'], port=9010, actions=act)

	except KeyboardInterrupt:
		pass

	print('[<] {} exiting'.format('pywitServer'))


if __name__ == '__main__':
	main()
