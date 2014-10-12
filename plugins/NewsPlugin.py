#!/usr/bin/env python

from Module import *


####################################################################
# 
# 
####################################################################
class Plugin(Module):
	def __init__(self):
		Module.__init__(self,'news')
		self.intent = 'news'
			
	def process(self, entity):
		return 'News module is not  implemented yet'
		



if __name__ == '__main__':
	n = Plugin()
	print n.process(0)
	