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
	"""
	Process base class - like a ros node
	"""
	def __init__(self, loglevel=logging.ERROR):
		mp.Process.__init__(self)
		logging.basicConfig(level=loglevel)
		# self.logger = logging.getLogger(__name__).addHandler(logging.NullHandler())
		mp.log_to_stderr()
		self.logger = mp.get_logger()
		self.logger.info('+ Process::constructor')

	def __del__(self):
		self.logger.info('+ Process::del')

	def run(self):
		self.logger.error('+ {} needs to redefine Process.run()', 'Process')


class myProcess(Process):
	def __init__(self, loglevel):
		Process.__init__(self, loglevel)
		self.logger.info('| myProcess::constructor')
		# print('hello my process')

	def __del__(self):
		# print('my process out!')
		# Process.__del__(self)  # error
		self.logger.info('| myProcess::del')

	def run(self):
		# print('run')
		self.logger.info('| myProcess::run')

if __name__ == "__main__":
	mp = myProcess(logging.INFO)
	mp.start()
	mp.join()
