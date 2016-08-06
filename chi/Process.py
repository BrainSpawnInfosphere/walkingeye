#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import logging
import multiprocessing as mp

"""
Not using this yet ... not sure there is a need

sets up:
- multi processing (little no advantage)
- logging (very small advantage)
"""


class Process(mp.Process):
	def __init__(self, loglevel=logging.ERROR):
		mp.Process.__init__(self)
		logging.basicConfig(level=loglevel)
		self.logger = logging.getLogger(__name__)

	def run(self):
		self.logger.error('{} needs to redefine Process.run()', __name__)

if __name__ == "__main__":
	print('hello')
