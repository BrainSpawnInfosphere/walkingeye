#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#
# PS4 has 6 axes, 14 buttons, 1 hat
# This program doesn't grab all buttons, just the most useful :)


from __future__ import division
from __future__ import print_function
import sdl2
import time  # sleep ... why?
import argparse
#import lib.zmqclass as zmq


class Joystick(object):
	"""
	Joystick class setup to handle a Playstation PS4 Controller and then
	publish the outputs via ZeroMQ.
	"""
	def __init__(self, host, port):
		# self.pub = zmq.Pub('tcp://' + str(host) + ':' + str(port))
#		self.pub = zmq.Pub((host, port))

		# init SDL2 and grab joystick
		sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
		self.js = sdl2.SDL_JoystickOpen(0)

		# grab info for display
		a = sdl2.SDL_JoystickNumAxes(self.js)
		b = sdl2.SDL_JoystickNumButtons(self.js)
		h = sdl2.SDL_JoystickNumHats(self.js)

		print('==========================================')
		print(' Joystick ')
		print('   axes:', a, 'buttons:', b, 'hats:', h)
		print('==========================================')

	def formatCmd(self, ps4):
		"""
		useful?

		This is a formatter ... could just send raw and have subscriber handle
		it?
		"""
		# command template to be sent
		cmd = {'cmd':
			{
				'linear': {'x': 0, 'y': 0},
				'angular': {'x': 0, 'y': 0, 'z': 0},
			}
		}

		lx = float(ps4['la']['x']) / 32767.0
		ly = float(ps4['la']['y']) / 32767.0

		cmd['cmd']['linear']['x'] = lx
		cmd['cmd']['linear']['y'] = ly

		ax = float(ps4['la']['x']) / 32767.0
		# ay = float(ps4['la']['y']) / 32767.0

		cmd['cmd']['angular']['z'] = ax

		# print cmd

		return cmd

	def run(self, verbose=False):
		js = self.js

		# Data structure holding the PS4 info
		ps4 = {
			'la': {'x': 0, 'y': 0},  # left axis
			'ra': {'x': 0, 'y': 0},
			'lt1': 0,  # left trigger 1
			'rt1': 0,
			'lt2': 0,  # left trigger 2
			'rt2': 0,
			'circle': 0,
			'triangle': 0,
			'square': 0,
			'x': 0,
			'hat': 0,
		}

		while True:
			try:
				sdl2.SDL_JoystickUpdate()

				# left axis
				ps4['la']['x'] = sdl2.SDL_JoystickGetAxis(js, 0)
				ps4['la']['y'] = sdl2.SDL_JoystickGetAxis(js, 1)

				# right axis
				ps4['ra']['x'] = sdl2.SDL_JoystickGetAxis(js, 2)
				ps4['ra']['y'] = sdl2.SDL_JoystickGetAxis(js, 5)

				# left trigger axis
				ps4['lt2'] = sdl2.SDL_JoystickGetAxis(js, 3)

				# right trigger axis
				ps4['rt2'] = sdl2.SDL_JoystickGetAxis(js, 4)

				# get buttons
				ps4['square'] = sdl2.SDL_JoystickGetButton(js, 0)
				ps4['x'] = sdl2.SDL_JoystickGetButton(js, 1)
				ps4['circle'] = sdl2.SDL_JoystickGetButton(js, 2)
				ps4['triangle'] = sdl2.SDL_JoystickGetButton(js, 3)
				ps4['lt1'] = sdl2.SDL_JoystickGetButton(js, 4)
				ps4['rt1'] = sdl2.SDL_JoystickGetButton(js, 5)

				# use share button as a quit
				# quit = sdl2.SDL_JoystickGetButton(js, 8)

				# get hat
				ps4['hat'] = sdl2.SDL_JoystickGetHat(js, 0)

				if verbose:
					print(ps4)

#				self.pub.pub('js', self.formatCmd(ps4))

				time.sleep(0.1)

			except (IOError, EOFError):
				print('[-] Connection gone .... bye')
				break

		# clean-up
		sdl2.SDL_JoystickClose(js)
		print('Bye ...')


# set up and handle command line args
def handleArgs():
	parser = argparse.ArgumentParser(description='A simple zero MQ publisher for joystick messages')
	parser.add_argument('publish', nargs=2, help='publish messages to addr:port, ex. js 10.1.1.1 9000')
	parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
	args = vars(parser.parse_args())
	return args


def main():
	args = handleArgs()
	js = Joystick(args['publish'][0], args['publish'][1])
	js.run(args['verbose'])

if __name__ == "__main__":
	main()
