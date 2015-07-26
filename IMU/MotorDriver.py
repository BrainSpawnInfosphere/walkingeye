#!/usr/bin/python

import Adafruit_MCP230xx as Ada
from RPIO import PWM
import time


class MotorDriver(object):
	"""
	This uses RPIO which replaced RPI.GPIO (name change I think)
	Current version is 0.10.0
	https://github.com/metachris/RPIO
	"""
	STOP    = 0
	FORWARD = 1
	REVERSE = 2
	COAST   = 3

	def __init__(self,pwm0,pwm1,pwm2,pwm3):
		"""
		"""
		self.mux = Ada.Adafruit_MCP230XX(0x20,8,1)

		for pin in range(0,8):
			self.mux.config(pin,Ada.MCP230XX_GPIO.OUT)
		
		self.pin0 = pwm0
		self.pin1 = pwm1
		self.pin2 = pwm2
		self.pin3 = pwm3
				
		self.motor0 = PWM.Servo(0)
		#self.motor0.stop_servo(self.pin0)
		
		self.motor1 = PWM.Servo(1)
		#self.motor1.stop_servo(self.pin1)
		
		self.motor2 = PWM.Servo(2)
		#self.motor2.stop_servo(self.pin2)
		
		self.motor3 = PWM.Servo(3)
		#self.motor3.stop_servo(self.pin3)

	def clamp(self,x):
		"""
		Clamps a PWM from 0-100 and puts it into the right servo usec timing.
		"""
		minimum = 0
		maximum = 100
		if x == 0: return 0 # really stop motor
		return max(minimum, min(x, maximum))*100+9000

	def setMotors(self,m0,m1,m2,m3):
		"""
		Takes 4 dicts (shown below) for each motor.
		
		dict: {'dir': x, 'duty': 0-100}
		
		MotorDriver.STOP    = 0
		MotorDriver.FORWARD = 1
		MotorDriver.REVERSE = 2
		MotorDriver.COAST   = 3
		"""
		#if not 'dir' in m0 or not 'duty' in m0: return
		
		low = 0
		high = 100

		# set mux
		val = m3['dir']<<6 | m2['dir']<<4 | m1['dir']<<2 | m0['dir']
		self.mux.write8(val)

		#set pwm
		pwm = self.clamp(m0['duty'])
		self.motor0.set_servo(self.pin0,pwm)
		
		pwm = self.clamp(m1['duty'])
		self.motor1.set_servo(self.pin1,pwm)
		
		pwm = self.clamp(m2['duty'])
		self.motor2.set_servo(self.pin2,pwm)
		
		pwm = self.clamp(m3['duty'])
		self.motor3.set_servo(self.pin3,pwm)

	def allStop(self):
		"""
		"""
		self.mux.write8(0)
		
		stop = {'dir': 0, 'duty': 0}
		self.setMotors(stop,stop,stop,stop)

def test():
	import time
	md = MotorDriver(17,18,22,23)
	
	go  = {'dir': MotorDriver.FORWARD, 'duty': 50}
	rev = {'dir': MotorDriver.REVERSE, 'duty': 100}
	stp = {'dir': MotorDriver.REVERSE, 'duty': 0}
	
	md.setMotors(go,go,go,go)
	time.sleep(10)
	md.setMotors(rev,rev,rev,rev)
	time.sleep(10)
	md.setMotors(go,stp,go,stp)
	time.sleep(10)
	md.setMotors(stp,rev,stp,rev)
	time.sleep(10)
	md.allStop()

if __name__ == '__main__':
	test()
