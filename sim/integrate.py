#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#

import numpy as np
import matplotlib.pyplot as plt
from math import *

"""
integral of sin(2*pi*t) = -cos( 2*pi*t)/(2*pi)
"""
def derivs(x,time):
	y = sin( 2.0*pi*time )
	return y


def rk4(y,time,dt,F):
	k1 = dt*F(y,time)
	k2 = dt*F(y+0.5*k1,time+0.5*dt)
	k3 = dt*F(y+0.5*k2,time+0.5*dt)
	k4 = dt*F(y+k3,time+dt)
	y_next = y+1.0/6.0*(k1+2.0*k2+2.0*k3+k4)
	return y_next

def rk2(y,time,dt,F):
	k0 = dt*F(y,time)
	k1 = dt*F(y+k0,time+dt)
	y_next = y+0.5*(k0+k1)
	return y_next

"""
main funtion
"""
def main():
	time = np.linspace(0,4,400)
	y = np.zeros(400)
	y2 = np.zeros(400)
	y[0] = -1.0/(2.0*pi)
	y2[0] = -1.0/(2.0*pi)
	for j in range(0,399):
		y[j+1] = rk4(y[j],time[j],time[1],derivs)
		y2[j+1] = -cos( 2.0*pi*time[j])/(2.0*pi)
	
	plt.plot(time,y,'b',time,y2,'r')
	plt.show()
	
	


if __name__ == '__main__':
	main()