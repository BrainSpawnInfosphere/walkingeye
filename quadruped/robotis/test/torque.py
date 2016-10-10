#!/usr/bin/env python
# from __future__ import print_function
# from __future__ import division
# # import numpy as np
# from math import cos, sin, sqrt
# from math import radians as d2r
#
#
# def footPos(b, g):
# 	"""
# 	a - shoulder angle is always 0
# 	b - femur angle (-90, 90)
# 	g - tibia angle (-180, 0)
# 	    +
# 	   /|
# 	  / | A
# 	 /  |
# 	+---+
# 	  B
# 	"""
# 	Lc = 0.026  # mm
# 	Lf = 0.042
# 	Lt = 0.063
#
# 	b = d2r(b)
# 	g = d2r(g)  # i don't use this right now
#
# 	A = Lf*sin(b)
# 	B = Lf*cos(b)
#
# 	pos = [
# 		Lc + B,
# 		0.0,
# 		-Lt + A
# 	]
# 	return pos
#
#
# def calcTorque(foot):
# 	"""
# 	s     s
# 	+-----+--------+ CM
# 	|              |
# 	|              v
# 	|
# 	    torque balance:  s + s = r W/3
# 	the servos are at location s, the center mass is at CM, the weight is W
# 	and r is the distance from the foot to CM. The shoulder servo works perpendicular
# 	to this plane and doesn't help to lift.
# 	"""
# 	Lc = 0.026  # mm
# 	Lf = 0.042
# 	Lt = 0.063
#
# 	# servo = 0.15  # TG9e servo torque in Nm
# 	servo = 0.39  # XL-320 servo torque in Nm
#
# 	x = foot[0]
# 	# r = dist_from_CM + foot_pos[x]
# 	r = .144/2 + x
#
# 	# 2*servo = r F
# 	F = 2.0*servo/r
# 	return 3.0*F
#
# foot = footPos(45, -135)
# print('Foot location [{:.3f} {:.3f} {:.3f}]'.format(*foot))
# N = calcTorque(foot)
# print('This can lift {:.3f} N'.format(N))
#
# # why the fuck do people confuse mass and weight!!! weight is N and mass is kg
# # the the stupid scale I used was in grams for weight ... idiots!!!
# print('This can lift {:.3f} g force'.format(1000*N/9.81))  # convert N to grams force
# print('The robot is: {} g force'.format(560))
