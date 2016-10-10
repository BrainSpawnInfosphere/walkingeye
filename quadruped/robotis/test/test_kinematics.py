import numpy as np
from ..kinematics import T, rot
from math import pi
from math import radians as d2r


def test_t():
	R = rot(0.0, 0.0, 0.0, 0.0)  # should be eye(4,4)
	a = np.array([1., 2., 3., 1.])
	b = np.dot(R, a)
	# print(R)
	# print(a,b)
	assert(np.linalg.norm(a-b) == 0.0)


def test_t_r():
	# works for Crane's Book, p 41
	ans = np.array([24.11197183, 20.11256511, 18.16670832, 1.])
	params = [
		# a_ij alpha_ij  S_j  theta_j
		[0,    d2r(90),  5.9, 5*pi/6],  # frame 12
		[17,    d2r(0),    0,  -pi/3],  # 23
		[0.8, d2r(270),   17,   pi/4],  # 34
		[0,    d2r(90),    0,   pi/3],  # 45
		[0,    d2r(90),    4,  -pi/6]   # 56
	]

	r = T(params, 5*pi/4)
	# print(r)
	pos = r.dot(np.array([5, 3, 7, 1]))
	res = np.linalg.norm(ans - pos)
	# print('res:', res)
	assert(res < 0.000001)
