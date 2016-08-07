#!/usr/bin/env python

import logging


class Module(object):
	"""
	Sets up the logger and stores the intent of the module.
	"""
	def __init__(self, mod_name='none'):
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')
		self.intent = mod_name
		self.logger.info('[+] Init module {0!s}'.format((self.intent)))

	def handleIntent(self, intent):
		"""
		Returns True if the intent passed matches the intent of this module.
		"""
		ans = False
		if self.intent == intent:
			ans = True
		return ans
