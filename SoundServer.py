#!/usr/bin/env python

import os
import sys
import wit
import pyaudio
import time
import logging
#import handle_voice as hv
import GoogleTTS
from multiprocessing.connection import Listener as Publisher
import multiprocessing as mp
import socket
#import random
import yaml
import glob
import wave  
import misc
#import json
#import forecastio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3
# Change this based on your OSes settings. This should work for OSX, though.
ENDIAN = 'little' 
# see https://wit.ai/docs/api PSOT/speech for more options: wav,mp3,ulaw
CONTENT_TYPE = 'raw;encoding=signed-integer;bits=16;rate={0};endian={1}'.format(RATE, ENDIAN)


###################################################################################

class Microphone:
	def __init__(self,real=True):


###################################################################################

"""
generator -- don't change!!
in: pyaudio and number of seconds to record
out: audio stream
"""
def listen(p,sec):
	
	stream = p.open(
		format=FORMAT, 
		channels=CHANNELS, 
		rate=RATE,
		input=True, 
		frames_per_buffer=CHUNK)
	
	for i in range(0, int(RATE / CHUNK * sec)): 
		yield stream.read(CHUNK)
	
	stream.stop_stream()
	stream.close()
	
	

####################################################################
# 
# 
####################################################################
class SoundServer(mp.Process):
	def __init__(self,host="localhost",port=9200):
		mp.Process.__init__(self)
		self.host = host
		self.port = port
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger(__name__)
		
		#self.getKeys()
		self.info = self.readYaml('/Users/kevin/Dropbox/accounts.yaml')
		
		# setup WIT.ai
		wit_token = self.info['WIT_TOKEN']
		self.logger.debug('Wit.ai API token %s'%(wit_token))
		
		if wit_token is None:
			self.logger.info( 'Need Wit.ai token, exiting now ...' )
			exit()	
		self.wit = wit.Wit(wit_token)
		
		# get microphone	
		self.mic = pyaudio.PyAudio()
		
		# modules to handle different intents
		#news = NewsModule()
		#weather = WeatherModule()
		#r = RandomModule()
		#t = TimeModule()
		#d = DateModule()
		#e = ExitModule()
		#starwars = StarWarsModule()
		#self.modules = [news,weather,r,t,d,e,starwars]
		
		# Grab plugins
		path = "plugins/"
		self.modules = []
		#modules = {}
		sys.path.insert(0, path)
		for f in os.listdir(path):
			fname, ext = os.path.splitext(f)
			if ext == '.py' and fname != 'Module':
				mod = __import__(fname)
				m=mod.Plugin()
				# not sure how to handle random with multiple intents??
				#modules[m.intent] = m
				#for i in m.intent:
				#	modules[i] = m
				self.modules.append( m )
		sys.path.pop(0)
		#print modules
	
	"""
	Read a yaml file and return the corresponding dictionary
	todo: duplicate of what is already in Module
	in: file name
	out: dict
	"""
	def readYaml(self,fname):
		f = open( fname )
		dict = yaml.safe_load(f)
		f.close()
		
		return dict
	
	"""
	Converts text to speech
	in: text
	out: None
	"""
	def playTxt(self,txt):
		if True:
			GoogleTTS.tts(txt,None)
			os.system('afplay output.mp3')
		else:
			os.system('say -v vicki ' + txt)
	
	"""
	Main process run loop
	in: none
	out: none
	"""
	def run(self):
		# main loop
		run = True
		while run:
			result = self.wit.post_speech(listen( self.mic, 2 ), content_type=CONTENT_TYPE)
			ans = self.getKey(result)
			
			# this doesn't work so good :(
			if ans == 'attention':
				self.logger.info('[*] Listening')
				misc.playWave('sounds/misc/beep_hi.wav')
				
				result = self.wit.post_speech(listen( self.mic, 3 ), content_type=CONTENT_TYPE)
				
				misc.playWave('sounds/misc/beep_lo.wav')
				self.logger.info('[*] Done listening')
				txt = self.handleVoice(result)
				
				if txt == 'exit_loop':
					run = False
				elif txt != '':
					self.playTxt(txt)
		
		self.playTxt('Good bye ...')
		self.mic.terminate()
		
	
	"""
	Gets intent from msg and handles errors
	in: wit.ai message
	out: key (intent)
	"""
	def getKey(self,msg):
		#print msg
	
		# hangle errors ----------------------------
		if not msg:
			self.logger.debug('<< no msg >>')
			key = 'empty'
		elif msg['msg_body'] == '':
			self.logger.debug('<< no msg body >>')
			key = 'empty'
		elif 'outcome' not in msg:
			self.logger.debug('no outcome')
			key = 'error'
		elif 'confidence' not in msg['outcome']:
			self.logger.debug('no confidence')
			key = 'error'
		elif msg['outcome']['confidence'] < 0.5:
			key = 'error'
			print 'confidence',msg['outcome']['confidence']
		else:
			key = msg['outcome']['intent']
	
		return key

	"""
	Handles intent from wit.ai
	in: processed voice from wit.ai and a list of standard answers
	out: text for speech
	todo: make this more dynamic and pluggin
	"""
	def handleVoice(self,msg):
		# get key and handle errors -----------------
		key = self.getKey(msg)
		resp = ''
	
		# handle nothing said (empty) ---------------
		if key == 'empty':
			resp = ''
	
		# handle dynamic responses ------------------
		for m in self.modules:
			if m.handleIntent( key ):
				resp = m.process( msg['outcome']['entities'] )
	
		#print 'response',resp
		self.logger.debug('response'+resp)
		
		return resp



if __name__ == '__main__':
	#output_file = StringIO()
	ss = SoundServer()
	ss.run()
	print 'bye ...'
	