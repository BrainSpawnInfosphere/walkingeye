#!/usr/bin/python
#
# Kevin J. Walchko
# 24 Sept 2014

from L3G4200D import L3G4200D
from Adafruit_LSM303 import Adafruit_LSM303 as LSM303
import numpy as np
import time
import ahrs

"""
The IMU is composed of several sensors for measuring: 
	- linear acceleration 
	- magnetic field 
	- angular velocity 
	- temperature
There is a built in AHRS algorithm which can be used to estimate the orientation.
"""
class minIMU9:
	"""
	Initialize the IMU
	todo: better way to pick beta ... seems random
	"""
	def __init__(self):
		self.gyro = L3G4200D()
		self.accel_mag = LSM303()
		beta = sqrt(3.0/4.0)*M_PI/180.0*5.0 # 5 deg of measurement error
		self.q = [0,0,0,1]
		self.ahrs = AHRS(1.0)
	
	def __del__(self):
		print 'IMU shutting down, bye ...'
	
	"""	
	from "tilt compensated compass.pdf" (LSM303DLH tech note)
    calculate heading from magnetometers and return heading in degrees.
    in: magnetic and quaternion
    out: compass heading in degrees
    """
    def heading(self,m,q):
		mx,my,mz = m # magnetic
		q0,q1,q2,q3 = q
    	
    	heading = 0.0
    	M_PI = pi
    	
    	# eqn 10 ... sort of
    	r = atan2(2.0*q2*q3-2.0*q0*q1,2.0*q0*q0+2.0*q3*q3-1.0) # roll
    	g = -asin(2.0*q1*q3+2.0*q0*q2) # pitch
    	
    	
    	invnorm = 1.0/np.linalg.norm(m)
    	mx1 = mx*invnorm
    	my1 = my*invnorm
    	mz1 = mz*invnorm
    	
    	# eqn 12
    	mx2 = mx1*cos(r)+mz1*sin(r)
    	my2 = mx1*sin(g)*sin(r)+my1*cos(g)-mz1*sin(g)*sin(r)
    	#mz2 = -mx1*cos(g)*sin(r)+my1*sin(g)+mz1*cos(g)*cos(r)
    	
    	heading = atan2(my2,mx2) # double check this
    	
    	# eqn 13
    	if mx2 > 0.0 && my2 >= 0.0: 
    		pass # all good 
    	elif mx2 < 0.0: 
    		heading = M_PI+heading
    	elif mx2>0.0 && my2 <=0.0: 
    		heading = 2.0*M_PI+heading
    	elif mx2 == 0.0 && my2 < 0.0: 
    		heading = M_PI/2.0 # 90 deg
    	elif mx2 == 0.0 && my2 > 0.0:
    		heading = 1.5*M_PI # 270 deg
    	
    	#print "heading: {:.2f}".format(heading)
    	
    	# return roll, pitch, heading
    	return [180.0/M_PI*r, 180.0/M_PI*g, 180.0/M_PI*heading]
    
	
	"""
	Reads sensors
	in: None
	out: accel (m/s2), angular vel (dps), quaterion
	"""
	def read(self,dt):
		wx,wy,wz = self.gyro.read()
		w = [wx,wy,wz]
		temp = self.gyro.getTemperature() # what can I do with this?
		a,m = self.accel_mag.read()
		q = self.q
		self.q = self.ahrs.update(a,m,w,q,dt)
		
		return a,w,q
		

if __name__ == '__main__':
	from time import sleep
	
	imu = minIMU9()
	
	while True:
		print imu.read()
		sleep(1)