#!/usr/bin/env python

import Module as mod
import random
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import lib.FileStorage as Fs


class Plugin(mod.Module):
	"""
	"""

	msglist = {}

	def __init__(self, config_file='./config/responce.json'):
		mod.Module.__init__(self, ['greeting', 'feelings', 'error', 'joke', 'mean'])
		fs = Fs.FileStorage()
		fs.readJson(config_file)
		self.msglist = fs.db

	def handleIntent(self, intent):
		if intent in self.intent:
			self.save_intent = intent
			return True
		return False

	def process(self, entity):
		resp = random.choice(self.msglist[self.save_intent])
		self.save_intent = ''
		return resp


if __name__ == '__main__':
	r = Plugin()
	r.handleIntent('greeting')
	print r.process(0)
