#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import Module as mod


class Plugin(mod.Module):
	def __init__(self):
		mod.Module.__init__(self, 'command')
		# self.intent = 'command'
		self.intent = ['forward', 'back', 'stop']

	def handleIntent(self, intent):
		"""
		Returns True if the intent passed matches the intent of this module.
		"""
		ans = False
		for key in self.intent:
			if key == intent:
				ans = True
				break
			# else:
				# print('not', key)

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
		if key == 'forward':
			if len(words) == 1: speed = 1.0
			else: speed = self.getNumber(words[1])
			resp = 'go - forward {}'.format(speed)
		elif key == 'back': resp = 'go - back'
		elif key == 'stop': resp = 'go - stop'

		return resp


if __name__ == '__main__':
	print('Hello space cowboy!')
