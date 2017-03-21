#!/usr/bin/env python
#
# Ultimately I want this to be all (or most of) the high level logic for the
# robot.
#
from __future__ import print_function
from __future__ import division


class Brain(object):
	"""
	FSM
	"""
	states = ['normal', 'bored', 'sit', 'stand']
	curr_state = 'normal'
	next_state = 'normal'

	def __init__(self):
		pass

	def findBall(self, img):
		pass

	def update(self, cmd, ir, compass):
		if self.curr_state is 'normal':
			self.curr_state = 'normal'
		return cmd


if __name__ == "__main__":
	b = Brain()
