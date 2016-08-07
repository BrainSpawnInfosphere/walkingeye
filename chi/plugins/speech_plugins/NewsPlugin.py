#!/usr/bin/env python

import Module as mod


class Plugin(mod.Module):
	def __init__(self):
		mod.Module.__init__(self, 'news')
		self.intent = 'news'

	def process(self, entity):
		return 'News module is not  implemented yet'


if __name__ == '__main__':
	n = mod.Plugin()
	print n.process(0)
