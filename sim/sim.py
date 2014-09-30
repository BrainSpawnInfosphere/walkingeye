#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#

import numpy as np
import matplotlib.pyplot as plt
from math import *


def robot(y,u,t):
	m = 5.0
	j = 4.0
	p = 45.0*pi/180.0
	l = 0.05
	
	phi = np.array([[sin(p),0,0],[0,cos(p),0],[0,0,l]])
	one = np.array([[1,-1,-1,1],[1,1,-1,-1],[1,1,1,1]])
	#q=phi*one,u))
	
	Fx = 1 #q[0]
	Fy = 0 #q[1]
	T = 0 #q[2]
	
	xd = y[0]
	yd = y[1]
	pd = y[2]
	
	xdd=Fx/m+2*pd*yd
	ydd=Fy/m-2*pd*xd
	pdd=T/j
	
	

def rk4u(y,u,time,dt,F):
	k1 = dt*F(y,u,time)
	k2 = dt*F(y+0.5*k1,u,time+0.5*dt)
	k3 = dt*F(y+0.5*k2,u,time+0.5*dt)
	k4 = dt*F(y+k3,u,time+dt)
	y_next = y+1.0/6.0*(k1+2.0*k2+2.0*k3+k4)
	return y_next

"""
main funtion
"""
def main():
	N = 100
	time = np.linspace(0,10,N)
	y = np.zeros(N)
	y[0] = -1.0/(2.0*pi)
	
	for j in range(0,N-1):
		y[j+1] = rk4u(y[j],0,time[j],time[1],robot)
	
	plt.plot(time,y,'b')
	plt.show()
	
	


if __name__ == '__main__':
	main()