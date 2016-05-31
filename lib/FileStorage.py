#!/usr/bin/env python

import yaml
import json


class FileStorageError(Exception):
	pass


class FileStorage(object):
	"""
	Store your API keys or other params in a json/yaml file and then import them
	with this class. You can also pass a dictionary to this and create a json/yaml
	file storage. All key/value pairs are stored in a dictionary called db.
	"""
	db = None

	def readYaml(self, fname):
		"""
		Reads a Yaml file
		"""
		try:
			f = open(fname, 'r')
			d = yaml.safe_load(f)
			f.close()
			self.db = d
			return len(self.db)
		except IOError:
			# print '[-] YamlDoc: IOError'
			raise FileStorageError('Could not open %s for reading' % (fname))

	def writeYaml(self, filename, data=None):
		"""
		Writes a Yaml file
		"""
		if data is None:
			data = self.db
		f = open(filename, 'w')
		yaml.safe_dump(data, f)
		f.close()

	def readJson(self, fname):  # FIXME: 20160522
		"""
		Reads a Json file
		"""
		try:
			with open(fname, 'r') as f:
				data = json.load(f)

			self.db = data
			return len(self.db)
		except IOError:
			# print '[-] YamlDoc: IOError'
			raise FileStorageError('Could not open %s for reading' % (fname))

	def writeJson(self, fname, data=None):  # FIXME: 20160522
		"""
		Writes a Json file
		"""
		try:
			if data is None:
				data = self.db

			with open(fname, 'w') as f:
				json.dump(data, f)

		except IOError:
			# print '[-] YamlDoc: IOError'
			raise FileStorageError('Could not open %s for writing' % (fname))

	def getKey(self, keyName):
		"""
		Given a key, returns a value
		in: key
		out: value or None
		"""
		if keyName in self.db: return self.db[keyName]
		else: return None

	def clear(self):
		self.db = None

# 
# def test_yaml():
# 	data = {
# 		'bob': 1,
# 		'tom': 2,
# 		'sam': 3
# 	}
#
# 	fname = 'test.yaml'
#
# 	fs = FileStorage()
# 	fs.writeYaml(fname, data)
# 	fs.clear()
# 	fs.readYaml(fname)
#
# 	# print fs.db
#
# 	assert fs.db == data
#
#
# def test_json():
# 	data = {
# 		'bob': 1,
# 		'tom': 2,
# 		'sam': 3
# 	}
#
# 	fname = 'test.json'
#
# 	fs = FileStorage()
# 	fs.writeJson(fname, data)
# 	fs.clear()
# 	fs.readJson(fname)
#
# 	# print fs.db
#
# 	assert fs.db == data

if __name__ == "__main__":
	print 'good bye cowboy!'
