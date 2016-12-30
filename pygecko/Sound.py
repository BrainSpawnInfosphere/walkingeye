#!/usr/bin/env python

from __future__ import print_function
import pygecko.lib.ZmqClass as zmq
import pygecko.lib.Sound as Audio
from pygecko.lib.TTS import TTS


class SoundsServer(object):
	def __init__(self):
		self.tts = TTS()
		self.tts.setOptions('-v Karen')  # this works on macOS and say

		self.audio = Audio()

	def run(self, topics, port=9000):
		try:
			sub = zmq.Sub(topics=topics, connect_to=('localhost', port))
			print('[>] {} subscribed to {} on {}:{}'.format('SoundsServer', topics, 'localhost', port))
			while True:
				topic, msg = sub.recv()
				if msg:
					if topic == 'text':
						print('tts: {}'.format(msg['txt']))
						self.tts.say(msg['txt'])
					elif topic == 'sound':
						print('sound: {}'.format())
						self.audio.play(msg['file'])

		except (IOError, EOFError):
			print('[-] Connection gone .... bye')
			sub.close()
			return


def main():
	snd = SoundsServer()

	try:
		snd.run(topics=['text', 'speech'], port=9010)

	except KeyboardInterrupt:
		pass

	print('{} exiting'.format(__name__))


if __name__ == '__main__':
	main()
