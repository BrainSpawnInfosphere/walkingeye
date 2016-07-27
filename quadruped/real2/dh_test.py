#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
import numpy as np
# from math import sin, cos, acos, atan2, sqrt, pi
from math import radians as d2r
# from math import degrees as r2d
# from tranforms import T, rot
from sympy import symbols, sin, cos, pi


a, b, g = symbols('a b g')
Lc, Lf, Lt = symbols('Lc Lf Lt')

a1, a2, t1, t2 = symbols('a1 a2 t1 t2')

def rot(a, alpha, S, theta):
	"""
	Creates a DH rotation matrix for forward kinematics.
	"""
	# return np.array([  # eqn 3.7 pg 36
	# 	[cos(theta), -sin(theta), 0.0, a],
	# 	[sin(theta) * cos(alpha), cos(theta) * cos(alpha), -sin(alpha), -sin(alpha) * S],
	# 	[sin(theta) * sin(alpha), cos(theta) * sin(alpha), cos(alpha), cos(alpha) * S],
	# 	[0.0, 0.0, 0.0, 1.0]
	# ])

	return np.array([  # inverse of above ?? spong text
		[cos(theta), -sin(theta) * cos(alpha), sin(theta) * sin(alpha), cos(theta) * a],
		[sin(theta), cos(theta) * cos(alpha), -cos(theta) * sin(alpha), sin(theta) * a],
		[0, sin(alpha), cos(alpha), S],
		[0, 0, 0, 1]
	])


def T(params, phi):
	"""
	Creates a transform from the leg frame to the foot.

	params = [[a, alpha, S, theta],[a, alpha, S, theta],...]
	"""
	# handle the base frame, eqn 3.9, p36
	t = np.array([
		[cos(phi), -sin(phi), 0.0, 0.0],
		[sin(phi), cos(phi), 0.0, 0.0],
		[0.0, 0.0, 1.0, 0.0],
		[0.0, 0.0, 0.0, 1.0]
	])
	for i, p in enumerate(params):
		t = t.dot(rot(*p))
	return t

def T2(params):
	"""
	Creates a transform from the leg frame to the foot.

	params = [[a, alpha, S, theta],[a, alpha, S, theta],...]
	"""
	# handle the base frame, eqn 3.9, p36
	t = np.array([
		[1.0, 0.0, 0.0, 0.0],
		[0.0, 1.0, 0.0, 0.0],
		[0.0, 0.0, 1.0, 0.0],
		[0.0, 0.0, 0.0, 1.0]
	])
	for i, p in enumerate(params):
		t = t.dot(rot(*p))
	return t

def fk(a, b, g):
	params = [
		# a_ij alpha_ij  S_j  theta_j
		[Lc,   pi/2,   0.0,   b],  # frame 12
		[Lf,    0.0,   0.0,   g]   # 23
	]

	r = T(params, a)
	foot = r.dot(np.array([Lt, 0.0, 0.0, 1.0]))

	return foot


def eval(f, inputs):
	h = []
	for i in range(0, 3):
		tmp = (f[i]).subs(inputs)
		h.append(tmp.evalf())
	return h


# kine = fk(a, b, g)
# print('Forward Kinematics')
# print(kine)
# print('----------------------------')
# # inputs = {a: -pi/4, b: 0.0, g: -pi/2, Lc: 26, Lf: 42, Lt: 63}
# inputs = {a: d2r(0.0), b: 0.0, g: d2r(-90.0), Lc: 26, Lf: 42, Lt: 63}
# print('for:', inputs)
# print(eval(kine, inputs))

params = [
	# a_ij alpha_ij  S_j  theta_j
	[a1,    0.0,   0.0,   t1],  # frame 12
	[a2,    0.0,   0.0,   t2]   # 23
]


print(rot(*params[0]))
print(rot(*params[1]))
r = T2(params)
print('Forward Kinematics')
print(r)
print('----------------------------')
# inputs = {a: -pi/4, b: 0.0, g: -pi/2, Lc: 26, Lf: 42, Lt: 63}
# inputs = {a: d2r(0.0), b: 0.0, g: d2r(-90.0), Lc: 26, Lf: 42, Lt: 63}
# print('for:', inputs)
# print(eval(kine, inputs))
