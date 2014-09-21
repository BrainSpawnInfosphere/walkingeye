#!/usr/bin/env python

import re
import os
import logging
import urllib2
import sys
import StringIO
import pygame
import pyglet
import wave
import pyaudio

# global constants
FREQ = 16000   # same as audio CD
BITSIZE = -16  # unsigned 16 bit
CHANNELS = 1   # 1 == mono, 2 == stereo
BUFFER = 1024  # audio buffer size in no. of samples

headers = {"Host": "translate.google.com",
		   "Referer": "http://www.gstatic.com/translate/sound_player2.swf",
		   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) "
		   "AppleWebKit/535.19 (KHTML, like Gecko) "
		   "Chrome/18.0.1025.163 Safari/535.19"
          }

#phrase = "ALERT, WARNING, WARNING, containment field about to fail, how now brown cow"
#phrase = "Never ignore coincidence, unless, you're busy. In which case, always ignore coincidence"

#print 'Phrase length:',len(phrase)

	

def test():

# 	#pygame.init()
# 	pygame.mixer.init(FREQ, BITSIZE, CHANNELS, BUFFER)
# 	pygame.mixer.music.load( 'test.mp3' )
# 	pygame.mixer.music.play()
	
# 	music = pyglet.resource.media( 'test.mp3' )
# 	music.play()

	chunk = 1024
	wf = wave.open('red-alert.wav', 'rb')
	p = pyaudio.PyAudio()
	
	print wf.getsampwidth()
	
	stream = p.open(
		format = p.get_format_from_width(wf.getsampwidth()),
		channels = wf.getnchannels(),
		rate = wf.getframerate(),
		output = True)
	data = wf.readframes(chunk)

	while data != '':
		stream.write(data)
		data = wf.readframes(chunk)

	stream.close()
	p.terminate()
	
if __name__ == '__main__':
	#phrase = 'WARNING, WARNING, containment system about to fail, evacuate'
	#tts(phrase)
	test()