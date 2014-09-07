#!/usr/bin/env python

import re
import os
import logging
import urllib2
import sys

headers = {"Host": "translate.google.com",
		   "Referer": "http://www.gstatic.com/translate/sound_player2.swf",
		   "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) "
		   "AppleWebKit/535.19 (KHTML, like Gecko) "
		   "Chrome/18.0.1025.163 Safari/535.19"
          }

#phrase = "ALERT, WARNING, WARNING, containment field about to fail, how now brown cow"
phrase = "Never ignore coincidence, unless, you're busy. In which case, always ignore coincidence"

#print 'Phrase length:',len(phrase)

# not sure what the real number is, Google seems finicky
if len(phrase) > 95:
	print 'Error: phrase must be less than 100 chars:',len(phrase)
	exit()

phrase = re.sub(' ','%20',phrase)

# try changing tl=en-us or en-uk
http = 'http://translate.google.com/translate_tts?ie=UTF-8&q=%22' + phrase + '%22&tl=en-uk' 

ans = urllib2.Request(http,'',headers)
responce = urllib2.urlopen(ans)

# write to disk
filename = 'test.mp3'
out = open(filename,'w')
out.write( responce.read() )
out.close()

os.system('afplay %s'%filename)