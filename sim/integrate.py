#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#

import numpy as np
import matplotlib.pyplot as plt
from math import *


def derivs(x,time):
	y = sin( 2.0*pi*time )
	print y,time
	return y


def rk4(y,time,dt,dervis):
	k1 = dt*dervis(y,time)
	k2 = dt*dervis(y+0.5*k1,time+0.5*dt)
	k3 = dt*dervis(y+0.5*k2,time+0.5*dt)
	k4 = dt*dervis(y+k3,time+dt)
	y_next = y+1.0/6.0*(k1+2.0*k2+2.0*k3+k4)
	
	return y_next

def rk2(y,time,dt,dervis):
	k0 = dt*dervis(y,time)
	k1 = dt*dervis(y+k0,time+dt)
	y_next = y+0.5*(k0+k1)
	
	return y_next

"""
main funtion
"""
def main():
	time = np.linspace(0,1,100)
	y = np.zeros(100)
	y[0] = 0.0
	for j in range(0,99):
		y[j+1] = rk4(y[j],time[j],time[1],derivs)
	
	plt.plot(time,y,'b')
	plt.show()
	
	


if __name__ == '__main__':
	main()