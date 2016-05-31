#!/usr/bin/env python

class Vector(dict):
	"""
	"""
	def __init__(self, **kw):
		__slots__ = ['x','y','z']
		dict.__init__(self)
		default = {'x': 0.0, 'y': 0.0, 'z': 0.0}
		self.update(default)
		if kw: self.update(kw)

	# def set(self, xx, yy, zz):
	# 	self.update(x=xx, y=yy, z=zz)

	def norm(self):
		m = self.values()
		return math.sqrt(m[0]**2 + m[1]**2 + m[2]**2)

class Twist(dict):
	"""
	"""
	__slots__ = ['linear','angular']
	def __init__(self):
		dict.__init__(self)
		self.update(linear=Vector())
		self.update(angular=Vector())

v = Twist()
# v.x = 5
v['zz'] = 25
v['linear']['x'] = 1

print v
