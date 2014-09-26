#!/usr/bin/python

# Python library for Adafruit Flora Accelerometer/Compass Sensor (LSM303).
# This is pretty much a direct port of the current Arduino library and is
# similarly incomplete (e.g. no orientation value returned from read()
# method).	This does add optional high resolution mode to accelerometer
# though.

# Copyright 2013 Adafruit Industries

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

from Adafruit_I2C import Adafruit_I2C

"""
"""
class Adafruit_LSM303(Adafruit_I2C):

	# Minimal constants carried over from Arduino library
	LSM303_ADDRESS_ACCEL = 0x18 
	LSM303_ADDRESS_MAG	 = (0x3C >> 1)	# 0011110x
											 # Default	  Type
	LSM303_REGISTER_ACCEL_CTRL_REG1_A = 0x20 # 00000111	  rw
	LSM303_REGISTER_ACCEL_CTRL_REG4_A = 0x23 # 00000000	  rw
	LSM303_REGISTER_ACCEL_OUT_X_L_A	  = 0x28
	LSM303_REGISTER_MAG_CRB_REG_M	  = 0x01
	LSM303_REGISTER_MAG_MR_REG_M	  = 0x02
	LSM303_REGISTER_MAG_OUT_X_H_M	  = 0x03
	LSM303_STATUS_REG_A				  = 0x27
	LSM303_STATUS_REG_ZYXDA_READY	  = 0x08
	
	# Gain settings for setMagGain()
	LSM303_MAGGAIN_1_3 = 0x20 # +/- 1.3
	LSM303_MAGGAIN_1_9 = 0x40 # +/- 1.9
	LSM303_MAGGAIN_2_5 = 0x60 # +/- 2.5
	LSM303_MAGGAIN_4_0 = 0x80 # +/- 4.0
	LSM303_MAGGAIN_4_7 = 0xA0 # +/- 4.7
	LSM303_MAGGAIN_5_6 = 0xC0 # +/- 5.6
	LSM303_MAGGAIN_8_1 = 0xE0 # +/- 8.1

	"""
	"""
	def __init__(self, busnum=-1, debug=False, hires=False):

		# Accelerometer and magnetometer are at different I2C
		# addresses, so invoke a separate I2C instance for each
		self.accel = Adafruit_I2C(self.LSM303_ADDRESS_ACCEL, busnum, debug)
		self.mag   = Adafruit_I2C(self.LSM303_ADDRESS_MAG  , busnum, debug)

		# Enable the accelerometer
		self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG1_A, 0x27)
		# Select hi-res (12-bit) or low-res (10-bit) output mode.
		# Low-res mode uses less power and sustains a higher update rate,
		# output is padded to compatible 12-bit units.
		if hires:
			self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG4_A,
			  0b00001000)
		else:
			self.accel.write8(self.LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0)
  
		# Enable the magnetometer
		self.mag.write8(self.LSM303_REGISTER_MAG_MR_REG_M, 0x00)
		
		# set default bias
		self.ax_mean = 0.0
		self.ay_mean = 0.0
		self.az_mean = 0.0
		
		self.mx_mean = 0.0
		self.my_mean = 0.0
		self.mz_mean = 0.0
		
		# now update these biases with good values
		self.calibrate()


	# Interpret signed 12-bit acceleration component from list
	def accel12(self, list, idx):
		n = list[idx] | (list[idx+1] << 8) # Low, high bytes
		if n > 32767: n -= 65536		   # 2's complement signed
		return n >> 4					   # 12-bit resolution


	# Interpret signed 16-bit magnetometer component from list
	def mag16(self, list, idx):
		n = (list[idx] << 8) | list[idx+1]	 # High, low bytes
		return n if n < 32768 else n - 65536 # 2's complement signed
	
	"""
	Reads the accel and magnetic 
	in: None
	out: accel [x,y,z] and mag[x,y,z,heading]
	todo: calculate heading, currently always 0.0
	"""
	def read(self):
		accel = self.accel.readReg(self.LSM303_REGISTER_ACCEL_OUT_X_L_A | 0x80)
		mag = self.mag.readReg(self.LSM303_REGISTER_MAG_OUT_X_H_M)
		
		# Read the accelerometer
		list = self.accel.readList(self.LSM303_REGISTER_ACCEL_OUT_X_L_A | 0x80, 6)
		accel = [self.accel12(list, 0) - self.ax_mean,
				 self.accel12(list, 2) - self.ay_mean,
				 self.accel12(list, 4) - self.az_mean ]
		
		# Read the magnetometer
		list = self.mag.readList(self.LSM303_REGISTER_MAG_OUT_X_H_M, 6)
		mag = [ self.mag16(list, 0) - self.mx_mean,
				self.mag16(list, 2) - self.my_mean,
				self.mag16(list, 4) - self.mz_mean]
		
		return accel,mag


	def setMagGain(gain=LSM303_MAGGAIN_1_3):
		self.mag.write8( LSM303_REGISTER_MAG_CRB_REG_M, gain)
	
	"""
	Determine if there is new data or not in the x,y,z registers
	in: None
	out: bool; true = yes new data, false = old data
	"""
	def dataReady(self):
		ans = self.accel.readU8(self.LSM303_STATUS_REG_A)
		ret = False
		unmasked = self.LSM303_STATUS_REG_ZYXDA_READY & ans
		if unmasked == self.LSM303_STATUS_REG_ZYXDA_READY: # new data available
			ret = True
		return ret
		
	"""
	Calibration routine. Estimates the mean bias error of each accel and saves them.
	in: how many samples do you want? default is 250
	out: None, prints results (mean,std) for each axis
	"""
	def calibrate(self,how_many=250):
		print '************************************'
		print '* Calibrating, do not move ...'
		print '************************************'
		
		# accels
		axbuff = []
		aybuff = []
		azbuff = []
		
		# mags
		mxbuff = []
		mybuff = []
		mzbuff = []
		
		for i in range(how_many):
			while not self.dataReady(): # this only looks at accels
				time.sleep(0.001)			
			a,m = self.read()
			
			axbuff.append(a[0])
			aybuff.append(a[1])
			azbuff.append(a[2])
			
			mxbuff.append(m[0])
			mybuff.append(m[1])
			mzbuff.append(m[2])
				
		amean = [ np.mean(axbuff), np.mean(aybuff), np.mean(azbuff) ]
		mmean = [ np.mean(mxbuff), np.mean(mybuff), np.mean(mzbuff) ]
		astd = [ np.std(axbuff), np.std(aybuff), np.std(azbuff) ]
		mstd = [ np.std(mxbuff), np.std(mybuff), np.std(mzbuff) ]
		
		self.ax_mean = amean[0]
		self.ay_mean = amean[1]
		self.az_mean = amean[2]
		
		self.mx_mean = mmean[0]
		self.my_mean = mmean[1]
		self.mz_mean = mmean[2]
		
		name = ['x','y','z']
		
		print 'Accel Calibration results:'
		for i in range(3):
			print '{} mean: {:.2f}	+/- {:.2f} g'.format(name[i],amean[i],astd[i])
		
		print 'Magnetic Calibration results:'
		for i in range(3):
			print '{} mean: {:.2f}	+/- {:.2f} m'.format(name[i],mmean[i],mstd[i])



# Simple example prints accel/mag data once per second:
if __name__ == '__main__':

	from time import sleep

	lsm = Adafruit_LSM303()

	print '[(Accelerometer X, Y, Z), (Magnetometer X, Y, Z, orientation)]'
	while True:
		print lsm.read()
		sleep(1) # Output is fun to watch if this is commented out
