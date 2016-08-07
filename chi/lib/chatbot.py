#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import re
import logging
import os
import sys


class ChatbotError(Exception):
	pass


class Chatbot(object):
	def __init__(self, path="../chat_plugins/"):
		self.intents = []
		self.readPlugins(path)
		self.logger = logging.getLogger(__name__)

	def text(self, input):
		ans = self.search(input)
		if ans:
			return ans
		else:
			return 'Sorry, I did not understand'

	def readPlugins(self, path):
		"""
		Clears the current modules and reads in all plugins located in path
		in: path to plugins
		out: none
		"""
		# self.modules = {}
		self.modules = []
		sys.path.insert(0, path)
		for f in os.listdir(path):
			fname, ext = os.path.splitext(f)
			if ext == '.py' and fname != 'Module' and fname != '__init__':
				# print('file:', fname, ext)
				# self.logger.debug('found plugin response: ', fname)
				mod = __import__(fname)
				m = mod.Plugin()
				# self.modules[m.intent] = m
				# self.intents.append(m.intent)
				self.modules.append(m)
		sys.path.pop(0)

	def search(self, input):
		"""
		Searches through all plugins to find one that can process this intent
		in: struct{'intent': '', 'entities': ''}
		out: text (answer from plugin or '' if nothing could handle it)
		"""
		input_intent = input.split()[0]  # first word is always the intent!!!!
		ans = None
		for plugin in self.modules:
			# print('plugin:', plugin.intent)
			if plugin.handleIntent(input_intent):
				ans = plugin.process(input)
				# self.logger.debug('found plugin response: ' + txt)
		return ans

if __name__ == '__main__':
	t = Chatbot()
	print("type 'exit' to quit")
	print('-------------------------------')
	while True:
		txt = raw_input(">> ")
		if txt == 'exit': break
		print(t.text(txt))
	print('bye ...')
