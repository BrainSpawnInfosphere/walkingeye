#!/usr/bin/env python

import Module as mod


class Plugin(mod.Module):
	def __init__(self):
		mod.Module.__init__(self, 'help')

	def process(self, entity):
		return 'Help module is not implemented yet'


if __name__ == '__main__':
	h = mod.Plugin()
	print h.process(0)
