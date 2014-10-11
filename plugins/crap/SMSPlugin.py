#!/usr/bin/env python

from Module import *
import logging

####################################################################
# 
# 
####################################################################
class Plugin(Module):
	def __init__(self):
		Module.__init__(self,'sms')
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
				to=self.info['Twilio']['phone'][who],
				self.from_phone ) 
			self.logger.debug( 'Good SMS: %s'%(message.sid) )
		
		except TwilioRestException as e:
			self.logger.error( e )
