#!/usr/bin/env python

import Module as mod


class Plugin(mod.Module):
	def __init__(self):
		mod.Module.__init__(self, 'safe_word')

	def process(self, entity):
		return 'exit_loop'


if __name__ == '__main__':
	e = mod.Plugin()
	print e.process(0)
