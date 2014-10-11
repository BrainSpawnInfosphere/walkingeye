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

# generator -- don't change!!
def listen(p):
	stream = p.open(
		format=FORMAT, channels=CHANNELS, rate=RATE,
		input=True, frames_per_buffer=CHUNK)
	print("* recording and streaming")
	
	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)): 
		yield stream.read(CHUNK)
	
	print("* done recording and streaming")
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
		
		self.getKeys()
		
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
		
		path = "plugins/"
		self.modules = []
		sys.path.insert(0, path)
		for f in os.listdir(path):
			fname, ext = os.path.splitext(f)
			if ext == '.py' and fname != 'Module':
				mod = __import__(fname)
				#self.modules[fname] = mod.Plugin()
				self.modules.append( mod.Plugin() )
		sys.path.pop(0)
	
	def getKeys(self):
		f = open('/Users/kevin/Dropbox/accounts.yaml')
		self.info = yaml.safe_load(f)
		f.close()
	
	"""
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
		while True:
			result = self.wit.post_speech(listen( self.mic ), content_type=CONTENT_TYPE)
			txt = self.handleVoice(result)
			
			if txt == 'exit_loop':
				break
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
	