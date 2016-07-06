#!/usr/bin/env python

"""
This allows either real or fake interfaces to low level hardware. When actually
running on linux, the interfaces talk to real hardware. When running this on
any other OS, fake interfaces are created.
"""

# pip install Adafruit_Python_PCA9685
from __future__ import print_function
from __future__ import division

import platform

if platform.system().lower() == 'linux':
	from Adafruit_Python_PCA9685 import PCA9685
	from Adafruit_MCP230XX import Adafruit_MCP230XX as MCP230XX
	import RPi.GPIO as Gpio  # PWM
	# from RPi.GPIO import PWM, setmode, setup, cleanup, BCM, OUT
	# import Adafruit_MCP230xx  # if more i2c i/o needed
else:
	# put this in logger too?
	print('************ Using FAKE interfaces ************')

	import logging
	logging.basicConfig(level=logging.DEBUG)
	logger = logging.getLogger('fake')

	class PCA9685(object):
		def __init__(self): pass
		def set_pwm_freq(self, a): logger.debug('set_pwm_freq: %d', a)
		def set_pwm(self, a, b, c): logger.debug('set_pwm[%d]: %d %d', a, b, c)

	class MCP230XX(object):  # mux
		def __init__(self, a, b, c): pass
		def write8(self, a): logger.debug('mux wrote: %d', a)
		def config(self, a, b): pass

	class PWM(object):  # motors
		def __init__(self, a, b): pass
		def start(self, a): pass
		def stop(self): pass
		def ChangeDutyCycle(self, a): logger.debug('ChangeDutyCycle %d', a)

	class GPIO(object):
		BCM = 11
		OUT = 0
		IN = 1
		@staticmethod
		def setmode(a): pass
		@staticmethod
		def setup(a, b): pass
		@staticmethod
		def cleanup(): pass
		@staticmethod
		def PWM(a, b): return PWM(a, b)

	Gpio = GPIO()


def main():
	Gpio.setmode(Gpio.BCM)
	Gpio.setup(18, Gpio.OUT)
	pwm = Gpio.PWM(18, 100)
	pwm.start(10)
	pwm.ChangeDutyCycle(10)

if __name__ == "__main__":
	main()
