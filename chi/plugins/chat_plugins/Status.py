#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import Module as mod


class Plugin(mod.Module):
	def __init__(self):
		mod.Module.__init__(self, 'status')
		# self.intent = 'command'
		self.intent = ['power', 'ping', 'servos']

	def handleIntent(self, intent):
		"""
		Returns True if the intent passed matches the intent of this module.
		"""
		ans = False
		for key in self.intent:
			if key == intent:
				ans = True
				break
		return ans

	def getNumber(self, number):
		try: speed = float(number)
		except: speed = 0.0  # not sure best solution here
		return speed

	def process(self, input):
		"""

		"""
		words = input.split()
		resp = None

		key = words[0]
		if key == 'power': resp = 'good to go!'
		elif key == 'ping': resp = 'ping: 00.2 sec'
		elif key == 'servos': resp = 'yes i have servos'

		return resp


if __name__ == '__main__':
	print('Hello space cowboy!')
