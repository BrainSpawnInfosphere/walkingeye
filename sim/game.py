#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#
# charlotte mckinney -- hot!

import numpy as np
import matplotlib.pyplot as plt
from math import *

def rk4u(y,u,time,dt,F):
	#print 'y',y
	#print 'u',u
	#print 'time',time
	#print 'dt',dt
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
import cv

class KalmanFilter():
	def __init__(self):
		

class PID_Controller():
	def __init__(self):
		error = 0.0
		int_error = 0.0
		der_error = 0.0
		self.posD = np.array([0,0,0])
		self.velD = np.array([0,0,0])
		self.kp = 0.0
		self.ki = 0.0
		self.kd = 0.0
		
	def calc(pos,vel):
		e = pos - self.posD
		i = 0
	
	def setDesired(pos,vel):
		self.posD = pos
		self.velD = vel
		
	def setPID(p,i,d):
		self.kp = p
		self.ki = i
		self.kd = d

white = pygame.Color(255,255,255)
red = pygame.Color(255,100,100)
blue = pygame.Color(100,100,250)

class Robot():
	def __init__(self,window,pos,vel=(0,0,0)):
		#self.pos = np.array([[pos[0]],[pos[1]],[pos[2]]])
		#self.vel = np.array([[vel[0]],[vel[1]],[vel[2]]])
		self.pos = np.array([pos[0],pos[1],pos[2]])
		self.vel = np.array([vel[0],vel[1],vel[2]])
		self.u = np.array([0,0,0,0])
		self.window = window
		self.motor_angle = 45.0*pi/180.0
		
	def draw(self):
		pos = int(self.pos[0]), int(self.pos[1])
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
		
		y = np.array([xd,yd,pd,xdd,ydd,pdd])
		
		return y
		
	def process(self):
		time = pygame.time.get_ticks()
		time = time/1000.0
		
		y = np.array([self.pos[0],self.pos[1],self.pos[2],self.vel[0],self.vel[1],self.vel[2]])
		
		#u = np.array([2,2,-2.0,-2])
		u = self.u
		
		y = rk4u(y,u,time,1.0/30.0,self.dynamics)
		
		self.pos = y[0:3]
		self.vel = y[3:6] 
		
		self.draw()

	def commandVel(self,xd,yd,pd):
		p = self.motor_angle
		L = 0.05
		
		# FIXME -- i think good?
		f1=xd*sin(p)+yd*cos(p)+L*pd
		f2=-xd*sin(p)+yd*cos(p)+L*pd
		f3=-xd*sin(p)-yd*cos(p)+L*pd
		f4=xd*sin(p)-yd*cos(p)+L*pd
		
		u = np.array([f1,f2,f3,f4])
		self.u = u

def printScreen(msg,window,font,x=0,y=0):
	surf = font.render(msg ,False, red)
	surfrect = surf.get_rect()
	surfrect.topleft = (x,y)
	window.blit(surf, surfrect)

def main():
	pygame.init()
	fpsClock = pygame.time.Clock()
	font = pygame.font.Font('freesansbold.ttf',24)
	
	window = pygame.display.set_mode((640,480))
	
	robot = Robot(window,(200,200,0))
	
	run = True
	auto = False
	
	while run:
		window.fill( white )
		
		printScreen('Time: '+str(pygame.time.get_ticks()/1000.0),window,font)
		
		if auto:
			print 'hi'
		
		robot.process()
		for event in pygame.event.get():
			if event.type == QUIT:
				run = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE or event.key == K_q:
					run = False
				elif event.key == K_UP:
					robot.commandVel(0,-2,0)
				elif event.key == K_DOWN:
					robot.commandVel(0,2,0)
				elif event.key == K_LEFT:
					robot.commandVel(-2,0,0)
				elif event.key == K_RIGHT:
					robot.commandVel(2,0,0)
				
		
		pygame.display.update()
		fpsClock.tick(30)
		
	print 'bye ...'
	return 0

if __name__ == '__main__':
	main()