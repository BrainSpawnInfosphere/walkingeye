#!/usr/bin/env python

import os
import sys
import wit
import pyaudio
import time
import logging
import GoogleTTS
from multiprocessing.connection import Listener as Publisher
import multiprocessing as mp
import socket
import yaml
import glob
import wave  
import misc
import pprint


###################################################################################

class Microphone:
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	ENDIAN = 'little' 
	# see https://wit.ai/docs/api PSOT/speech for more options: wav,mp3,ulaw
	CONTENT_TYPE = 'raw;encoding=signed-integer;bits=16;rate={0};endian={1}'.format(RATE, ENDIAN)

	def __init__(self,wit_token,real,stdin):
		self.real = real
		self.stdin = stdin
		
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')
		
		self.wit = wit.Wit(wit_token)

		# get microphone	
		if real: 
			self.mic = pyaudio.PyAudio()
	
	def __del__(self):
		if self.real: self.mic.terminate()
		
	"""
	Will grab audio from microphone or text from keyboard
	in: nothing
	out: wit.ai json responce
	"""
	def stt(self):
		txt = ''
		ret = False

		if self.real:
			result = self.wit.post_speech(self.grabAudio( self.mic, 2 ), content_type=self.CONTENT_TYPE)
			ans = self.getKey(result)
		
			# this doesn't work so good :(
			if ans == 'attention':
				self.logger.info('[*] Listening')
				misc.playWave('sounds/misc/beep_hi.wav')
			
				txt = self.wit.post_speech(self.grabAudio( self.mic, 3 ), content_type=self.CONTENT_TYPE)
				
				misc.playWave('sounds/misc/beep_lo.wav')
				self.logger.info('[*] Done listening')
				ret = True
				
		else:
			print "you:",
			input = self.stdin.readline()
			txt = self.wit.get_message(input)
			pprint.pprint( txt )
			ret = True
			
		return txt, ret
		
	"""
	generator -- don't change!!
	in: pyaudio and number of seconds to record
	out: audio stream
	"""
	def grabAudio(self,p,sec):
	
		stream = p.open(
			format=self.FORMAT, 
			channels=self.CHANNELS, 
			rate=self.RATE,
			input=True, 
			frames_per_buffer=self.CHUNK)
	
		for i in range(0, int(self.RATE / self.CHUNK * sec)): 
			yield stream.read(self.CHUNK)
	
		stream.stop_stream()
		stream.close()


	
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

# 	def calcThreshold(self):
#  		# prepare recording stream
# 		stream = self._audio.open(format=pyaudio.paInt16,
# 								  channels=1,
# 								  rate=RATE,
# 								  input=True,
# 								  frames_per_buffer=CHUNK)
# 
# 		# stores the audio data
# 		frames = []
# 
# 		# stores the lastN score values
# 		lastN = [i for i in range(30)]
# 
# 		# calculate the long run average, and thereby the proper threshold
# 		for i in range(0, RATE / CHUNK * THRESHOLD_TIME):
# 
# 			data = stream.read(CHUNK)
# 			frames.append(data)
# 
# 			# save this data point as a score
# 			lastN.pop(0)
# 			lastN.append(self.getScore(data))
# 			average = sum(lastN) / len(lastN)
# 
# 		# this will be the benchmark to cause a disturbance over!
# 		THRESHOLD = average * THRESHOLD_MULTIPLIER


###################################################################################

# """
# generator -- don't change!!
# in: pyaudio and number of seconds to record
# out: audio stream
# """
# def listen(p,sec):
# 	
# 	stream = p.open(
# 		format=FORMAT, 
# 		channels=CHANNELS, 
# 		rate=RATE,
# 		input=True, 
# 		frames_per_buffer=CHUNK)
# 	
# 	for i in range(0, int(RATE / CHUNK * sec)): 
# 		yield stream.read(CHUNK)
# 	
# 	stream.stop_stream()
# 	stream.close()
	
	

####################################################################
# 
# 
####################################################################
class RobotSoundServer(mp.Process):
	def __init__(self,stdin,host="localhost",port=9200):
		mp.Process.__init__(self)
		self.host = host
		self.port = port
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('robot')
		self.tts = GoogleTTS()
		
		#self.getKeys()
		self.info = self.readYaml('/Users/kevin/Dropbox/accounts.yaml')
		
		# setup WIT.ai
		wit_token = self.info['WIT_TOKEN']
		
		if wit_token is None:
			self.logger.info( 'Need Wit.ai token, exiting now ...' )
			exit()	
		else:
			self.logger.info('Wit.ai API token %s'%(wit_token))
		
		# get microphone	
		use_mic = False
		self.mic = Microphone(wit_token,use_mic,stdin)
		
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
			fname = tts.tts(txt,None)
			os.system('afplay %s'%(fname))
		else:
			os.system('say -v vicki ' + txt)
	
	"""
	Main process run loop
	in: none
	out: none
	"""
	def run(self):
		# main loop
		self.logger.info(str(self.name)+'['+str(self.pid)+'] started on'+ 
			str(self.host) + ':' + str(self.port) +', Daemon: '+str(self.daemon))
		run = True
		while run:		
			print 'loop'	
			# get wit.ai json 
			result,ret = self.mic.stt()
			if ret:
 				txt = self.handleVoice(result)
				
				if txt == 'exit_loop':
					run = False
				elif txt == 'empty':
					pass
				elif txt != '':
					self.playTxt(txt)
		
		self.playTxt('Good bye ...')
		
	
	"""
	Gets intent from msg and handles errors
	in: wit.ai message
	out: key (intent)
	todo: duplicates of this
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
			print '[-] Error confidence:',msg['outcome']['confidence']
		else:
			key = msg['outcome']['intent']
	
		return key

	"""
	Handles intent from wit.ai
	in: processed voice from wit.ai
	out: text for speech or empty
	todo: make this more dynamic and pluggin
	"""
	def handleVoice(self,msg):
		# get key and handle errors -----------------
		key = self.getKey(msg)
		resp = ''
		
		# handle nothing said (empty) ---------------
		if key == 'empty':
			resp = 'empty'
		else:
			# handle dynamic responses ------------------
			for m in self.modules:
				if m.handleIntent( key ):
					resp = m.process( msg['outcome']['entities'] )
		
		# shouldn't have to do this
		if not resp:
			resp = 'empty'	
		self.logger.debug('response'+resp)
		
		return resp



if __name__ == '__main__':
	#output_file = StringIO()
	s = RobotSoundServer()
	s.run()
	print 'bye ...'
	