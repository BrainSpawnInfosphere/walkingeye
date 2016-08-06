#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
import os							# run commands and get/use path
import platform						# determine os
import sys							# ?
# import time							# sleep
import logging						# logging
import multiprocessing as mp		# multiprocess
import lib.zmqclass as zmq
import lib.FileStorage as fs
import lib.WitInput as wi


class SoundServer(mp.Process):
	"""
	"""
	# def __init__(self, YAML_FILE, REAL, stdin=os.fdopen(os.dup(sys.stdin.fileno())), host="localhost", port=9200):
	def __init__(self, wit_token, host="localhost", port=9200):
		mp.Process.__init__(self)
		self.host = host
		self.port = port
		logging.basicConfig(level=logging.DEBUG)
		self.logger = logging.getLogger('SoundServer')
		self.os = platform.system()  # why?

		self.logger.info('soundserver stdin: ' + str(sys.stdin.fileno()))

		self.pub = zmq.Pub((host, port))
		self.sub = zmq.Sub('wit-text', (host, str(port + 1)))

		# maybe change this to an env variable ... do travis.ci?
		# db = fs.FileStorage()
		# db.readYaml(YAML_FILE)
		# wit_token = db.getKey('WIT_TOKEN')

		if wit_token is None:
			self.logger.info('Need Wit.ai token, exiting now ...')
			exit()
		else:
			self.logger.info('Wit.ai API token %s', wit_token)

		self.input = wi.WitInput(wit_token)

		# Grab plugins
		self.readPlugins()

		results = """--------------------------
		Sound Server up
		Pub[wit results]: %s:%d
		Sub[text]: %s:%d
		Modules: %d
		--------------------------
		"""
		self.logger.info(results, host, port, host, port + 1, len(self.modules))

	def readPlugins(self, path="./plugins/"):
		"""
		Clears the current modules and reads in all plugins located in path
		in: path to plugins
		out: none
		"""
		self.modules = []
		sys.path.insert(0, path)
		for f in os.listdir(path):
			fname, ext = os.path.splitext(f)
			if ext == '.py' and fname != 'Module' and fname != '__init__':
				print('file:', fname, ext)
				mod = __import__(fname)
				m = mod.Plugin()
				self.modules.append(m)
		sys.path.pop(0)

	"""
	Converts text to speech using tools in the OS
	in: text
	out: None
	"""
	def speak(self, txt):
		if True:
			# fname = self.tts.tts(txt)
			# os.system('afplay %s'%(fname))
			print('speak:', txt)
		else:
			if self.os == 'Darwin': os.system('say -v vicki ' + txt)
			elif self.os == 'Linux': os.system('say ' + txt)
			else: self.logger.info('speak() error')

	def search(self, result):
		"""
		Searches through all plugins to find one that can process this intent
		in: struct{'intent': '', 'entities': ''}
		out: text (answer from plugin or '' if nothing could handle it)
		"""
		for m in self.modules:
			# print 'plugin:',m
			# print 'handleIntent:',m.handleIntent( result['intent'] )
			if m.handleIntent(result['intent']):
				# print result
				txt = m.process(result['entities'])
				self.logger.debug('found plugin response: ' + txt)
				return txt
		return ''

	@staticmethod
	def sound(snd):
		os.system('afplay {0!s}'.format((snd)))

	def run(self):
		"""
		Main process run loop
		in: none
		out: none
		"""
		# main loop
		try:
			# self.logger.info(str(self.name)+'['+str(self.pid)+'] started on '+
			# 	str(self.host) + ':' + str(self.port) +', Daemon: '+str(self.daemon))
			loop = True
			while loop:
				# get wit.ai json
				# result = self.input.listenPrompt()
				result = self.input.listen()

				txt = self.search(result)

				if txt == 'exit_loop':
					loop = False
				elif txt == 'empty' or not txt:
					self.logger.info('no plugin response')
					continue
				else:
					self.logger.debug('response' + txt)
					self.speak(txt)

			self.speak('Good bye ...')

		except KeyboardInterrupt:
			print('{} exiting'.format(__name__))
			raise KeyboardInterrupt


if __name__ == '__main__':
	# s = SoundServer('/Users/kevin/Dropbox/accounts.yaml')
	token = os.getenv('WIT')
	s = SoundServer(token)
	s.start()
	print('bye ...')
