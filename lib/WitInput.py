#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
# import json
import wit
import sox
import logging


class WitInputError(Exception):
	pass


class WitInput(object):
	def __init__(self, token, logger=None):
		self.wit = wit.Wit(token)
		self.mic = sox.Microphone()
		self.logger = logger or logging.getLogger(__name__)

	def text(self, text):
		"""
		Will grab text from keyboard and process the wit.ai json message
		in: text
		out: dict {intent, [entities]}, return value (True/False)
		"""
		# self.logger.debug('text()')
		# try:
		ans = self.wit.message(text)
		self.logger.debug(ans)
		return ans

	def listenPrompt(self):
		"""
		Will grab audio from microphone and process the wit.ai json message
		in: nothing
		out: dict {intent, [entities]}, return value (True/False)
		"""
		result = {}
		result['intent'] = ''

		while(result['intent'] != 'attention'):
			# print '--------'
			result = self.listen()
			# print '/////',result
			print(result)

		return self.listen(True)

	def listen(self, confidence=0.7):
		"""
		Will grab audio from microphone and process the wit.ai json message
		in: nothing
		out: dict {intent, [entities]}
		"""
		try:
			# result = wit.voice_query_auto( self.wit_token )
			# if ps: self.playSound('../sounds/misc/beep_hi.wav')
			print('Speak')
			self.mic.getAudio()
			kv = self.wit.speech(self.mic.audio)
			ans = self.getKey(kv, confidence)
			print('Got: %s' % ans)
			# if ps: self.playSound('../sounds/misc/beep_lo.wav')
			return ans
		except:
			raise WitInputError('Error: listen()')

	def getKey(self, msg, confidenceLevel):
		"""
		Gets intent from msg and handles errors
		in: wit.ai message as a dict
		out: dict {intent, [entities]}
		"""
		# pp.pprint( msg )

		key = 'error'
		ent = []
		cl = -1.0

		# print type(msg)

		# hangle errors ----------------------------
		if not msg:
			self.logger.debug('<< no msg >>')
			# key = 'error'
		elif 'outcomes' not in msg:
			self.logger.debug('no outcome')
			# key = 'error'
		elif len(msg['outcomes']) == 0:
			self.logger.debug('outcome empty')
		elif msg['outcomes'][0]['intent']:  # FIXME: 20150304, assume [0] is highest outcome for now
			if msg['outcomes'][0]['confidence'] > confidenceLevel:
				key = msg['outcomes'][0]['intent']
				ent = msg['outcomes'][0]['entities']
				cl = msg['outcomes'][0]['confidence']

		ans = {}
		ans['intent'] = key
		ans['entities'] = ent
		ans['confidence'] = cl

		return ans


def main():
	import os
	token = os.getenv('WIT')
	w = WitInput(token)

	while True:
		txt = raw_input(">> ")
		resp = w.text(txt)
		print('>>', resp)
		print('listening')
		resp = w.listen()
		print('heard:', resp)


if __name__ == "__main__":
	main()
