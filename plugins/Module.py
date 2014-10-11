#!/usr/bin/env python

import os
import logging
import yaml


####################################################################
# Base class
# 
####################################################################
class Module:
	"""
	"""
	def __init__(self,mod_name='none'):
		print 'Module init()'
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger(__name__)
		self.modName = mod_name
		self.logger.info('[+] Init module %s'%(self.modName))
		
		# get parameters
		# does this get called everytime? Can i share, like static in C++?
		f = open('/Users/kevin/Dropbox/accounts.yaml')
		self.info = yaml.safe_load(f)
		f.close()
		
	"""
	"""
	def handleIntent(self,intent):
		ans = False
		if self.intent == intent:
			ans = True
		return ans