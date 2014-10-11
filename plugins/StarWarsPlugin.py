#!/usr/bin/env python

from Module import *
import glob
import wave  



####################################################################
# 
# 
####################################################################
class Plugin(Module):
	def __init__(self):
		self.intent = 'star_wars'
		
		# setup Star Wars
		file = '/Users/kevin/Desktop/star_wars_sounds'
		self.star_wars_sounds = glob.glob(file + '/*.wav')
			
	"""
	"""
	def process(self, entity):
		sound = random.choice( self.star_wars_sounds )
		self.playWave( sound )
		return ''
		
	
	"""
	Plays a Wave file
	in: path to sound to play
	out: none
	"""
	def playWave(self,file):
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
	


if __name__ == '__main__':
	print 'bye ...'
	