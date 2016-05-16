#!/usr/bin/env python

from subprocess import call
import logging
# import datetime
from time import sleep
import tempfile
import StringIO

class Microphone(object):
	"""
	Uses SoX to capture audio from the default microphone
	"""
	def __init__(self, threshold='3%'):
		# sensitivity of silence recognition
		self.threshold = threshold
		logging.basicConfig(level=logging.INFO)
		self.logger = logging.getLogger('microphone')

	def __del__(self):
		# print 'Microphone ... goodbye'
		self.logger.debug('microphone closing')

	def playAudio(self,fileName):
		"""
		Plays back the captured audio
		in: file name
		out: none
		"""
		cmd = ['play', '-q', fileName]
		call(cmd)

	def readAudio(self,fileName):
		"""
		Reads a wave file into memory and stores it in a StringIO
		in: file name of wave
		out: returns the StringIO
		"""
		f=open(output_filename)
		byte = f.read(1)

		s = StringIO.StringIO()
		s.write(byte)
		while byte != '':
			byte=f.read(1)
			s.write(byte)
		return s

	def getAudio(self):
		"""
		from: https://wit.ai/docs/http/20160330#get-intent-via-text-link
		sox -d -b 16 -c 1 -r 16k sample.wav

		$ file sample.wav
			sample.wav: RIFF (little-endian) data, WAVE audio, Microsoft PCM, 16 bit, mono 16000 Hz

		$ curl -XPOST 'https://api.wit.ai/speech?v=20141022' \
			-i -L \
			-H "Authorization: Bearer $TOKEN" \
			-H "Content-Type: audio/wav" \
			--data-binary "@sample.wav"
		"""
		# print 'Ready'
		self.logger.debug('Ready')

		# rec -q -t wav -c 1 test.wav rate 8k silence 1 0.1 3% 1 3.0 3%
		temp = tempfile.NamedTemporaryFile()
		self.logger.debug('Openned tempfile: %s'%{temp.name})
		cmd = ['rec', '-q', '-t', 'wav', '-c', '1', temp.name, 'rate', '8k', 'silence', '1', '0.1', self.threshold, '1', '3.0', self.threshold]
		call(cmd)

		# print 'ok ... got it!'
		self.logger.debug('ok ... got it!')

		return temp

	def test(self):
		while True:
			filename = self.getAudio()
			self.playAudio(filename)
			snd = self.readAudio(filename)
			print 'Sound size: %s'%{snd.len}
			filename.close() # close tempfile
			snd.close() # close string.io buffer
			sleep(1)


def main():
	mic = Microphone()
	mic.test()


if	__name__ == "__main__":
	main()
