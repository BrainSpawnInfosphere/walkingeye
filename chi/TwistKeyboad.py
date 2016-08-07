#!/usr/bin/env python
#
# by Kevin J. Walchko 6 Aug 2016
#


from __future__ import print_function
from __future__ import division
import argparse
import sys, tty, termios
import lib.zmqclass as Zmq
import lib.Messages as Msg


class Keyboard(object):
	"""
	Keyboard class to handle input and then
	publish the it via ZeroMQ.

	Still needs lots of work and a true purpose :)
	"""
	def __init__(self, host, port):
		self.addr = (host, port)
		pass

	def run(self):
		pub = Zmq.Pub(self.addr)
		twist = Msg.Twist()

		# fd = sys.stdin.fileno()
		# tty.setraw(sys.stdin.fileno())

		while True:
			# have to do some fancy stuff to avoid sending \n all the time
			fd = sys.stdin.fileno()
			old_settings = termios.tcgetattr(fd)
			try:
				tty.setraw(fd)
				key = sys.stdin.read(1)
			finally:
				termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

			print('>>>', key)

			if key == 'a': twist['angular']['z'] += 0.1
			elif key == 'd': twist['angular']['z'] -= 0.1
			elif key == 'w': twist['linear']['x'] += 0.1
			elif key == 'x': twist['linear']['y'] -= 0.1
			elif key == 's':  # stop - all 0's
				twist.update(dict(linear=Msg.Vector()))
				twist.update(dict(angular=Msg.Vector()))
			elif key == 'q': exit()

			pub.pub('twist_kb', twist)


# set up and handle command line args
def handleArgs():
	parser = argparse.ArgumentParser(description='A simple zero MQ publisher for keyboard messages')
	parser.add_argument('-p', '--publish', nargs=2, help='publish messages to addr:port, ex. js 10.1.1.1 9000', default=['localhost', '9000'])
	# parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
	args = vars(parser.parse_args())
	return args


def main():
	args = handleArgs()

	print('------------------------')
	print('q - quit')
	print('------------------------')
	print('w - forward')
	print('a/d - left/right')
	print('x - reverse')
	print('s - stop')
	print('------------------------')

	kb = Keyboard(args['publish'][0], args['publish'][1])
	kb.run()

	# clean-up
	print('Bye ...')


if __name__ == "__main__":
	main()
