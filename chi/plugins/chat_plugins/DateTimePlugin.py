#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import Module as mod
import time


class Plugin(mod.Module):
	def __init__(self):
		mod.Module.__init__(self, 'time_date')
		self.intent = ['time', 'date']

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

	def date(self):
		t = time.localtime()
		day = t[2]
		months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		mon = months[t[1] - 1]
		yr = t[0]
		resp = 'The date is {0:d} {1!s} {2:d}'.format(day, mon, yr)
		return resp

	def time(self):
		t = time.localtime()
		hrs = t[3]
		if hrs > 12:
			hrs = hrs - 12
			ampm = 'pm'
		else:
			ampm = 'am'
		mins = t[4]
		resp = 'The current time is {0:d} {1:d} {2!s}'.format(hrs, mins, ampm)
		return resp

	def process(self, input):
		"""
		Grabs the local time
		"""
		ans = None
		# print('input', input)
		if input == 'time': ans = self.time()
		elif input == 'date': ans = self.date()
		return ans


if __name__ == '__main__':
	print('hello space cowboy!')
