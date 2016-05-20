#!/usr/bin/env python

# algorithm based on sheep.art.pl

import Math

"""
a = alpha - hip
b = beta - knee
g = gamma - tibia

Lc - coxa
Lf - femur
Lt - tibia
"""


class Quadraped(object):
	"""
	Implements a quadraped
	"""
	def __init__(self, params):
		self.Lc = params['coxa']
		self.Lf = params['femur']
		self.Lt = params['tibia']
		self.cm = params['cm']  # center mass

	def inverseKinematics(self, point):
		x = point['x']
		y = point['y']
		z = point['z']

		a = Math.atan2(x, y)
		f = Math.sqrt(x**2+y**2) - self.Lc
		b1 = Math.atan2(z, f)
		d = Math.sqrt(f**2+x**2)
		b2 = Math.acos((self.Lf**2+d**2-self.Lt**2)/(2*self.Lf*d))
		b = b1+b2
		g = Math.acos((self.Lf**2+self.Lt**2-d**2)/(2*self.Lf*self.Lt))

		return {'a': a, 'b': b, 'g': g}

	def areaOfSupprt(self, l1, l2, l3):
		a = 1
		return False  # FIXME: 20160520
