#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#

import numpy as np
import matplotlib.pyplot as plt
from math import *

"""
Creates a polar plot
"""
def polar(a,r,c,l):
	ax = plt.subplot(111,polar=True)
	ax.plot(a,r,c,label=l)
	ax.set_rmax(4.5)
	#ax.grid(True)
	return ax



"""
motors(phi, angles)
phi = motor angle in degrees
angles = 0 ... 2pi
"""
def motors(phi,a):
	em = np.empty( len(a) )
	phi = phi*pi/180.0;
	t =  np.array([[sin(phi),  cos(phi), 1],
		           [-sin(phi), cos(phi), 1],
	               [-sin(phi), -cos(phi), 1],
	               [sin(phi),  -cos(phi), 1]])
	
	i = 0    
	for angle in a:
		x = np.array([[cos(angle),sin(angle),0]]).T
		v = np.dot(t,x)
		em[i] = np.sum(np.abs(v));
		i += 1
	
	return em

"""
main funtion
"""
def main():
	size = 100
	angles = np.linspace(0,2.0*pi,size)

	em30 = motors(30,angles);
	em45 = motors(45,angles);
	em60 = motors(60,angles);
	
	p = polar(angles,em30,'r-','30');
	p = polar(angles,em45,'g--','45');
	p = polar(angles,em60,'b-.','60');

	p.grid(True)
	p.set_title('Number of Equivelent Motors');
	plt.legend()
	plt.show()

if __name__ == '__main__':
	main()