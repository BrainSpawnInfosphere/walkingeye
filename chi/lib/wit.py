#!/usr/bin/env python

"""
Might make this its own library: wit.ai
- wit
- witinput
- sox
"""

from __future__ import print_function
from __future__ import division
import requests
import os
import logging

WIT_API_HOST = os.getenv('WIT_URL', 'https://api.wit.ai')


class WitError(Exception):
	pass


class Wit(object):
	"""
	Simple Wit.ai interface
	"""
	access_token = None

	def __init__(self, access_token, logger=None):
		self.access_token = access_token
		self.logger = logger or logging.getLogger(__name__)

	def message(self, msg):
		"""
		Send a text message to Wit.ai
		"""
		self.logger.debug("Message request: msg=%r", msg)
		params = {}
		if msg:
			params['q'] = msg
		resp = self.req('GET', '/message', params)
		self.logger.debug("Message response: %s", resp)
		return resp

	def speech(self, fileio):
		"""
		Send a wave audio file to Wit.ai
		"""
		self.logger.debug("Speech request")
		fileio.seek(0)
		resp = self.req('POST', '/speech', {}, data=fileio.read())
		self.logger.debug("Speech response: %s", resp)
		return resp

	def req(self, meth, path, params, **kwargs):
		if path == '/message':
			rsp = requests.request(
				meth,
				WIT_API_HOST + path,
				headers={
					'authorization': 'Bearer ' + self.access_token,
					'accept': 'application/vnd.wit.20160330+json'
				},
				params=params,
				**kwargs
			)
		elif path == '/speech':
			rsp = requests.request(
				meth,
				WIT_API_HOST + path + '?v=20160511',
				headers={
					'authorization': 'Bearer ' + self.access_token,
					# 'accept': 'application/vnd.wit.20160330+json'
					'Content-Type': 'audio/wav',
					# 'Content-Type': 'audio/raw;encoding=signed-integer;bits=16;rate=16000;endian=little'
				},
				# params=params,
				**kwargs
			)
		else:
			raise WitError('This library does not support {0!s} path'.format({path}))

		if rsp.status_code > 200:
			raise WitError('Wit responded with status: ' + str(rsp.status_code) +
						' (' + rsp.reason + ')')
		json = rsp.json()
		if 'error' in json:
			raise WitError('Wit responded with an error: ' + json['error'])
		return json


def main():
	token = os.getenv('WIT')
	client = Wit(token)
	resp = client.message('hi')
	print(resp)


if __name__ == "__main__":
	main()
