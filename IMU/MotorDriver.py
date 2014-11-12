#!/usr/bin/python

import Adafruit_MCP230xx as Ada

need pwm stuff too!

class MotorDriver:
	STOP = 0
	FORWARD = 1
	REVERSE = 2
	COAST = 3
	def __init__(self,m0,m1,m2,m3):
		self.m0 = m0
		self.m1 = m1
		self.m2 = m2
		self.m3 = m3
		
		self.mux = Ada.Adafruit_MCP230XX(20,8,1)
		
		for pin in range(0,8):
			mux.config(pin,Ada.MCP230XX_GPIO.OUT)
		
	"""
	"""
	def setMotors(m0,m1,m2,m3):
		# set mux
		val = m3.dir<<6 | m2.dir<<4 | m1.dir<<2 | m0.dir
		self.mux.write8(val)
		set pwm
		
	def allStop(self):
		self.mux.write8(0)

if __name__ == '__main__':
    
