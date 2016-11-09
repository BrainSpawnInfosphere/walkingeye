#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import numpy as np
from sympy import symbols, sin, cos, pi, simplify, trigsimp
# from sympy import rad as d2r


a, b, g = symbols('a b g')
Lc, Lf, Lt = symbols('Lc Lf Lt')


def eval(f, inputs):
	"""
	Do substitution of angles/lengths
	"""
	h = []
	for i in range(0, 3):
		tmp = (f[i,3]).subs(inputs)
		h.append(tmp.evalf())
	return h

def simp(f):
	"""
	Simplify down equations
	"""
	h = []
	for i in range(0, 3):
		h.append(simplify(f[i,3]))
	return h

class DH(object):
	def __init__(self):
		pass

	def fk(self, params):
		t = np.eye(4)
		for p in params:
			t = t.dot(self.makeT(*p))
		return t

	def makeT(self, a, alpha, d, theta):
		# alpha = d2r(alpha)
		# theta = d2r(theta)
		return np.array([  # classic DH
			[cos(theta), -sin(theta) * cos(alpha),  sin(theta) * sin(alpha), cos(theta) * a],
			[sin(theta),  cos(theta) * cos(alpha), -cos(theta) * sin(alpha), sin(theta) * a],
			[         0,               sin(alpha),               cos(alpha),              d],
			[         0,                        0,                        0,              1]
		])


def test_DH():
	# a, alpha, d, theta
	params = [
		[Lc, pi/2, 0, a],
		[Lf,    0, 0, b],
		[Lt,    0, 0, g]
	]
	dh = DH()
	t = dh.fk(params)
	# t = eval(t,[])
	t = simp(t)
	print('{}\n\n {}\n\n {}\n'.format(t[0],t[1],t[2]))

test_DH()
