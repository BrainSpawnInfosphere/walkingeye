#!/usr/bin/env python

import Module as mod
import time


class Plugin(mod.Module):
	def __init__(self):
		mod.Module.__init__(self, 'time')
		self.intent = 'time'

	def process(self, entity):
		"""
		Grabs the local time
		"""
		t = time.localtime()
		hrs = t[3]
		if hrs > 12:
			hrs = hrs - 12
			ampm = 'pm'
		else:
			ampm = 'am'
		mins = t[4]
		resp = 'The current time is %d %d %s' % (hrs, mins, ampm)
		return resp


if __name__ == '__main__':
	t = mod.Plugin()
	print t.process(0)
	print 'bye ...'
