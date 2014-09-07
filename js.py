#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#
# PS4 has 6 axes, 14 buttons, 1 hat
# This program doesn't grab all buttons, just the most useful :)

import sdl2
import time

import time
import json
from multiprocessing.connection import Client as Subscriber

###############################################
# Formats joystick into a ROS twist like message
###############################################
def formatCmd(ps4):
	# command template to be sent
	cmd = {'cmd': 
		{'linear': {'x': 0, 'y': 0}, 
		 'angular': {'x': 0, 'y': 0, 'z': 0}, 
		}
	
	lx = float(ps4['la']['x'])/32767.0
	ly = float(ps4['la']['y'])/32767.0
	
	cmd['cmd']['linear']['x'] = lx
	cmd['cmd']['linear']['y'] = ly
	
	
	ax = float(ps4['la']['x'])/32767.0
	#ay = float(ps4['la']['y'])/32767.0
	
	cmd['cmd']['angular']['z'] = ax
	
	return cmd

if __name__ == '__main__':
	
	# init SDL2
	sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
	
	js = sdl2.SDL_JoystickOpen(0)
	
	# grab info
	a = sdl2.SDL_JoystickNumAxes(js)
	b = sdl2.SDL_JoystickNumButtons(js)
	h = sdl2.SDL_JoystickNumHats(js)
	
	print '=========================================='
	print ' Joystick '
	print '   axes:',a,'buttons:',b,'hats:',h
	print '=========================================='
	
	
	# Data structure holding the PS4 info
	ps4 = {
		'la': {'x': 0, 'y': 0},  # left axis
		'ra': {'x': 0, 'y': 0},
		'lt1': 0, # left trigger 1
		'rt1': 0,
		'lt2': 0, # left trigger 2
		'rt2': 0,
		'circle': 0,  
		'triangle': 0,   
		'square': 0,
		'x': 0,
		'hat': 0,
		}
	
	s = Subscriber(("192.168.1.22",9000))
	
	while True:
		try:
			
			while True:
				sdl2.SDL_JoystickUpdate()
				
				# left axis
				ps4['la']['x'] = sdl2.SDL_JoystickGetAxis(js,0)
				ps4['la']['y'] = sdl2.SDL_JoystickGetAxis(js,1)
				
				# right axis
				ps4['ra']['x'] = sdl2.SDL_JoystickGetAxis(js,2)
				ps4['ra']['y'] = sdl2.SDL_JoystickGetAxis(js,5)
				
				# left trigger axis
				ps4['lt2'] = sdl2.SDL_JoystickGetAxis(js,3)
				
				# right trigger axis
				ps4['rt2'] = sdl2.SDL_JoystickGetAxis(js,4)
				
				# get buttons
				ps4['square'] = sdl2.SDL_JoystickGetButton(js,0)
				ps4['x'] = sdl2.SDL_JoystickGetButton(js,1)
				ps4['circle'] = sdl2.SDL_JoystickGetButton(js,2)
				ps4['triangle'] = sdl2.SDL_JoystickGetButton(js,3)
				ps4['lt1'] = sdl2.SDL_JoystickGetButton(js,4)
				ps4['rt1'] = sdl2.SDL_JoystickGetButton(js,5)
				
				# use share button as a quit
				quit = sdl2.SDL_JoystickGetButton(js,8)
				
				# get hat
				ps4['hat'] = sdl2.SDL_JoystickGetHat(js,0)
				
				s.send( formatCmd(ps4) )
				
				if quit == True:
					break
				
				time.sleep(0.1)
				
		except (IOError, EOFError):
			print '[-] Connection gone .... bye'
			break
	
	# clean-up
	s.close()	 
	sdl2.SDL_JoystickClose(js)
	print 'Bye ...'

