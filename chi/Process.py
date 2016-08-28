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
		# self.logger = logging.getLogger(__name__).addHandler(logging.NullHandler())
		mp.log_to_stderr()
		self.logger = mp.get_logger()
		self.logger.info('constructor')

	def __del__(self):
		self.logger.info('{} is shutting down', mp.current_process().name)

	def run(self):
		self.logger.error('{} needs to redefine Process.run()', mp.current_process().name)

class myProcess(Process):
	def __init__(self, loglevel):
		Process.__init__(self, loglevel)
		self.logger.info('myProcess::constructor')
		# print('hello my process')
	#
	# def __del__(self):
	# 	print('my process out!')

	# def run(self):
	# 	print('run')

if __name__ == "__main__":
	mp = myProcess(logging.INFO)
	mp.start()
	mp.join()
