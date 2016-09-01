#!/usr/bin/env python


import os
import sys
import multiprocessing as mp
sys.path.insert(0, os.path.abspath('..'))
import lib.zmqclass as zmq


def test_pub_sub():
	tcp = ('127.0.0.1', 9000)
	pub = zmq.Pub(tcp)
	sub = zmq.Sub('test', tcp)
	tmsg = {'a': 1, 'b': 2}
	while True:
		pub.pub('test', tmsg)
		topic, msg = sub.recv()

		if msg:
			assert msg == tmsg
			assert topic == 'test'
			break


def test_serivce():

	ans = {'a': 1, 'b': 2}

	class tServer(mp.Process):
		def __init__(self):
			mp.Process.__init__(self)

		def run(self):
			tcp = ('127.0.0.1', 9000)
			serv = zmq.ServiceProvider(tcp)
			serv.listen(self.callback)
			return 0

		def callback(self, msg):
			return msg

	s = tServer()
	s.start()

	tcp = ('127.0.0.1', 9000)
	client = zmq.ServiceClient(tcp)
	msg = client.get(ans)
	assert msg == ans

	s.terminate()
	s.join()
