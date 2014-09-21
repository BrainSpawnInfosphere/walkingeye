#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#
# PS4 has 6 axes, 14 buttons, 1 hat
# This program doesn't grab all buttons, just the most useful :)


import time
import json
from multiprocessing.connection import Client as Subscriber


class Module:
	def __init__(self):
		a=1
	def handleIntent(self,intent):
		if intent == 'bob':
			return True
		else:
			return False
	
	def process(self,args):
		print 'process'