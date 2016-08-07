#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import logging


class Module(object):
	"""
	Sets up the logger and stores the intent of the module.
	"""
	def __init__(self, mod_name='none'):
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')
		self.name = mod_name
		self.intent = None
		self.logger.info('[+] Init module {0!s}'.format((self.intent)))

	def handleIntent(self, intent):
		"""
		Returns True if the intent passed matches the intent of this module.
		"""
		ans = False
		if self.intent == intent:
			ans = True
		return ans

	def process(self, input):
		pass
