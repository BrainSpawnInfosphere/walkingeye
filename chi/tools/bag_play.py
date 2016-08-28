#!/usr/bin/env python

from __future__ import print_function
from bag import Play
import argparse


def handleArgs():
	parser = argparse.ArgumentParser(description="""
	A simple zero MQ message tool. It will play back a bag file as though a real
	node is publishing it.

	Format:
	- play port topic bag_file -l|--loop

	Examples:
	- play 9000 cmds /path/stuff.bag -l
	""")

	parser.add_argument('args', nargs=3, help='port topic bag, ex. 9000 imu ./path/imu_save.bag')
	# parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
	parser.add_argument('-l', '--loop', help='continuously loop through bag data', action='store_true')
	args = vars(parser.parse_args())
	return args


def main():
	args = handleArgs()
	port = args['args'][0]
	topic = args['args'][1]
	bag = args['args'][2]
	loop = args['loop']

	play = Play()
	# play.run('test.bag', 'bob', 9000, True)
	play.run(bag, topic, port, loop)


if __name__ == '__main__':
	main()
