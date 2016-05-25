#!/usr/bin/env python

import os							# run commands and get/use path
import platform						# determine os
import sys							# ?
# import time							# sleep
import logging						# logging
# import GoogleTTS as gtts			# use google tts
import multiprocessing as mp		# multiprocess
# import socket
# import yaml
# import glob
# import json
import lib.zmqclass as zmq
# import lib.sox as sox
import lib.FileStorage as fs
# import lib.wit as wit				# wit.ai
import lib.WitInput as wi

"""
OMG!!

use pip install wit

NOT

pip install pywit
"""


# class YamlKeys(object):
# 	def __init__(self, yamlkeys):
# 		self.keys = self.readYaml(yamlkeys)
#
# 	def readYaml(self, fname):
# 		f = open(fname)
# 		dict = yaml.safe_load(f)
# 		f.close()
# 		return dict
#
# 	def getKey(self, keyName):
# 		return self.keys[keyName]

###################################################################################
# wit.init()
#
# class Microphone(object):
# 	"""
# 	This is more of a Wit.ai input class that takes voice or text and returns
# 	a wit.ai response dict.
# 	"""
# 	def __init__(self,wit_token):
# 		# wit.init()
#
# 		logging.basicConfig(level=logging.INFO)
# 		self.logger = logging.getLogger('microphone')
# 		self.wit_token = wit_token
#
# 	def __del__(self):
# 		# wit.close()
# 		# print 'Microphone closing'
# 		self.logger.debug('microphone closing')
#
# 	def text(self,text):
# 		"""
# 		Will grab text from keyboard and process the wit.ai json message
# 		in: text
# 		out: dict {intent, [entities]}, return value (True/False)
# 		"""
# 		# self.logger.debug('text()')
# 		# try:
# 		result = wit.message(self.wit_token, text )
# 		ans = self.getKey( json.loads(result) )
# 		self.logger.debug(ans)
# 		return ans
#
# 		#
# 		# except KeyboardInterrupt:
# 		# 	raise KeyboardInterrupt
# 		#
# 		# except:
# 		# 	return {}, False
#
# 	def listen(self, ps=False):
# 		"""
# 		Will grab audio from microphone and process the wit.ai json message
# 		in: nothing
# 		out: dict {intent, [entities]}, return value (True/False)
# 		"""
# 		if ps: self.playSound('../sounds/misc/beep_hi.wav')
# 		try:
# 			# result = wit.voice_query_auto( self.wit_token )
# 		except:
# 			raise
# 		if ps: self.playSound('../sounds/misc/beep_lo.wav')
# 		# return self.getKey( json.loads(result) )
# 		return self.getKey( result )
#
#
# 	def listenPrompt(self,prompt):
# 		"""
# 		Will grab audio from microphone and process the wit.ai json message
# 		in: nothing
# 		out: dict {intent, [entities]}, return value (True/False)
# 		"""
# 		result = {}
# 		result['intent'] = ''
#
# 		while(result['intent'] == 'attention'):
# 		# while(result['_text'] != prompt):
# 			# print '--------'
# 			result = self.listen()
# 			# print '/////',result
# 			print result
#
# 		return self.listen(True)
	#
	# #
	# # def voice(self):
	# # 	"""
	# # 	Will grab audio from microphone and process the wit.ai json message
	# # 	in: nothing
	# # 	out: dict {intent, [entities]}, return value (True/False)
	# # 	"""
	# # 	try:
	# # 		txt = {}
	# # 		result = ''
	# # 		ret = False
	# #
	# # 		# need to say 'jarvis' or 'hey robot' to start
	# # 		self.logger.debug('microphone')
	# # 		result = wit.voice_query_auto( self.wit_token )
	# # 		ans = self.getKey( json.loads(result) )
	# #
	# # 		# now get the command
	# # 		if ans['intent'] == 'attention':
	# # 			# self.logger.info('[*] Listening')
	# # 			self.playSound('../sounds/misc/beep_hi.wav')
	# # 			result = wit.voice_query_auto( self.wit_token )
	# # 			txt = self.getKey( json.loads(result) )
	# # 			# self.logger.info('[*] Done listening')
	# # 			self.playSound('../sounds/misc/beep_lo.wav')
	# # 			ret = True
	# # 		else:
	# # 			self.logger.info('[-] Error, no audio detected')
	# # 			ret = False
	# #
	# # 		return txt, ret
	# #
	# # 	except KeyboardInterrupt:
	# # 		raise KeyboardInterrupt
	# #
	# # 	except:
	# # 		self.logger.debug('voice error')
	# # 		return {}, False
	#
	#
	# def playSound(self, snd):
	# 	os.system('afplay %s'%(snd))
	#
	#
	# def getKey(self,msg):
	# 	"""
	# 	Gets intent from msg and handles errors
	# 	in: wit.ai message as a dict
	# 	out: dict {intent, [entities]}
	# 	"""
	# 	# pp.pprint( msg )
	#
	# 	key = 'error'
	# 	ent = []
	#
	# 	# print type(msg)
	#
	# 	# hangle errors ----------------------------
	# 	if not msg:
	# 		self.logger.debug('<< no msg >>')
	# 		# key = 'error'
	# 	elif 'outcomes' not in msg:
	# 		self.logger.debug('no outcome')
	# 		# key = 'error'
	# 	elif len(msg['outcomes']) == 0:
	# 		self.logger.debug('outcome empty')
	# 	elif msg['outcomes'][0]['intent']: # assume [0] is highest outcome for now FIXME: 4 mar 15
	# 		if msg['outcomes'][0]['confidence'] > 0.5:
	# 			key = msg['outcomes'][0]['intent']
	# 			ent = msg['outcomes'][0]['entities']
	#
	# 	ans = {}
	# 	ans['intent'] = key
	# 	ans['entities'] = ent
	#
	# 	return ans


class SoundServer(mp.Process):
	"""
	"""
	# def __init__(self, YAML_FILE, REAL, stdin=os.fdopen(os.dup(sys.stdin.fileno())), host="localhost", port=9200):
	def __init__(self, YAML_FILE, host="localhost", port=9200):
		mp.Process.__init__(self)
		self.host = host
		self.port = port
		logging.basicConfig(level=logging.DEBUG)
		self.logger = logging.getLogger('SoundServer')
		self.os = platform.system()  # why?

		self.logger.info('soundserver stdin: ' + str(sys.stdin.fileno()))

		# subscriber [text]/publisher [wit responses]
		tcp = 'tcp://%s:%s'
		# print 'DEBUG:',tcp % (host, str(port + 1))
		self.pub = zmq.Pub(tcp % (host, port))
		self.sub = zmq.Sub('wit-text', tcp % (host, str(port + 1)))

		# self.info = self.readYaml(YAML_FILE)

		# setup WIT.ai
		# wit_token = self.info['WIT_TOKEN']
		db = fs.FileStorage()
		db.readYaml(YAML_FILE)
		wit_token = db.getKey('WIT_TOKEN')

		if wit_token is None:
			self.logger.info('Need Wit.ai token, exiting now ...')
			exit()
		else:
			self.logger.info('Wit.ai API token %s' % (wit_token))

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
		self.logger.info(results % (host, port, host, port + 1, len(self.modules)))

	def readPlugins(self, path="../plugins/"):
		"""
		Clears the current modules and reads in all plugins located in path
		in: path to plugins
		out: none
		"""
		self.modules = []
		sys.path.insert(0, path)
		for f in os.listdir(path):
			fname, ext = os.path.splitext(f)
			if ext == '.py' and fname != 'Module':
				mod = __import__(fname)
				m = mod.Plugin()
				self.modules.append(m)
		sys.path.pop(0)

	# """
	# Read a yaml file and return the corresponding dictionary
	# todo: duplicate of what is already in Module
	# in: file name
	# out: dict
	# """
	# def readYaml(self, fname):
	# 	f = open(fname)
	# 	dict = yaml.safe_load(f)
	# 	f.close()
	#
	# 	return dict

	# # for multiprocessing issue
	# def start(self):
	# 	self.run()
	#
	# # for multiprocessing issue
	# def join(self):
	# 	a=1

	"""
	Converts text to speech using tools in the OS
	in: text
	out: None
	"""
	def speak(self, txt):
		if True:
			# fname = self.tts.tts(txt)
			# os.system('afplay %s'%(fname))
			print 'speak:', txt
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

	def sound(self, snd):
		os.system('afplay %s' % (snd))

	"""
	Main process run loop
	in: none
	out: none
	"""
	def run(self):
		# main loop
		# try:
			# self.logger.info(str(self.name)+'['+str(self.pid)+'] started on '+
			# 	str(self.host) + ':' + str(self.port) +', Daemon: '+str(self.daemon))
		loop = True
		while loop:
			# get wit.ai json
			result = self.input.listenPrompt('jarvis')

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

		# except KeyboardInterrupt:
		# 	print 'sound server exiting'
		# 	# exit()
		# 	raise KeyboardInterrupt


if __name__ == '__main__':
	s = SoundServer('/Users/kevin/Dropbox/accounts.yaml')
	s.start()
	print 'bye ...'
