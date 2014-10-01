#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#

import numpy as np
import matplotlib.pyplot as plt
from math import *


	
	

def rk4u(y,u,time,dt,F):
	print 'y',y
	print 'u',u
	print 'time',time
	print 'dt',dt
	k1 = dt*F(y,u,time)
	k2 = dt*F(y+0.5*k1,u,time+0.5*dt)
	k3 = dt*F(y+0.5*k2,u,time+0.5*dt)
	k4 = dt*F(y+k3,u,time+dt)
	y_next = y+1.0/6.0*(k1+2.0*k2+2.0*k3+k4)
	return y_next
	
#################################################################

import pygame
import sys
from pygame.locals import *



white = pygame.Color(255,255,255)
red = pygame.Color(255,100,100)
blue = pygame.Color(100,100,250)

class Robot():
	def __init__(self,window,pos,vel=(0,0,0)):
		self.pos = pos
		self.vel = vel
		self.window = window
		
	def draw(self):
		pos = self.pos[0], self.pos[1]
		radius = 20;
		angle = self.pos[2]
		
		#           surface, color, center, radius, width
		pygame.draw.circle( self.window, red, pos, radius, 0 )
		pygame.draw.line(self.window, blue, pos, (radius*cos(angle)+pos[0],radius*sin(angle)+pos[1]),4)
	
	"""
	in:
		y=pos,vel
		u=f1,f2,f3,f4
		t=time(sec)
	out:
		
	"""
	def dynamics(self,y,u,t):
		m = 5.0
		j = 4.0
		p = 45.0*pi/180.0
		l = 0.05
		
		Fx = u[0]*sin(p)-u[1]*sin(p)-u[2]*sin(p)+u[3]*sin(p)
		Fy = u[0]*cos(p)+u[1]*cos(p)-u[2]*cos(p)-u[3]*cos(p)
		T = u[0]*l+u[1]*l+u[2]*l+u[3]*l
		
		xd = y[3]
		yd = y[4]
		pd = y[5]
		
		xdd=Fx/m+2*pd*yd
		ydd=Fy/m-2*pd*xd
		pdd=T/j
		
		y = xd,yd,pd,xdd,ydd,pdd
		
	def process(self):
		time = pygame.time.get_ticks()
		time = time/1000.0
		
		y = self.pos[0],self.pos[1],self.pos[2],self.vel[0],self.vel[1],self.vel[2]
		u = 1,0,0,0
		
		#y = rk4u(y,u,time,1.0/30.0,self.dynamics)
		
		self.pos = y[0],y[1],y[2]
		self.vel = y[3],y[4],y[5] 
		
		self.draw()

def main():
	pygame.init()
	fpsClock = pygame.time.Clock()
	
	window = pygame.display.set_mode((640,480))
	
	robot = Robot(window,(200,200,0))
	run = True
	while run:
		window.fill( white )
		
		robot.process()
		for event in pygame.event.get():
			if event.type == QUIT:
				run = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_q:
					run = False
		
		pygame.display.update()
		fpsClock.tick(30)
		
	print 'bye ...'
	return 0

if __name__ == '__main__':
	main()