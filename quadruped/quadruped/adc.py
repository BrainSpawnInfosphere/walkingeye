#!/usr/bin/env python

# Driver for the MCP3208 ADC

# import platform

try:
	import Adafruit_GPIO.SPI as SPI
	# import Adafruit_MCP3008
	import Adafruit_GPIO as GPIO

	class MCP3208(object):
		"""Class to represent an Adafruit MCP3008 analog to digital converter.
		"""

		def __init__(self, clk=None, cs=None, miso=None, mosi=None, spi=None, gpio=None):
			"""Initialize MAX31855 device with software SPI on the specified CLK,
			CS, and DO pins.  Alternatively can specify hardware SPI by sending an
			Adafruit_GPIO.SPI.SpiDev device in the spi parameter.
			"""
			self._spi = None
			# Handle hardware SPI
			if spi is not None:
				self._spi = spi
			elif clk is not None and cs is not None and miso is not None and mosi is not None:
				# Default to platform GPIO if not provided.
				if gpio is None:
					gpio = GPIO.get_platform_gpio()
				self._spi = SPI.BitBang(gpio, clk, mosi, miso, cs)
			else:
				raise ValueError('Must specify either spi for for hardware SPI or clk, cs, miso, and mosi for softwrare SPI!')
			self._spi.set_clock_hz(1000000)
			self._spi.set_mode(0)
			self._spi.set_bit_order(SPI.MSBFIRST)

		def read_adc(self, adc_number):
			"""Read the current value of the specified ADC channel (0-7).  The values
			can range from 0 to 1023 (10-bits).
			"""
			assert 0 <= adc_number <= 7, 'ADC number must be a value of 0-7!'
			# Build a single channel read command.
			# For example channel zero = 0b11000000
			command = 0b11 << 6                  # Start bit, single channel read
			command |= (adc_number & 0x07) << 3  # Channel number (in 3 bits)
			# Note the bottom 3 bits of command are 0, this is to account for the
			# extra clock to do the conversion, and the low null bit returned at
			# the start of the response.
			resp = self._spi.transfer([command, 0x0, 0x0])
			# Parse out the 10 bits of response data and return it.
			result = (resp[0] & 0x01) << 9
			result |= (resp[1] & 0xFF) << 1
			result |= (resp[2] & 0x80) >> 7
			return result & 0x3FF

except ImportError:
	print('WARNING: Using fake MCP3208 (ADC) and SPI library')

	class SPI(object):
		@staticmethod
		def SpiDev(a, b):
			pass

	class MCP3208(object):
		def __init__(self, clk=None, cs=None, miso=None, mosi=None, spi=None, gpio=None):
			pass

		def read_adc(self, adc_number):
			return 1024
