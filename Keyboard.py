#!/usr/bin/env python
#
# by Kevin J. Walchko 16 June 2016
#


from __future__ import print_function
from __future__ import division
import curses
import argparse
import lib.zmqclass as Zmq
import lib.Messages as Msg
import time


class Keyboard(object):
	"""
	Keyboard class to handle input and then
	publish the it via ZeroMQ.

	Still needs lots of work and a true purpose :)
	"""
	def __init__(self, host, port):
		# self.pub = Zmq.Pub((host, port))
		pass

	def run(self):
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
						# print('bye')
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
			return


# set up and handle command line args
def handleArgs():
	parser = argparse.ArgumentParser(description='A simple zero MQ publisher for joystick messages')
	parser.add_argument('pub', nargs=2, help='publish messages to addr:port, ex. js 10.1.1.1 9000')
	# parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
	args = vars(parser.parse_args())
	return args


def main():
	args = handleArgs()
	# print(args)
	kb = Keyboard(args['pub'][0], args['pub'][1])
	kb.run()

	# clean-up
	print('Bye ...')


if __name__ == "__main__":
	main()
