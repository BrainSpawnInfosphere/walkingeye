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
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')
		self.intent = mod_name
		self.logger.info('[+] Init module %s'%(self.intent))
		
		# get parameters
		# does this get called everytime? Can i share, like static in C++?
		if not hasattr(self,'info'):
			file = '/Users/kevin/Dropbox/accounts.yaml'
			self.info = self.readYaml(file)
			#self.logger.info('[+] Loaded: %s'%(file))
	
	"""
	Read a yaml file and return the corresponding dictionary
	in: file name
	out: dict
	"""
	def readYaml(self,fname):
		f = open( fname )
		dict = yaml.safe_load(f)
		f.close()
		
		return dict
	
	"""
	"""
	def handleIntent(self,intent):
		ans = False
		if self.intent == intent:
			ans = True
		return ans