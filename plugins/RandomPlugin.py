#!/usr/bin/env python

from Module import *
import random


####################################################################
# 
# 
####################################################################
class Plugin(Module):

	msglist = {
	'greeting': 
    	['hello yourself',
    	'hi',
    	'greetings',
    	'ola!',
    	'guten tag!',
    	'well hey baby'],
	'feelings':
		['I am fine',
		'good',
		'I feel good',
		'super',
		'excellent'],
	'error':
		['say again, over',
		'sorry, I did not understand',
		'what did you say',
		'stop mumbling please',
		'I did not hear you',
		'did you say bat guana ... speak up',
		'Go Venture Brothers! ... oh, what did you say?',
		'Hey Groot, get a vocabulary. I do not understand you',
		'whatcha talking about Willis?',
		'that does not compute',
		'not now',
		'let me think about it for a minute',
		'try again later',
		'ola! No hablo ingles',
		"I don't have time to listen to you mumble"],
	'joke':
		['Wifi went down for five minutes, so i had to talk to my family. They seem like nice people',
		'Why do cows wear bells ... because their horns do not honk',
		'What side of an Ewok has the most hair ... the outside',
		'Tosh point O says titties'],
	'mean':
		['be nice',
		'watch your mouth ... there are children around',
		'stop talking like that or I will tell Nina!',
		'you will hurt my feelings if you keep this up',
		'how would you like it if I talked to you like that, now stop']
	}

	def __init__(self):
		Module.__init__(self,['greeting','feelings','error','joke','mean'])
		
	"""
	"""
	def handleIntent(self,intent):
		if intent in self.intent:
			self.save_intent = intent
			return True
		return False
			
	"""
	"""
	def process(self, entity):
		resp = random.choice( self.msglist[self.save_intent] )
		self.save_intent = ''
		return resp




if __name__ == '__main__':
	r = Plugin()
	r.handleIntent('greeting')
	print r.process(0)
	