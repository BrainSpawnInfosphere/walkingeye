#!/usr/bin/env python

import wave  
import pyaudio

"""
Plays a wave file
in: file path and name
out: None
"""
def playWave(file):
	#define stream chunk   
	chunk = 1024  

	#open a wav format music  
	f = wave.open(file,"rb")  

	#instantiate PyAudio  
	p = pyaudio.PyAudio()  

	#open stream  
	stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
					channels = f.getnchannels(),  
					rate = f.getframerate(),  
					output = True)  
	#read data  
	data = f.readframes(chunk)  

	#paly stream  
	while data != '':  
		stream.write(data)  
		data = f.readframes(chunk)  

	#stop stream  
	stream.stop_stream()  
	stream.close()  

	#close PyAudio  
	p.terminate()  

"""
Gets intent from msg and handles errors and low confidence
in: wit.ai message
out: key (intent)
todo: duplicates of this
"""
def getKey(self,msg,min_confidence=0.5):
	#print msg

	# hangle errors ----------------------------
	if not msg:
		key = 'empty'
	elif msg['msg_body'] == '':
		key = 'empty'
	elif 'outcome' not in msg:
		key = 'error'
	elif 'confidence' not in msg['outcome']:
		key = 'error'
	elif msg['outcome']['confidence'] < min_confidence:
		key = 'error'
	else:
		key = msg['outcome']['intent']

	return key

if __name__ == '__main__':
	
	print 'there is nothing to run from the command line, bye ...'
	