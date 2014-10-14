#!/usr/bin/python
#
# Kevin J. Walchko 12 Oct 2014
#

import os
import sys
import re
import urllib, urllib2
import time
import tempfile


"""
Uses Google translation to convert text-to-speech. Since there is a 100 word limit on tts this will also break up long sentences in smaller chunks. Google returns a mp3 file which is stored using tempfile and automatically is deleted once GoogleTTS quits.
"""
class GoogleTTS:
	def __init__(self):
		self.output = tempfile.NamedTemporaryFile()
		
	def __del__(self):
		self.output.close()
		
	def split_text(self,input_text, max_length=100):
		"""
		Try to split between sentences to avoid interruptions mid-sentence.
		Failing that, split between words.
		See split_text_rec
		"""
		return self.split_text_rec(input_text.replace('\n', ''),
							  ['([\,|\.|;]+)', '( )'])


	def split_text_rec(self,input_text, regexps, max_length=100):
		"""
		Split a string into substrings which are at most max_length.
		Tries to make each substring as big as possible without exceeding
		max_length.
		Will use the first regexp in regexps to split the input into
		substrings.
		If it it impossible to make all the segments less or equal than
		max_length with a regexp then the next regexp in regexps will be used
		to split those into subsegments.
		If there are still substrings who are too big after all regexps have
		been used then the substrings, those will be split at max_length.

		Args:
			input_text: The text to split.
			regexps: A list of regexps.
				If you want the separator to be included in the substrings you
				can add parenthesis around the regular expression to create a
				group. Eg.: '[ab]' -> '([ab])'

		Returns:
			a list of strings of maximum max_length length.
		"""
		if(len(input_text) <= max_length): return [input_text]

		#mistakenly passed a string instead of a list
		if isinstance(regexps, basestring): regexps = [regexps]
		regexp = regexps.pop(0) if regexps else '(.{%d})' % max_length

		text_list = re.split(regexp, input_text)
		combined_text = []
		#first segment could be >max_length
		combined_text.extend(split_text_rec(text_list.pop(0), regexps, max_length))
		for val in text_list:
			current = combined_text.pop()
			concat = current + val
			if(len(concat) <= max_length):
				combined_text.append(concat)
			else:
				combined_text.append(current)
				#val could be >max_length
				combined_text.extend(split_text_rec(val, regexps, max_length))
		return combined_text

	def tts(self,input_text):
		self.output.close()
		self.output = tempfile.NamedTemporaryFile()
		
		language='en-uk'
		
		#process input_text into chunks
		#Google TTS only accepts up to (and including) 100 characters long texts.
		#Split the text in segments of maximum 100 characters long.
		combined_text = self.split_text(input_text)

		#download chunks and write them to the output file
		for idx, val in enumerate(combined_text):
			mp3url = "http://translate.google.com/translate_tts?tl=%s&q=%s&total=%s&idx=%s" % (
				language,
				urllib.quote(val),
				len(combined_text),
				idx)
			headers = {"Host": "translate.google.com",
					   "Referer": "http://www.gstatic.com/translate/sound_player2.swf",
					   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) "
									 "AppleWebKit/535.19 (KHTML, like Gecko) "
									 "Chrome/18.0.1025.163 Safari/535.19"
			}
			req = urllib2.Request(mp3url, '', headers)
		
			if len(val) > 0:
				try:
					response = urllib2.urlopen(req)
					self.output.write(response.read())
					time.sleep(.5)
				except urllib2.URLError as e:
					print ('%s' % e)
					
		self.output.flush()
		return self.output.name
		

if __name__ == "__main__":
    g = GoogleTTS()
    file = g.tts('how now brown cow')
    os.system('afplay %s'%(file))
    file = g.tts('hickery dickery dock')
    os.system('afplay %s'%(file))
