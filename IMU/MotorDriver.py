#!/usr/bin/python

import Adafruit_MCP230xx as Ada
import RPi.GPIO as GPIO

class MotorDriver:
	STOP = 0
	FORWARD = 1
	REVERSE = 2
	COAST = 3

	def __init__(self,pwm0,pwm1,pwm2,pwm3):

		self.mux = Ada.Adafruit_MCP230XX(20,8,1)

		for pin in range(0,8):
			mux.config(pin,Ada.MCP230XX_GPIO.OUT)

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pwm0, GPIO.OUT)
		GPIO.setup(pwm1, GPIO.OUT)
		GPIO.setup(pwm2, GPIO.OUT)
		GPIO.setup(pwm3, GPIO.OUT)

		self.pwm0 = GPIO.PWM(pwm0, 100)
		self.pwm1 = GPIO.PWM(pwm1, 100)
		self.pwm2 = GPIO.PWM(pwm2, 100)
		self.pwm3 = GPIO.PWM(pwm3, 100)

	"""
	"""
	def setMotors(m0,m1,m2,m3):
		#if not 'dir' in m0 or not 'duty' in m0: return

		# set mux
		val = m3['dir']<<6 | m2['dir']<<4 | m1['dir']<<2 | m0['dir']
		self.mux.write8(val)

		#set pwm
		self.pwm0.ChangeDutyCycle(m0['duty']) # duty cycle: 0-100
		self.pwm1.ChangeDutyCycle(m1['duty']) # duty cycle: 0-100
		self.pwm2.ChangeDutyCycle(m2['duty']) # duty cycle: 0-100
		self.pwm3.ChangeDutyCycle(m3['duty']) # duty cycle: 0-100

	def allStop(self):
		self.mux.write8(0)

if __name__ == '__main__':
