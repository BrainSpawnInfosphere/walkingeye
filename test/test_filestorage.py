#!/usr/bin/env python


import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import lib.FileStorage as Fs


def test_yaml():
	data = {
		'bob': 1,
		'tom': 2,
		'sam': 3
	}

	fname = 'test.yaml'

	fs = Fs.FileStorage()
	fs.writeYaml(fname, data)
	fs.clear()
	fs.readYaml(fname)

	# print fs.db
	os.remove(fname)

	assert fs.db == data


def test_json():
	data = {
		'bob': 1,
		'tom': 2,
		'sam': 3
	}

	fname = 'test.json'

	fs = Fs.FileStorage()
	fs.writeJson(fname, data)
	fs.clear()
	fs.readJson(fname)

	# print fs.db
	os.remove(fname)

	assert fs.db == data
