#!/usr/bin/env python


from pygecko.lib.ZmqClass import Sub as zmqSub
from pygecko.lib.ZmqClass import Pub as zmqPub
from pygecko.lib import Messages as Msg
import multiprocessing as mp


class Brain(mp.Process):
	states = ['normal', 'bored', 'sit', 'stand']
	curr_state = 'normal'
	next_state = 'normal'

	def __init__(self):
		mp.Process.__init__(self)
		self.range = []

	def update(self):
		cmd = (0, 0, 0)
		if self.curr_state is 'normal':
			self.curr_state = 'normal'
		return cmd

	def run(self):
		pub_cmd = zmqPub(('0.0.0.0', 8500))
		sub_ir = zmqSub(['ir'], ('0.0.0.0', 8100))
		while True:
			topic, msg = sub_ir.recv()
			if msg:
				if topic is 'ir':
					self.range = msg.range
			self.update()
			pub_cmd.pub(['cmd'], (0, 0, 0))
