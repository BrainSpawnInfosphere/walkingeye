#!/usr/bin/env python

from Module import *
import time


####################################################################
# 
# 
####################################################################
class Plugin(Module):
	def __init__(self):
		Module.__init__(self,'time')
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
		resp = 'The current time is %d %d %s'%(hrs,mins,ampm)
		return resp


if __name__ == '__main__':
	t = Plugin()
	print t.process(0)
	print 'bye ...'
	