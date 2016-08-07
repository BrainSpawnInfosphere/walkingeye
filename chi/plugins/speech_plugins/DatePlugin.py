#!/usr/bin/env python

# from Module import *
import Module as mod
import time


class Plugin(mod.Module):
	"""
	Returns the current date
	"""
	def __init__(self):
		self.intent = 'date'
		mod.Module.__init__(self, 'date')

	def process(self, entity):
		t = time.localtime()
		day = t[2]
		months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		mon = months[t[1] - 1]
		yr = t[0]
		resp = 'The date is {0:d} {1!s} {2:d}'.format(day, mon, yr)
		return resp


if __name__ == '__main__':
	p = mod.Plugin()
	print p.process(0)
