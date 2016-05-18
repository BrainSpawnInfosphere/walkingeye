#!/usr/bin/env python

# algorithm based on sheep.art.pl

"""
a = alpha - hip
b = beta - knee
g = gamma - tibia
"""

class Quadraped(object):
	def __init__(self,params):
		Lc = params['coxa']
		Lf = params['femur']
		Lt = params['tibia']


	def inverseKinematics(self, point):
		x = point['x']
		y = point['y']
		z = point['z']

		a = Math.atan2(x,y)
		f = Math.sqrt(x**2+y**2)
		b1 = Math.atan2(z,f)
		d = Math.sqrt(f**2+x**2)
		b2 = Math.acos((Lf**2+d**2-Lt**2)/(2*Lf*d))
		b = b1+b2
		g = Math.acos((Lf**2+Lt**2-d**2))
