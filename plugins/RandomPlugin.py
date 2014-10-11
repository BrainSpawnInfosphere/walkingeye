#!/usr/bin/env python

from Module import *
import random


####################################################################
# 
# 
####################################################################
class Plugin(Module):
	def __init__(self):
		Module.__init__(self,['greeting','feelings','error','joke','mean'])
		self.intent = ['greeting','feelings','error','joke','mean']
		
		# get canned responces
		f = open( self.info['response_path'] )
		self.msglist = yaml.safe_load(f)
		f.close()
		
	"""
	"""
	def handleIntent(self,intent):
		for i in self.intent:
			if i == intent:
				self.save_intent = intent
				return True
		
		return False
			
	"""
	"""
	def process(self, entity):
		resp = random.choice( self.msglist[self.save_intent] )
		self.save_intent = ''
		return resp




if __name__ == '__main__':
	print 'bye ...'
	