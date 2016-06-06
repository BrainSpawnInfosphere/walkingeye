#!/usr/bin/env python

import time
import json
import math


def serialize(c):
	"""
	Takes a dictionary and turns it into a json string.
	"""
	return json.dumps(c, default=lambda o: vars(o))


def deserialize(s):
	"""
	Takes a json string and turns it into a dictionary.
	"""
	return json.loads(s)


class Vector(dict):
	"""
	Handles vectors

	Shortcut to set:
	v = Vector(x=1, y=33, z=55)
	v.update(y=44, z=22)
	"""
	def __init__(self, **kw):
		dict.__init__(self)
		default = {'x': 0.0, 'y': 0.0, 'z': 0.0}
		self.update(default)
		if kw: self.update(kw)

	def __str__(self):  # pretty up the print statement
		return 'Vector[x,y,z]: {:.4f} {:.4f} {:.4f}'.format(self.get('x'), self.get('y'), self.get('z'))

	# def set(self, xx, yy, zz):
	# 	self.update(x=xx, y=yy, z=zz)

	def norm(self):
		m = self.values()
		return math.sqrt(m[0]**2 + m[1]**2 + m[2]**2)


class Quaternion(dict):
	def __init__(self, **kw):
		dict.__init__(self)
		default = {'x': 0.0, 'y': 0.0, 'z': 0.0, 'w': 1.0}
		self.update(default)
		if kw:
			self.update(kw)
			m = self.values()
			d = math.sqrt(m[0]**2 + m[1]**2 + m[2]**2 + m[3]**2)
			# print d
			if d > 0.0:
				for k, v in self.items():
					# print k,v
					self.update({k: v / d})

	# def set(self, xx, yy, zz, ww):
	# 	self.update(x=xx, y=yy, z=zz, w=ww)

	def __str__(self):  # pretty up the print statement
		return 'Quaternion[x,y,z,w]: {:.4f} {:.4f} {:.4f} {:.4f}'.format(self.get('x'), self.get('y'), self.get('z'), self.get('w'))
# q=Quaternion(x=1,y=3,w=4); print q


class Twist(dict):
	"""
	Twist is a combined linear and angular motion

	t = Twist()
	t['linear'].update(x=22, z=33)
	"""
	def __init__(self):
		dict.__init__(self)
		self.update(linear=Vector())
		self.update(angular=Vector())

	def __str__(self):  # pretty up the print statement
		return 'Twist:\n\tLinear {}\n\tAngular {}'.format(self.get('linear'), self.get('angular'))


class Wrench(dict):
	def __init__(self):
		dict.__init__(self)
		self.update(force=Vector())
		self.update(torque=Vector())


class Pose(dict):
	def __init__(self):
		dict.__init__(self)
		self.update(position=Vector())
		self.update(orientation=Quaternion())


class PoseStamped(dict):
	"""
	This is primarily used in path planning. The planner returns a position/orientation at a given time.
	"""
	def __init__(self):
		dict.__init__(self)
		self.update(stamp=time.time())
		self.update(position=Vector())
		self.update(orientation=Quaternion())


class Range(dict):
	"""
	Holds the ranges of the Sharp IR sensors. Note, currently, these are just digital and only return True (1) or False (0) and have a real distance of around 7 inches. This is because the analog signal is tied to a digital pin.
	"""
	def __init__(self):
		dict.__init__(self)
		self.update(stamp=time.time())
		self.update(fov=20.0)  # need to fix this
		self.update(limits=(0.01, 0.08))
		self.update(range=[0, 0, 0, 0, 0, 0, 0, 0])  # this is for all 8 IR's


class IMU(dict):
	def __init__(self):
		dict.__init__(self)
		self.update(stamp=time.time())
		self.update(linear_acceleration=Vector())
		self.update(angular_velocity=Vector())
		self.update(orientation=Quaternion())
		self.update(heading=0.0)  # degrees
		self.update(temperature=0.0)  # degrees C

	def __str__(self):
		return 'IMU:\n\tLinear Accel {}\n\tAngular Vel {}\n\tOrientation {}\n\tHeading [deg]: {}\n\tTemp [C]: {}'.format(
			self.get('linear_acceleration'), self.get('angular_velocity'),
			self.get('orientation'), self.get('heading'), self.get('temperature')
		)


class Odom(dict):
	def __init__(self):
		dict.__init__(self)
		self.update(stamp=time.time())
		self.update(position=Pose())
		self.update(velocity=Twist())


class Path(dict):
	"""
	The returned path from a path planner which is an array of position/orientation at various times. These poses take the robot from the start to the stop position of the getPlan message.
	"""
	def __init__(self):
		dict.__init__(self)
		self.update(stamp=time.time())
		self.update(poses=[])


class GetPlan(dict):
	"""
	Define the start and stop position/orientation/time for a path planner
	"""
	def __init__(self):
		dict.__init__(self)
		self.update(start=PoseStamped())
		self.update(stop=PoseStamped())


class Text(dict):
	"""
	Simple text message
	"""
	def __init__(self):
		dict.__init__(self)
		self.update(stamp=time.time())
		self.update(message='')


if __name__ == '__main__':
	# print 'run "nosetests -v ./Messages.py" to test'
	v = Vector(x=1.23, y=-1.23, z=32.1)
	# v.set()
	print v

	t = Twist()
	print t

	i = IMU()
	print i
