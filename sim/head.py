#!/usr/bin/env python
#
# by Kevin J. Walchko 2 Nov 2014
#
# 
#################################################################

import pygame
import sys
from pygame.locals import *
from plyer import accelerometer
import datetime as dt
import random

# colors
white = pygame.Color(255,255,255)
red = pygame.Color(255,100,100)
blue = pygame.Color(100,100,250)
gray = pygame.Color(200,200,200)

X = True
_ = False

emty = [[_,_,_,_,_,_,_,_],
		[_,_,_,_,_,_,_,_],
		[_,_,_,_,_,_,_,_],
		[_,_,_,_,_,_,_,_],
		[_,_,_,_,_,_,_,_],
		[_,_,_,_,_,_,_,_],
		[_,_,_,_,_,_,_,_],
		[_,_,_,_,_,_,_,_]]

"""
Simple timer class, that keeps track of a time delta (how long you want 
something to run for) and returns True when you check() the timer. This is
used for the animations of the Tengu.
"""
class Timer:
	def __init__(self,time=dt.timedelta(0,1,0),reset=True):
		self.epoch = dt.datetime.now()
		self.reset = reset
		self.delta = time 
		
	def setDeltaSeconds(self,sec):
		self.delta = dt.timedelta(0,sec,0) 
		
	def setDeltaMilliSeconds(self,msec):
		self.delta = dt.timedelta(0,0,msec*1000)
		
	def check(self): 
		ans = False
		if (dt.datetime.now()-self.epoch) > self.delta:
			ans = True
			self.epoch = dt.datetime.now()
		return ans

"""
This class spits out a character at a specified rate to animate a mouth. It
uses the Timer class above to keep track of time.
"""
class WordFIFO:
	def __init__(self):
		self.timer = Timer( dt.timedelta(0,0,100000) )
		self.word = 'hello'
		self.p = 0
		
	def setWord(self,w):
		self.word = w
		self.p = 0
		
	def next(self):
		l = len(self.word)
		ret = True
		
		if self.timer.check():
			self.p += 1
			if self.p == l-1:
				self.p = 0
				ret = False
				
		print self.word[self.p]	
		char = self.word[self.p]
		return ret,char	

class Tengu:
	Neutral = 1
	Angry = 2
	Sad = 4
	Happy = 8
	
	def __init__(self,led):
		self.led = led
		self.emmotion = Tengu.Neutral
		self.fifo = WordFIFO()
		self.timer = Timer()
		
	def drawFace(self,face):
		face[0] = [_,_,X,_,_,_,X,_]
		face[1] = [_,_,_,_,X,_,_,_]
		face[2] = [_,_,_,X,X,_,_,_]
		
	def drawMouth(self,face,mouth):
		if mouth == 'a':
			face[4] = [_,X,X,X,X,X,X,_]
			face[5] = [_,X,_,_,_,_,X,_]
			face[6] = [_,_,X,_,_,X,_,_]
			face[7] = [_,_,_,X,X,_,_,_]
		elif mouth == 'e':
			face[4] = [_,X,X,X,X,X,X,_]
			face[5] = [_,_,X,_,_,X,_,_]
			face[6] = [_,_,_,X,X,_,_,_]
		elif mouth == 'w' or mouth == 'r':
			face[4] = [_,_,_,X,X,_,_,_]
			face[5] = [_,_,X,_,_,X,_,_]
			face[6] = [_,_,X,_,_,X,_,_]
			face[7] = [_,_,_,X,X,_,_,_]
		elif mouth == 'm' or mouth == 'b' or mouth == 'p':
			face[4] = [_,_,X,X,X,X,_,_]
		elif mouth == 'o':
			face[4] = [_,_,_,X,X,_,_,_]
			face[5] = [_,_,X,_,_,X,_,_]
			face[6] = [_,_,_,X,X,_,_,_]
		elif mouth == 'u' or mouth == 'q':
			face[4] = [_,_,X,X,X,_,_,_]
			face[5] = [_,_,X,_,X,_,_,_]
			face[6] = [_,_,X,X,X,_,_,_]
			face[7] = [_,_,_,_,_,_,_,_]
		elif mouth == 'f' or mouth == 'v':
			face[4] = [_,X,X,X,X,X,X,_]
			face[5] = [_,X,_,_,_,_,X,_]
			face[6] = [_,_,X,X,X,X,_,_]
		elif mouth == 's' or mouth == 't':
			face[4] = [_,X,X,X,X,X,X,_]
			face[5] = [_,X,_,_,_,_,X,_]
			face[6] = [_,_,X,X,X,X,_,_]
		elif mouth == 'l' or mouth == 'n':
			face[4] = [_,X,X,X,X,X,X,_]
			face[5] = [_,X,_,_,_,_,X,_]
			face[6] = [_,X,_,_,_,_,X,_]
			face[7] = [_,_,X,X,X,X,_,_]
		else:
			face[4] = [_,X,X,X,X,X,X,_]
	
	def setWord(self, word = 'hello'):
		self.fifo.setWord( word )
	
	def draw(self,look=(0,0)):	
	
		face = [[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_]]
		
		
		self.drawFace(face)
		
		ret,char = self.fifo.next()
		if ret == False: char = ' '
		self.drawMouth(face,char)
			
		self.led.draw(face)

#####################################################

class TenguEmmo:
	Neutral = 1
	Angry = 2
	Sad = 4
	Happy = 8
	
	def __init__(self,led):
		self.led = led
		self.emmotion = TenguEmmo.Neutral
		
	def drawFace(self,face,row):
		face[row+0] = [_,_,X,_,_,_,X,_]
		face[row+1] = [_,_,_,_,X,_,_,_]
		face[row+2] = [_,_,_,X,X,_,_,_]
		
	def drawMouth(self,face,row,emmo):
		if emmo == TenguEmmo.Neutral:
			face[row+3] = [_,_,_,_,_,_,_,_]
			face[row+4] = [_,X,X,X,X,X,X,_]
			
		elif emmo == TenguEmmo.Happy:
			face[row+3] = [_,X,_,_,_,_,X,_]
			face[row+4] = [_,_,X,X,X,X,_,_]
			
		elif emmo == TenguEmmo.Sad:
			row = 3
			face[row+3] = [_,_,X,X,X,X,_,_]
			face[row+4] = [_,X,_,_,_,_,X,_]
			
		elif emmo == TenguEmmo.Angry:
			face[row+4] = [_,_,X,_,X,_,X,_]
			face[row+5] = [_,X,_,X,_,X,_,_]
	
	def setEmmotion(self, emmo):
		self.emmotion = emmo
	
	def draw(self,look=(0,0)):	
	
		face = [[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_]]
		
		
		self.drawFace(face,0)
		self.drawMouth(face,0,self.emmotion)
			
		self.led.draw(face)

#####################################################

class TenguAnimation:
	
	def __init__(self,led):
		self.led = led
		self.timer = Timer(dt.timedelta(0,0,200000))
		self.cnt = 0
		
	def drawFace(self,face):
		face[0] = [_,_,X,_,_,_,X,_]
		
	def drawMouth(self,face):
		if self.timer.check():
			self.cnt = (self.cnt + 1)%4
			
		if self.cnt == 0:
			
			face[1] = [_,_,_,_,_,_,_,_]
			face[2] = [_,_,_,X,_,_,_,_]
			face[3] = [_,_,_,_,_,_,_,_]
			face[4] = [_,_,_,X,X,_,X,_]
			face[5] = [_,X,_,X,X,_,_,_]
			face[6] = [_,_,_,_,_,_,_,_]
			face[7] = [_,_,_,_,X,_,_,_]
			
		elif self.cnt == 1:
			
			face[1] = [_,_,_,_,_,_,_,_]
			face[2] = [_,_,X,_,_,_,_,_]
			face[3] = [_,_,_,_,_,_,X,_]
			face[4] = [_,_,_,X,X,_,_,_]
			face[5] = [_,_,_,X,X,_,_,_]
			face[6] = [_,X,_,_,_,_,_,_]
			face[7] = [_,_,_,_,_,X,_,_]
		
# 		elif self.cnt == 2:
# 			
# 			face[1] = [_,_,_,_,_,_,_,_]
# 			face[2] = [_,X,_,_,_,_,X,_]
# 			face[3] = [_,_,_,_,_,_,_,_]
# 			face[4] = [_,_,_,X,X,_,_,_]
# 			face[5] = [_,_,_,X,X,_,_,_]
# 			face[6] = [_,_,_,_,_,_,_,_]
# 			face[7] = [_,X,_,_,_,_,X,_]
				
		elif self.cnt == 2:
			
			face[1] = [_,_,_,_,_,_,_,_]
			face[2] = [_,_,_,_,_,X,_,_]
			face[3] = [_,X,_,_,_,_,_,_]
			face[4] = [_,_,_,X,X,_,_,_]
			face[5] = [_,_,_,X,X,_,_,_]
			face[6] = [_,_,_,_,_,_,X,_]
			face[7] = [_,_,X,_,_,_,_,_]
			
		elif self.cnt == 3:
			
			face[1] = [_,_,_,_,_,_,_,_]
			face[2] = [_,_,_,_,X,_,_,_]
			face[3] = [_,_,_,_,_,_,_,_]
			face[4] = [_,X,_,X,X,_,_,_]
			face[5] = [_,_,_,X,X,_,X,_]
			face[6] = [_,_,_,_,_,_,_,_]
			face[7] = [_,_,_,X,_,_,_,_]
			
	def draw(self,look=(0,0)):	
	
		face = [[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_]]
		
		
		self.drawFace(face)
		self.drawMouth(face)
			
		self.led.draw(face)

######################################################################

		
class SymbolEye():
	Question = 0
	Exclaimation = 1
	Battery = 2
	Dead = 4
	
	def __init__(self,led):
		self.led = led
		self.pic = SymbolEye.Exclaimation
	
	def setSymbol(self,s):
		self.pic = s
	
	def draw(self,look):
		eye = 0
		pic = self.pic
		
		if pic == SymbolEye.Exclaimation:	
			eye = [	[_,_,_,X,X,_,_,_],
					[_,_,_,X,X,_,_,_],
					[_,_,_,X,X,_,_,_],
					[_,_,_,X,X,_,_,_],
					[_,_,_,X,X,_,_,_],
					[_,_,_,_,_,_,_,_],
					[_,_,_,X,X,_,_,_],
					[_,_,_,X,X,_,_,_]]
		
		elif pic == SymbolEye.Question:	
			eye = [	[_,_,X,X,X,X,_,_],
					[_,X,X,X,X,X,X,_],
					[_,X,X,_,_,X,X,_],
					[_,_,_,_,X,X,_,_],
					[_,_,_,X,X,_,_,_],
					[_,_,_,_,_,_,_,_],
					[_,_,_,X,X,_,_,_],
					[_,_,_,X,X,_,_,_]]
		
		elif pic == SymbolEye.Battery:	
# 			eye = [	[_,_,X,X,X,X,_,_],
# 					[_,X,X,_,_,X,X,_],
# 					[_,X,_,_,_,_,X,_],
# 					[_,X,_,_,_,_,X,_],
# 					[_,X,_,_,_,_,X,_],
# 					[_,X,_,_,_,_,X,_],
# 					[_,X,_,_,_,_,X,_],
# 					[_,X,X,X,X,X,X,_]]

			eye = [	[_,_,_,X,X,_,_,_],
					[_,_,X,X,X,X,_,_],
					[_,_,X,_,_,X,_,_],
					[_,_,X,_,_,X,_,_],
					[_,_,X,_,_,X,_,_],
					[_,_,X,_,_,X,_,_],
					[_,_,X,_,_,X,_,_],
					[_,_,X,X,X,X,_,_]]
					
		elif pic == SymbolEye.Dead:	
			eye = [	[_,_,_,_,_,_,_,_],
					[_,X,_,_,_,_,X,_],
					[_,_,X,_,_,X,_,_],
					[_,_,_,X,X,_,_,_],
					[_,_,_,X,X,_,_,_],
					[_,_,X,_,_,X,_,_],
					[_,X,_,_,_,_,X,_],
					[_,_,_,_,_,_,_,_]]
					
		self.led.draw(eye)

class CylonEye():
	def __init__(self,led):
		self.led = led
		self.epoch = dt.datetime.now()
		self.cnt = 0
		self.dir = 0
		self.scan = dt.timedelta(0,0,100000)
	
	def fillRow(self,i,a):
		a[i] = [X,X,X,X,X,X,X,X]
		
	def fillCol(self,i,a):
		for j in range (0,8):
			a[j][i] = X
	
	def draw(self,look):
		if (dt.datetime.now()-self.epoch) > self.scan:
			self.epoch = dt.datetime.now()
			
			if self.dir == 0 and self.cnt == 7: self.dir = 1
			elif self.dir == 1 and self.cnt == 0: self.dir = 0
			
			if self.dir == 0: self.cnt += 1
			else: self.cnt -= 1
			
		eye = [	[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_],
				[_,_,_,_,_,_,_,_]]
		
		self.fillRow(self.cnt,eye)
		#self.fillCol(self.cnt,eye)
		
		self.led.draw(eye)
		

class LED_Matrix():
	def __init__(self,window):
		self.window = window
		
	def draw(self,pattern):
		ox = 100
		oy = 100
		
		#pygame.draw.rect( self.window, gray, (ox,oy,300,300), 0 )
		
		radius = 5
		for i in range(0,8):
			for j in range(0,8):
				color = gray
				if pattern[j][i] == 1:
					color = blue
				space = 2
				pos = ox+space*i*radius,oy+space*j*radius
				pygame.draw.circle( self.window, color, pos, radius, 0 )


def printScreen(msg,window,font,x=0,y=0):
	surf = font.render(msg ,False, red)
	surfrect = surf.get_rect()
	surfrect.topleft = (x,y)
	window.blit(surf, surfrect)

def grav(g):
	look = 0
	if abs(g) > 150: 
		if g > 0: look = 3
		else: look = -3
	elif abs(g) > 100:  
		if g > 0: look = 2
		else: look = -2
	elif abs(g) > 50:  
		if g > 0: look = 1
		else: look = -1
	
	return look

def main():
	pygame.init()
	fpsClock = pygame.time.Clock()
	font = pygame.font.Font('freesansbold.ttf',24)
	
	accelerometer.enable()
	
	window = pygame.display.set_mode((640,480))
	
	led = LED_Matrix(window)
	eye = TenguEmmo(led)
	run = True
	
	while run:
		window.fill( white )
		
		printScreen('Time: '+str(pygame.time.get_ticks()/1000.0),window,font)
		
		g = accelerometer.acceleration
		gx,gy,gz = g
		
		if not gx: 
			gx,gy = (0,0)
		
		look = [0,0]
		
		# X
		look[0] = grav(gx)
		
		# Y
		look[1] = grav(gy)
		
		eye.draw(look)
		
		for event in pygame.event.get():
			if event.type == QUIT:
				run = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_q:
					run = False
				elif event.key == K_a:
 					eye = TenguAnimation(led)
				
				elif event.key == K_e:
 					eye = TenguEmmo(led)
 					eye.setEmmotion(random.choice([1,2,4,8]))
 					
				elif event.key == K_s:
 					eye = SymbolEye(led)
 					eye.setSymbol(random.choice([0,1,2,4]))
 				
 				elif event.key == K_c:
 					eye = CylonEye(led)
 				
 				elif event.key == K_t:
 					eye = Tengu(led)
 					eye.setWord('hello how are you today my fine friend')
 					
#  				elif event.key == K_n:
#  					
#  				elif event.key == K_RIGHT:
				
		
		pygame.display.update()
		fpsClock.tick(30)
		
	print 'bye ...'
	return 0

if __name__ == '__main__':
	main()