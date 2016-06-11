#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#


import curses
import argparse
import lib.zmqclass as Zmq
import lib.Messages as Msg
import time

class Keyboard(object):
	"""
	Joystick class setup to handle a Playstation PS4 Controller and then
	publish the outputs via ZeroMQ.
	"""
	def __init__(self, host, port):
		self.pub = Zmq.Pub((host, port))

		# init SDL2 and grab joystick
		# sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
		# self.js = sdl2.SDL_JoystickOpen(0)

		# grab info for display
		# a = sdl2.SDL_JoystickNumAxes(self.js)
		# b = sdl2.SDL_JoystickNumButtons(self.js)
		# h = sdl2.SDL_JoystickNumHats(self.js)

		# print '=========================================='
		# print ' Joystick '
		# print '   axes:', a, 'buttons:', b, 'hats:', h
		# print '=========================================='

	# def formatCmd(self, ps4):
	# 	"""
	# 	useful?
	#
	# 	This is a formatter ... could just send raw and have subscriber handle
	# 	it?
	# 	"""
	# 	# command template to be sent
	# 	cmd = {'cmd':
	# 		{
	# 			'linear': {'x': 0, 'y': 0},
	# 			'angular': {'x': 0, 'y': 0, 'z': 0},
	# 		}
	# 	}
	#
	# 	lx = float(ps4['la']['x']) / 32767.0
	# 	ly = float(ps4['la']['y']) / 32767.0
	#
	# 	cmd['cmd']['linear']['x'] = lx
	# 	cmd['cmd']['linear']['y'] = ly
	#
	# 	ax = float(ps4['la']['x']) / 32767.0
	# 	# ay = float(ps4['la']['y']) / 32767.0
	#
	# 	cmd['cmd']['angular']['z'] = ax
	#
	# 	# print cmd
	#
	# 	return cmd

	def run(self):

		while True:
			try:
				time.sleep(0.1)

			except (IOError, EOFError):
				print '[-] Connection gone .... bye'
				break

		# clean-up
		print 'Bye ...'


# set up and handle command line args
def handleArgs():
	parser = argparse.ArgumentParser(description='A simple zero MQ publisher for joystick messages')
	parser.add_argument('publish', nargs=2, help='publish messages to addr:port, ex. js 10.1.1.1 9000')
	parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
	args = vars(parser.parse_args())
	return args


def main():
	# args = handleArgs()
	pub = Zmq.Pub()
	try:
		stdscr = curses.initscr()
		stdscr.keypad(1)  # capture special keys like KEY_UP
		curses.echo()

		while True:
			stdscr.erase()
			stdscr.addstr(0, 0, '> ')
			stdscr.refresh()
			# time.sleep(0.1)
			c = 123
			buffer = []
			while c != ord('\n'):
				c = stdscr.getch()
				if c == ord('q'):
					curses.endwin()
					print 'bye'
					exit()
				elif c == curses.KEY_UP:
					stdscr.addstr(10, 10, '{}'.format('KEY_UP'))
					stdscr.refresh()
					msg = Msg.Twist()
					msg['linear']['x'] = 1.0
					pub.pub('cmd', msg)
					time.sleep(0.5)
					break
				elif c == curses.KEY_DOWN:
					stdscr.addstr(10, 10, '{}'.format('KEY_DOWN'))
					stdscr.refresh()
					msg = Msg.Twist()
					msg['linear']['x'] = -1.0
					pub.pub('cmd', msg)
					time.sleep(0.5)
					break
				elif c == curses.KEY_LEFT:
					stdscr.addstr(10, 10, '{}'.format('KEY_LEFT'))
					stdscr.refresh()
					msg = Msg.Twist()
					msg['linear']['y'] = 1.0
					pub.pub('cmd', msg)
					time.sleep(0.5)
					break
				elif c == curses.KEY_RIGHT:
					stdscr.addstr(10, 10, '{}'.format('KEY_RIGHT'))
					stdscr.refresh()
					msg = Msg.Twist()
					msg['linear']['y'] = -1.0
					pub.pub('cmd', msg)
					time.sleep(0.5)
					break
				else: buffer.append(chr(c))

			stdscr.addstr(''.join(buffer))
			stdscr.refresh()
			time.sleep(1)
	except:
		curses.beep()
		curses.endwin()


if __name__ == "__main__":
	main()
