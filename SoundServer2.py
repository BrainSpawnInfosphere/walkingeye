#!/usr/bin/env python

import os
import wit
import pyaudio
import time
import logging
#import handle_voice as hv
import GoogleTTS
from multiprocessing.connection import Listener as Publisher
import multiprocessing as mp
import socket
import random
import yaml
import glob
import pyaudio  
import wave  
import json
import forecastio

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3
# Change this based on your OSes settings. This should work for OSX, though.
ENDIAN = 'little' 
# see https://wit.ai/docs/api PSOT/speech for more options: wav,mp3,ulaw
CONTENT_TYPE = 'raw;encoding=signed-integer;bits=16;rate={0};endian={1}'.format(RATE, ENDIAN)



####################################################################
# Base class
# 
####################################################################
class Module(mod_name='none'):
	"""
	"""
	def __init__(self):
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger(__name__)
		self.modName = mod_name
		self.logger.info('[+] Init module %s'%(self.modName))
		
		# get parameters
		# does this get called everytime? Can i share, like static in C++?
		f = open('/Users/kevin/Dropbox/accounts.yaml')
		self.info = yaml.safe_load(f)
		f.close()
		
	"""
	"""
	def handleIntent(self,intent):
		ans = false
		if self.intent == intent:
			ans = True
		return ans


####################################################################
# 
# 
####################################################################
class SMSModule(Module):
	def __init__(self):
		# Your Account Sid and Auth Token from twilio.com/user/account
		account_sid = info['Twilio']['sid'] 
		auth_token  = info['Twilio']['token'] 
		self.client = TwilioRestClient(account_sid, auth_token)
		self.from_phone=info['Twilio']['phone']['Twilio']
		
		self.logger.debug('Twilio sid: %s'%(account_sid))
		self.logger.debug('Twilio token: %s'%(auth_token))
			
	"""
	"""
	def process(self, entity):
		try:
			who = entity['contact']['value']
			msg = entity['message_body']['value']
			message = self.client.messages.create(body=msg,
				to=self.info['Twilio']['phone'][who] ,    
				self.from_phone ) 
			self.logger.debug( 'Good SMS: %s'%(message.sid) )
		
		except TwilioRestException as e:
			self.logger.error( e )

####################################################################
# 
# 
####################################################################
class WeatherModule(Module):
	def __init__(self):
		api_key = self.info['FORECAST_API_KEY']
	
		if api_key is None:
			self.logger.error('Need Forecast.io token, exiting now ...')
			exit()

		# Latitude, Longitude for location
		lat = self.info['Geolocation']['LATITUDE']
		long = self.info['Geolocation']['LONGITUDE']  
	
		self.forecast = forecastio.load_forecast(api_key, lat, long)
		self.weather_time = time.gmtime()
		
		self.intent = 'weather'
	
	"""
	Grab a forcast
	in: day of week (0-6) to grab weather forecast and json info
	out: forecast txt
	"""
	def grabWeatherDay(self,day):
		j = self.forecast.json
		
		high = int(round(j['daily']['data'][day]['apparentTemperatureMax'],0))
		low = int(round(j['daily']['data'][day]['apparentTemperatureMin'],0))
		clouds = int(round(j['daily']['data'][day]['cloudCover']*100.0,0))
		sum = j['daily']['summary']
		wind = int(round(j['daily']['data'][day]['windSpeed'],0))
	
		days = ['today','tomorrow', 'there']
	
		if day > 2:
			day = 2
	
		resp = '%s will be a high of %d and low of %d with %d percent clouds and %d mile per hour winds'%(days[day],high,low,clouds,wind)
	
		return resp

	"""
	Handles the weather request. If the last one isn't too old, it just uses that one.
	in: what day (now, tomorrow, today, etc)
	out: txt response
	todo: 
	"""
	def process(self, entity):	
		resp = ''
		w_time = ''
		
		if 'datetime' in entity: 
			w_time = entity['datetime']['body']
	
		# convert time to seconds from epoch and div by 60 for minutes
		now = time.localtime()
		diff = (time.mktime(self.weather_time) - time.mktime(now))/60
		
		j = self.forecast.json
		
		# update if it has been too long
		if diff > 5:
			self.forecast.update()
			j = self.forecast.json
			self.weather_time = now
	
		if w_time == 'tomorrow':
			resp = self.grabWeatherDay(1)
		
		elif w_time == 'today':
			resp = self.grabWeatherDay(0)
		
		elif w_time == 'this week':
			resp =  j['daily']['summary']
		
		else:
			temp = j['currently']['apparentTemperature']
			rain = j['currently']['precipProbability']*100.0	
			resp = 'The weather is currently %d degrees with %d percent chance of rain'%(temp,rain)
		
		return resp


####################################################################
# 
# 
####################################################################
class StarWarsModule(Module):
	def __init__(self):
		self.intent = 'star_wars'
		
		# setup Star Wars
		file = '/Users/kevin/Desktop/star_wars_sounds'
		self.star_wars_sounds = glob.glob(file + '/*.wav')
			
	"""
	"""
	def process(self, entity):
		sound = random.choice( self.star_wars_sounds )
		self.playWave( sound )
		return ''
		
	
	"""
	Plays a Wave file
	in: path to sound to play
	out: none
	"""
	def playWave(self,file):
		#define stream chunk   
		chunk = 1024  
	
		#open a wav format music  
		f = wave.open(file,"rb")  
	
		#instantiate PyAudio  
		p = pyaudio.PyAudio()  
	
		#open stream  
		stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
						channels = f.getnchannels(),  
						rate = f.getframerate(),  
						output = True)  
		#read data  
		data = f.readframes(chunk)  
	
		#paly stream  
		while data != '':  
			stream.write(data)  
			data = f.readframes(chunk)  
	
		#stop stream  
		stream.stop_stream()  
		stream.close()  
	
		#close PyAudio  
		p.terminate()  
	

####################################################################
# 
# 
####################################################################
class TimeModule(Module):
	def __init__(self):
		self.intent = 'time'
		
	"""
	"""	
	def process(self, entity):
		t = time.localtime()
		hrs = t[3]
		if hrs > 12:
			hrs = hrs - 12
			ampm = 'pm'
		else:
			ampm = 'am'
		mins = t[4]
		resp = 'The current time is %d %d %s'%(hrs,mins,ampm)
		return resp


####################################################################
# 
# 
####################################################################
class DateModule(Module):
	def __init__(self):
		self.intent = 'date'
		
	"""
	"""
	def process(self, entity):
		t = time.localtime()
		day = t[2]
		months = ['January', 'February','March','April','May','June','July','August','September','October','November','December']
		mon = months[t[1]-1]
		yr = t[0]
		resp = 'The date is %d %s %d'%(day,mon,yr)
		return resp


####################################################################
# 
# 
####################################################################
class RandomModule(Module):
	def __init__(self):
		self.intent = ['greeting','feelings','error','joke','mean']
		
		# get canned responces
		f = open( self.info['reponse_path'] )
		self.msglist = yaml.safe_load(f)
		f.close()
		
	"""
	"""
	def handleIntent(self,intent):
		for i in self.intent:
			if i == intent:
				self.save_intent = intent
				return True
		
		return False
			
	"""
	"""
	def process(self, entity):
		resp = random.choice( self.msglist[self.save_intent] )
		self.save_intent = ''
		return resp


####################################################################
# Help:
# Lists available commands, or describes a command in detail
# 
####################################################################
class HelpModules(Module):
	def __init__(self):
		self.intent = 'help'
			
	def process(self, entity):
		return 'Help module is not implemented yet'

####################################################################
# 
# 
####################################################################
class NewsModule(Module):
	def __init__(self):
		self.intent = 'news'
			
	def process(self, entity):
		return 'News module is not  implemented yet'
		
####################################################################
# 
# 
####################################################################
class ExitModule(Module):
	def __init__(self):
		self.intent = 'safe_word'
			
	def process(self, entity):
		return 'exit_loop'

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
		news = NewsModule()
		weather = WeatherModule()
		r = RandomModule()
		t = TimeModule()
		d = DateModule()
		e = ExitModule()
		starwars = StarWarsModule()
		
		self.modules = [news,weather,r,t,d,e,starwars]

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
	