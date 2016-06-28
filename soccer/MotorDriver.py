#!/usr/bin/python

from __future__ import division
from __future__ import print_function

# since i do a lot of dev on Apple, this creates a fake interface
import platform
if platform.system().lower() == 'linux':
	# pip install Adafruit_MCP230XX
	from Adafruit_MCP230XX import Adafruit_MCP230XX as MCP230XX
	# import RPi.GPIO as GPIO  # PWM
	from RPi.GPIO import PWM, setmode, setup, cleanup, BCM, OUT

	# print('RPi detected:', GPIO.RPI_INFO['P1_REVISION'])
	# print('GPIO Version:', GPIO.VERSION)

else:
	class MCP230XX(object):  # mux
		def __init__(self, a, b, c): pass
		def write8(self, a): print('mux wrote:', a)
		def config(self, a, b): pass

	class PWM(object):  # motors
		def __init__(self, a, b): pass
		def start(self, a): pass
		def stop(self): pass
		def ChangeDutyCycle(self, a): print('ChangeDutyCycle', a)

	# class GPIO:  # this shit isn't working!!!!
	# I don't like this solution!!!
	BCM = 11
	OUT = 0
	def setmode(a): pass
	def setup(a, b): pass
	def cleanup(): pass


class MotorDriver(object):
	"""
	This uses RPI.GPIO
	"""
	STOP    = 0
	FORWARD = 1
	REVERSE = 2
	COAST   = 3

	def __init__(self, pwm0, pwm1, pwm2, pwm3):
		"""
		"""
		self.mux = MCP230XX(0x20, 16, 1)

		for pin in range(0, 15):
			self.mux.config(pin, OUT)

		# this can be:
		# BOARD -> Board numbering scheme. The pin numbers follow the pin numbers on header P1.
		# BCM -> Broadcom chip-specific pin numbers.
# 		GPIO.setmode(GPIO.BCM)
		setmode(BCM)  # Pi cover uses BCM pin numbers, GPIO.BCM = 11
		setup([pwm0, pwm1, pwm2, pwm3], OUT)  # GPIO.OUT = 0

		freq = 100.0  # Hz
		self.motor0 = PWM(pwm0, freq)
		self.motor1 = PWM(pwm1, freq)
		self.motor2 = PWM(pwm2, freq)
		self.motor3 = PWM(pwm3, freq)

		self.motor0.start(0)
		self.motor1.start(0)
		self.motor2.start(0)
		self.motor3.start(0)

	def __del__(self):
		print('motor drive ... bye')
		self.allStop()
		self.motor0.stop()
		self.motor1.stop()
		self.motor2.stop()
		self.motor3.stop()
		cleanup()

	def clamp(self, x):
		"""
		Clamps a PWM from 0-100 and puts it into the right servo usec timing.
		"""
		minimum = 0
		maximum = 100
		if x == 0: return 0  # really stop motor
		return max(minimum, min(x, maximum))

	def setMotors(self, m0, m1, m2, m3):
		"""
		Takes 4 dicts (shown below) for each motor.

		dict: {'dir': x, 'duty': 0-100}

		MotorDriver.STOP    = 0
		MotorDriver.FORWARD = 1
		MotorDriver.REVERSE = 2
		MotorDriver.COAST   = 3
		"""
		# if not 'dir' in m0 or not 'duty' in m0: return
		# low = 0
		# high = 100

		print(m0, m1, m2, m3)

		# set mux
		val = m3['dir'] << 6 | m2['dir'] << 4 | m1['dir'] << 2 | m0['dir']
		self.mux.write8(val)

		# set pwm
		pwm = self.clamp(m0['duty'])
		self.motor0.ChangeDutyCycle(pwm)

		pwm = self.clamp(m1['duty'])
		self.motor1.ChangeDutyCycle(pwm)

		pwm = self.clamp(m2['duty'])
		self.motor2.ChangeDutyCycle(pwm)

		pwm = self.clamp(m3['duty'])
		self.motor3.ChangeDutyCycle(pwm)

	def allStop(self):
		"""
		"""
		self.mux.write8(0)

		stop = {'dir': 0, 'duty': 0}
		self.setMotors(stop, stop, stop, stop)


def test():
	import time
	md = MotorDriver(4, 15, 14, 18)

	# duty cycle 0.0 - 100.0
	go = {'dir': MotorDriver.FORWARD, 'duty': 10}
	rev = {'dir': MotorDriver.REVERSE, 'duty': 25}
	stp = {'dir': MotorDriver.REVERSE, 'duty': 0}

	md.setMotors(go, go, go, go)
	time.sleep(10)
	md.setMotors(rev, rev, rev, rev)
	time.sleep(10)
	md.setMotors(go, stp, go, stp)
	time.sleep(10)
	md.setMotors(stp, rev, stp, rev)
	time.sleep(10)
	md.allStop()

if __name__ == '__main__':
	test()
