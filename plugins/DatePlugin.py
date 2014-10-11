#!/usr/bin/env python

from Module import *
import time



####################################################################
# 
# 
####################################################################
class Plugin(Module):
	def __init__(self):
		self.intent = 'date'
		Module.__init__(self,'date')
		
	"""
	"""
	def process(self, entity):
		t = time.localtime()
		day = t[2]
		months = ['January', 'February','March','April','May','June','July','August','September','October','November','December']
		mon = months[t[1]-1]
		yr = t[0]
		resp = 'The date is %d %s %d'%(day,mon,yr)
		return resp



if __name__ == '__main__':
	p = Plugin()
	print p.process(0)
	