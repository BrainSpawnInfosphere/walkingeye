#!/usr/bin/env python

import Module as mod
import logging
import twilio
from twilio.rest import TwilioRestClient
from twilio.rest.exceptions import TwilioRestException


class Plugin(mod.Module):
	"""
	"""
	def __init__(self, auth_token, account_sid):
		"""
		in:
			sid - ???
			token - api token
		"""
		mod.Module.__init__(self, 'sms', sid, token)
		# Your Account Sid and Auth Token from twilio.com/user/account
		# account_sid = self.info['Twilio']['sid']
		# auth_token  = self.info['Twilio']['token']
		self.client = TwilioRestClient(account_sid, auth_token)
		# self.from_phone = self.info['Twilio']['phone']['Twilio']

		self.logger.debug('Twilio sid: %s' % (account_sid))
		self.logger.debug('Twilio token: %s' % (auth_token))

	def process(self, entity):
		"""
		"""
		#print '>> process',entity
		try:
			if ('message_body' not in entity) or ('contact' not in entity):
				self.logger.error( '[-] Error:'+ str(entity) )
				return 'error'

			# need better solution
			who = entity['contact']['value']
			if who == 'kevin': who = 'Kevin'
			if who == 'nina': who = 'Nina'
			msg = entity['message_body']['value']

			#print 'who',who,'msg',msg,'from phone',self.from_phone,'to phone',self.info['Twilio']['phone']

			message = self.client.messages.create(body=msg,
				to=self.info['Twilio']['phone'][who],
				from_=self.from_phone )
			self.logger.debug( '[+] Good SMS: %s'%(message.sid) )

		except TwilioRestException as e:
			self.logger.error( e )
			return 'error'

		except:
			self.logger.error( '[-] Error:'+ str(entity) )
			return 'error'

		return 'empty'

if __name__ == '__main__':
	token = os.getenv('TWILIO_TOKEN')
	sid = os.getenv('TWILIO_SID')

	if token is None or sid is None:
		exit('No Twilio token or sid given in os env')

	p = Plugin(token, sid)
	print ret
