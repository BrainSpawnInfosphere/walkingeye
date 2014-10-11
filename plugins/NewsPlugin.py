#!/usr/bin/env python

from Module import *


####################################################################
# 
# 
####################################################################
class Plugin(Module):
	def __init__(self):
		self.intent = 'news'
			
	def process(self, entity):
		return 'News module is not  implemented yet'
		



if __name__ == '__main__':
	print 'bye ...'
	