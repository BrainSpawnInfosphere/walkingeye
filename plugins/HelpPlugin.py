#!/usr/bin/env python

from Module import *

####################################################################
# Help:
# Lists available commands, or describes a command in detail
# 
####################################################################
class Plugin(Module):
	def __init__(self):
		self.intent = 'help'
			
	def process(self, entity):
		return 'Help module is not implemented yet'




if __name__ == '__main__':
	print 'bye ...'
	