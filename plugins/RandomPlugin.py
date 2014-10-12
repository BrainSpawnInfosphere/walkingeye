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
		
		# get canned responces
		self.msglist = self.readYaml( self.info['response_path'] )
		
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
	r = Plugin()
	r.handleIntent('greeting')
	print r.process(0)
	