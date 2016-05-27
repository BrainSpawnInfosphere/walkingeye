#!/usr/bin/env python


import os
import sys
import multiprocessing as mp
sys.path.insert(0, os.path.abspath('..'))

import lib.zmqclass as zmq
# import lib.Messages as msg
# import lib.Camera as Camera
#
# nose.run('../lib/zmqclass.py')

def test_pub_sub():
	pub = zmq.Pub('tcp://127.0.0.1:9000')
	sub = zmq.Sub('test', 'tcp://127.0.0.1:9000')
	tmsg = {'a': 1, 'b': 2}
	while True:
		pub.pub('test', tmsg)
		topic, msg = sub.recv()

		if msg:
			assert msg == tmsg
			break


def test_serivce():

	ans = {'a': 1, 'b': 2}

	class tServer(mp.Process):
		def __init__(self):
			mp.Process.__init__(self)

		def run(self):
			serv = zmq.ServiceProvider('tcp://127.0.0.1:9000')
			serv.listen(self.callback)
			return 0

		def callback(self, msg):
			return msg

	s = tServer()
	s.start()

	client = zmq.ServiceClient('tcp://127.0.0.1:9000')
	msg = client.get(ans)
	assert msg == ans

	s.terminate()
	s.join()
