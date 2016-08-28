#!/usr/bin/env python

from __future__ import print_function
from bag import Record
import argparse


def handleArgs():
	parser = argparse.ArgumentParser(description="""
	A simple zero MQ message tool. It will either publish messages on a specified
	topic or subscribe to a topic and print the messages.

	Format:
	- record host port topic -f|--file bag_file

	Examples:
	- record 1.1.1.1 9000 cmds --file /path/stuff.bag
	""")

	parser.add_argument('args', nargs=3, help='address port topic, ex. 1.1.1.1 9000 imu')
	# parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
	parser.add_argument('-f', '--file', help='name of bag file', default=None)
	args = vars(parser.parse_args())
	return args


def main():
	args = handleArgs()
	topic = args['args'][2]
	port = args['args'][1]
	host = args['args'][0]
	bag = args['file']

	rec = Record()
	# rec.run('test', 9000, 'localhost', 'test.bag')
	rec.run(topic, port, host, bag)


if __name__ == '__main__':
	main()
