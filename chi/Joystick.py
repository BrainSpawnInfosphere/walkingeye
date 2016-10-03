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
import lib.zmqclass as zmq
import lib.Messages as Msg


class Joystick(object):
	"""
	Joystick class setup to handle a Playstation PS4 Controller and then
	publish the outputs via ZeroMQ.

	Buttons
	    Square  = joystick button 0
	    X       = joystick button 1
	    Circle  = joystick button 2
	    Triangle= joystick button 3
	    L1      = joystick button 4
	    R1      = joystick button 5
	    L2      = joystick button 6
	    R2      = joystick button 7
	    Share   = joystick button 8
	    Options = joystick button 9
	    L3      = joystick button 10
	    R3      = joystick button 11
	    PS      = joystick button 12
	    PadPress= joystick button 13

	Axes:
	    LeftStickX      = X-Axis
	    LeftStickY      = Y-Axis (Inverted?)
	    RightStickX     = 3rd Axis
	    RightStickY     = 4th Axis (Inverted?)
	    L2              = 5th Axis (-1.0f to 1.0f range, unpressed is -1.0f)
	    R2              = 6th Axis (-1.0f to 1.0f range, unpressed is -1.0f)
	    DPadX           = 7th Axis
	    DPadY           = 8th Axis (Inverted?)

	"""
	def __init__(self, host, port):
		self.pub = zmq.Pub((host, port))

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
		print('   publishing: {}:{}'.format(host, port))
		print('==========================================')

	def run(self, verbose, rate):
		js = self.js
		dt = 1.0/float(rate)
		ps4 = Msg.Joystick()

		while True:
			try:
				sdl2.SDL_JoystickUpdate()

				# left axis
				x = sdl2.SDL_JoystickGetAxis(js, 0) / 32768
				y = sdl2.SDL_JoystickGetAxis(js, 1) / 32768
				ps4['axes']['leftStick'] = [x, y]

				# right axis
				x = sdl2.SDL_JoystickGetAxis(js, 2) / 32768
				y = sdl2.SDL_JoystickGetAxis(js, 5) / 32768
				ps4['axes']['rightStick'] = [x, y]

				# other axes
				ps4['axes']['L2'] = sdl2.SDL_JoystickGetAxis(js, 3) / 32768
				ps4['axes']['R2'] = sdl2.SDL_JoystickGetAxis(js, 4) / 32768

				# accels
				x = sdl2.SDL_JoystickGetAxis(js, 6) / 32768
				y = sdl2.SDL_JoystickGetAxis(js, 7) / 32768
				z = sdl2.SDL_JoystickGetAxis(js, 8) / 32768
				ps4['axes']['accels'] = [x, y, z]

				# gyros
				x = sdl2.SDL_JoystickGetAxis(js, 9) / 32768
				y = sdl2.SDL_JoystickGetAxis(js, 10) / 32768
				z = sdl2.SDL_JoystickGetAxis(js, 11) / 32768
				ps4['axes']['gyros'] = [x, y, z]

				# get buttons
				ps4['buttons']['s'] = sdl2.SDL_JoystickGetButton(js, 0)
				ps4['buttons']['x'] = sdl2.SDL_JoystickGetButton(js, 1)
				ps4['buttons']['o'] = sdl2.SDL_JoystickGetButton(js, 2)
				ps4['buttons']['t'] = sdl2.SDL_JoystickGetButton(js, 3)
				ps4['buttons']['L1'] = sdl2.SDL_JoystickGetButton(js, 4)
				ps4['buttons']['R1'] = sdl2.SDL_JoystickGetButton(js, 5)
				ps4['buttons']['L2'] = sdl2.SDL_JoystickGetButton(js, 6)
				ps4['buttons']['R2'] = sdl2.SDL_JoystickGetButton(js, 7)
				ps4['buttons']['share'] = sdl2.SDL_JoystickGetButton(js, 8)
				ps4['buttons']['options'] = sdl2.SDL_JoystickGetButton(js, 9)
				ps4['buttons']['L3'] = sdl2.SDL_JoystickGetButton(js, 10)
				ps4['buttons']['R3'] = sdl2.SDL_JoystickGetButton(js, 11)
				ps4['buttons']['ps'] = sdl2.SDL_JoystickGetButton(js, 12)
				ps4['buttons']['pad'] = sdl2.SDL_JoystickGetButton(js, 13)

				# get hat
				# [up right down left] = [1 2 4 8]
				ps4['buttons']['hat'] = sdl2.SDL_JoystickGetHat(js, 0)

				# print('b 12', sdl2.SDL_JoystickGetButton(js, 12))
				# print('b 13', sdl2.SDL_JoystickGetButton(js, 13))

				if verbose: print(Msg.Joystick.screen(ps4))

				self.pub.pub('js', ps4)
				time.sleep(dt)

			except (IOError, EOFError):
				print('[-] Connection gone .... bye')
				break
			# except Exception as e:
			# 	print('Ooops:', e)
			# else:
			# 	raise Exception('Joystick: Something bad happened!')

		# clean-up
		sdl2.SDL_JoystickClose(js)
		print('Bye ...')


# set up and handle command line args
def handleArgs():
	parser = argparse.ArgumentParser(description='A simple zero MQ publisher for joystick messages')
	parser.add_argument('publish', nargs=2, help='publish messages to addr:port, ex. js 10.1.1.1 9000')
	parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
	parser.add_argument('-r', '--rate', help='publish rate in Hz, default is 1.0 Hz', default=1.0)
	args = vars(parser.parse_args())
	return args


def main():
	args = handleArgs()
	js = Joystick(args['publish'][0], args['publish'][1])
	js.run(args['verbose'], args['rate'])

if __name__ == "__main__":
	main()
