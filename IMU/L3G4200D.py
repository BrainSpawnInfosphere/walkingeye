#!/usr/bin/python
#
# Kevin J. Walchko
# 24 Sept 2014

from Adafruit_I2C import Adafruit_I2C
import numpy as np
import time


"""
A simple class that handles the L3G4200D 3-axis gyro.
"""
class L3G4200D(Adafruit_I2C):
	GYRO_ADDRESS                      = 0x69   # DEFAULT    TYPE
	GYRO_REGISTER_WHO_AM_I            = 0x0F   # 11010011   r
	GYRO_REGISTER_CTRL_REG1           = 0x20   # 00000111   rw
	GYRO_REGISTER_CTRL_REG2           = 0x21   # 00000000   rw
	GYRO_REGISTER_CTRL_REG3           = 0x22   # 00000000   rw
	GYRO_REGISTER_CTRL_REG4           = 0x23   # 00000000   rw
	GYRO_REGISTER_CTRL_REG5           = 0x24   # 00000000   rw
	GYRO_REGISTER_REFERENCE           = 0x25   # 00000000   rw
	GYRO_REGISTER_OUT_TEMP            = 0x26   #            r
	GYRO_REGISTER_STATUS_REG          = 0x27   #            r
	GYRO_REGISTER_OUT_X_L             = 0x28   #            r
	GYRO_REGISTER_OUT_X_H             = 0x29   #            r
	GYRO_REGISTER_OUT_Y_L             = 0x2A   #            r
	GYRO_REGISTER_OUT_Y_H             = 0x2B   #            r
	GYRO_REGISTER_OUT_Z_L             = 0x2C   #            r
	GYRO_REGISTER_OUT_Z_H             = 0x2D   #            r
	GYRO_REGISTER_FIFO_CTRL_REG       = 0x2E   # 00000000   rw
	GYRO_REGISTER_FIFO_SRC_REG        = 0x2F   #            r
	GYRO_REGISTER_INT1_CFG            = 0x30   # 00000000   rw
	GYRO_REGISTER_INT1_SRC            = 0x31   #            r
	GYRO_REGISTER_TSH_XH              = 0x32   # 00000000   rw
	GYRO_REGISTER_TSH_XL              = 0x33   # 00000000   rw
	GYRO_REGISTER_TSH_YH              = 0x34   # 00000000   rw
	GYRO_REGISTER_TSH_YL              = 0x35   # 00000000   rw
	GYRO_REGISTER_TSH_ZH              = 0x36   # 00000000   rw
	GYRO_REGISTER_TSH_ZL              = 0x37   # 00000000   rw
	GYRO_REGISTER_INT1_DURATION       = 0x38   # 00000000   rw
	
	GYRO_STATUS_REG_ZYXDA             = 0x08   # Z, Y, X data available
	
	"""
	Initialise the L3G4200D gyro, will print Gyro found or Error.
	in: bus number (default 1) and debug (default False)
	out: None
	"""
	def __init__(self, busnum=1, debug=False):
		self.gyro = Adafruit_I2C(self.GYRO_ADDRESS, busnum, debug)
		
		# Do I have the right address and gyro?
		ans = self.gyro.readU8(self.GYRO_REGISTER_WHO_AM_I)
		if ans == 0xD3:
			print '[+] Gyro found'
		else:
			print '[-] Error initializing Gyro'
			exit()
		
		# Reg1 [DR BW PD Z Y X]	
		# Set 100 Hz output: DR=00 BW=00, give a cut-off of 12.5 Hz BW
		# Set normal mode PD=1
		# Enable x = 1, y = 1, z = 1
		self.gyro.write8(self.GYRO_REGISTER_CTRL_REG1 , 0x0F)
		
		# Reg2 [0 0 HPM HPCF]
		# Set high pass filter HPM to 00 for normal mode
		# Set HPCF to 0000; cut-off freq to 8 Hz, given ODR is 100 Hz 
		self.gyro.write8(self.GYRO_REGISTER_CTRL_REG2 , 0x00)
		
		# Reg 3 is all interrupt stuff ... not using, set to 0
		self.gyro.write8(self.GYRO_REGISTER_CTRL_REG3 , 0x00)
		
		# Set degrees per sec using reg4
		# FS1 FS2  dps
		#   0   0  250 (default)
		#   0   1  500
		#   1   0 2000
		#   1   1 2000
		self.gyro.write8(self.GYRO_REGISTER_CTRL_REG4 , 0x00)
		
		# Reg5 [0 0 0 HP 0 0 Out_Sel] ignoring boot and interrupt stuff
		# Note: LPF1 -> HPF -> LPF2 -> Data Reg
		# see table 35 and fig 19 on pg 33 for combinations of filtering
		# HP = 1, on
		# Out_Sel = 
		self.gyro.write8(self.GYRO_REGISTER_CTRL_REG5 , 0x00)
		
		# if you change FS1 or FS2, you need to change this!
		self.gain = 0.00875 # converts int to dps; see table 4 spec sheet
		
		# init these to zero, then calibrate to figure out what they should be
		self.x_mean = 0.0
		self.y_mean = 0.0
		self.z_mean = 0.0
		
		self.calibrate()
		
	__del__(self):
		print 'Gyro: Good bye ...'

	"""
	Determine if there is new data or not in the x,y,z registers
	in: None
	out: bool; true = yes new data, false = old data
	"""
	def dataReady(self):
		ans = self.gyro.readU8(self.GYRO_REGISTER_STATUS_REG)
		#print 'ans',ans
		ret = False
		unmasked = self.GYRO_STATUS_REG_ZYXDA & ans
		if unmasked == self.GYRO_STATUS_REG_ZYXDA: # new data available
			ret = True
		return ret
	
	"""
	Calibration routine. Estimates the mean bias error of each gyro and saves them.
	in: how many samples do you want? default is 250
	out: None, prints results (mean,std) for each axis
	"""
	def calibrate(self, how_many=250):
		print '************************************'
		print '* Calibrating, do not move ...'
		print '************************************'
		xbuff = []
		ybuff = []
		zbuff = []
		for i in range(how_many):
			while not self.dataReady():
				time.sleep(0.001)			
			x,y,z = self.read()
			xbuff.append(x)
			ybuff.append(y)
			zbuff.append(z)
				
		#dmax = [ max(xbuff), max(ybuff), max(zbuff) ]
		#dmin = [ min(xbuff), min(ybuff), min(zbuff) ]
		dmean = [ np.mean(xbuff), np.mean(ybuff), np.mean(zbuff) ]
		dstd = [ np.std(xbuff), np.std(ybuff), np.std(zbuff) ]
		dname = ['x','y','z']
		
		self.x_mean = dmean[0]
		self.y_mean = dmean[1]
		self.z_mean = dmean[2]
		
		print 'Calibration results:'
		for i in range(3):
			print '{} mean: {:.2f}  +/- {:.2f} dps'.format(dname[i],dmean[i],dstd[i])
		

	"""
	Read the lower and upper bytes of the gyros.
	in: None
	out: signed float for x,y,z in dps
	"""
	def read(self):
		X_L = self.gyro.readU8(self.GYRO_REGISTER_OUT_X_L)
		X_H = self.gyro.readU8(self.GYRO_REGISTER_OUT_X_H)
		
		Y_L = self.gyro.readU8(self.GYRO_REGISTER_OUT_Y_L)
		Y_H = self.gyro.readU8(self.GYRO_REGISTER_OUT_Y_H)
		
		Z_L = self.gyro.readU8(self.GYRO_REGISTER_OUT_Z_L)
		Z_H = self.gyro.readU8(self.GYRO_REGISTER_OUT_Z_H)
		
		X = X_H << 8 | X_L
		Y = Y_H << 8 | Y_L
		Z = Z_H << 8 | Z_L
		
		X = self.getSignedNumber(X)
		Y = self.getSignedNumber(Y)
		Z = self.getSignedNumber(Z)
		
		x = self.gain * float(X) - self.x_mean
		y = self.gain * float(Y) - self.y_mean
		z = self.gain * float(Z) - self.z_mean
		
		return x,y,z
	
	"""
	Grab the contents of a single register
	"""
	def getRegister(self,reg):
		return self.gyro.readU8(reg)
	
	"""
	Grab the contents of all 5 registers and print them to the screen
	todo: make a little more useful
	"""
	def dumpRegisters(self):
		print '[*] GYRO_REGISTER_CTRL_REG1', self.getRegister(self.GYRO_REGISTER_CTRL_REG1)
		print '[*] GYRO_REGISTER_CTRL_REG2', self.getRegister(self.GYRO_REGISTER_CTRL_REG2)
		print '[*] GYRO_REGISTER_CTRL_REG3', self.getRegister(self.GYRO_REGISTER_CTRL_REG3)
		print '[*] GYRO_REGISTER_CTRL_REG4', self.getRegister(self.GYRO_REGISTER_CTRL_REG4)
		print '[*] GYRO_REGISTER_CTRL_REG5', self.getRegister(self.GYRO_REGISTER_CTRL_REG5)
		
	
	"""
	Temp updates at 1 Hz and operates between -40C to +85C
	in: None
	out: 8b int temperature in degrees C
	"""
	def getTemperature(self):
		temp = self.gyro.readU8(self.GYRO_REGISTER_OUT_TEMP)
		return temp
		
	"""
	Converts 16 bit two's compliment reading to signed int
	in: two's complement
	out: signed int
	"""
	def getSignedNumber(self,number):
		if number & (1 << 15):
			return number | ~65535
		else:
			return number & 65535


if __name__ == '__main__':
	from time import sleep
	#import string
	
	gyro = L3G4200D()
	gyro.dumpRegisters()
	#gyro.calibrate()
	
	while True:
		X,Y,Z = gyro.read()
		T = gyro.getTemperature()
		
		print 'x: {:5.2f} dps  y: {:5.2f} dps  z: {:5.2f} dps  Temp: {:3d} C'.format(X,Y,Z,T)
		
		sleep(0.2)