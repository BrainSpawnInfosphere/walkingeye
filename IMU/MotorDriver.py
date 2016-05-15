#!/usr/bin/python

import Adafruit_MCP230xx as Ada
# from RPIO import PWM
import RPi.GPIO as GPIO
import time


class MotorDriver(object):
	"""
	This uses RPI.GPIO

	"""
	STOP    = 0
	FORWARD = 1
	REVERSE = 2
	COAST   = 3

	def __init__(self,pwm0,pwm1,pwm2,pwm3):
		"""
		"""
		self.mux = Ada.Adafruit_MCP230XX(0x20,16,1)
		
		print 'RPi detected:',GPIO.RPI_INFO['P1_REVISION']
		print 'GPIO Version:',GPIO.VERSION

		for pin in range(0,15):
			self.mux.config(pin,Ada.MCP230XX_GPIO.OUT)
		
		# don't need these anymore
# 		self.pin0 = pwm0
# 		self.pin1 = pwm1
# 		self.pin2 = pwm2
# 		self.pin3 = pwm3
		
		# this can be: 
		# BOARD -> Board numbering scheme. The pin numbers follow the pin numbers on header P1.
		# BCM -> Broadcom chip-specific pin numbers. 
# 		GPIO.setmode(GPIO.BOARD)
		GPIO.setmode(GPIO.BCM) # Pi cover uses BCM pin numbers
# 		GPIO.setup(pwm0, GPIO.OUT)
# 		GPIO.setup(pwm1, GPIO.OUT)
# 		GPIO.setup(pwm2, GPIO.OUT)
# 		GPIO.setup(pwm3, GPIO.OUT)
		GPIO.setup([pwm0,pwm1,pwm2,pwm3], GPIO.OUT)
		
		freq = 100.0 # Hz
		self.motor0 = GPIO.PWM(pwm0,freq)
		self.motor1 = GPIO.PWM(pwm1,freq)
		self.motor2 = GPIO.PWM(pwm2,freq)
		self.motor3 = GPIO.PWM(pwm3,freq)
		
		self.motor0.start(0)
		self.motor1.start(0)
		self.motor2.start(0)
		self.motor3.start(0)
				
# 		self.motor0 = PWM.Servo(0)
		#self.motor0.stop_servo(self.pin0)
		
# 		self.motor1 = PWM.Servo(1)
		#self.motor1.stop_servo(self.pin1)
		
# 		self.motor2 = PWM.Servo(2)
		#self.motor2.stop_servo(self.pin2)
		
# 		self.motor3 = PWM.Servo(3)
		#self.motor3.stop_servo(self.pin3)

	def __del__(self):
		print 'motor drive ... bye'
		self.allStop()
		self.motor0.stop()
		self.motor1.stop()
		self.motor2.stop()
		self.motor3.stop()
		GPIO.cleanup()

	def clamp(self,x):
		"""
		Clamps a PWM from 0-100 and puts it into the right servo usec timing.
		"""
		minimum = 0
		maximum = 100
		if x == 0: return 0 # really stop motor
		return max(minimum, min(x, maximum))

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
		
		print m0,m1,m2,m3

		# set mux
		val = m3['dir']<<6 | m2['dir']<<4 | m1['dir']<<2 | m0['dir']
		print 'mux:',val
		self.mux.write8(val)

		#set pwm
		pwm = self.clamp(m0['duty'])
		print pwm
# 		self.motor0.set_servo(self.pin0,pwm)
		self.motor0.ChangeDutyCycle(pwm)
		
		pwm = self.clamp(m1['duty'])
		print pwm
# 		self.motor1.set_servo(self.pin1,pwm)
		self.motor1.ChangeDutyCycle(pwm)
		
		pwm = self.clamp(m2['duty'])
		print pwm
# 		self.motor2.set_servo(self.pin2,pwm)
		self.motor2.ChangeDutyCycle(pwm)
		
		pwm = self.clamp(m3['duty'])
		print pwm
# 		self.motor3.set_servo(self.pin3,pwm)
		self.motor3.ChangeDutyCycle(pwm)

	def allStop(self):
		"""
		"""
		self.mux.write8(0)
		
		stop = {'dir': 0, 'duty': 0}
		self.setMotors(stop,stop,stop,stop)

def test():
	import time
	md = MotorDriver(4,15,14,18)
	
	# duty cycle 0.0 - 100.0
	go  = {'dir': MotorDriver.FORWARD, 'duty': 10}
	rev = {'dir': MotorDriver.REVERSE, 'duty': 25}
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
