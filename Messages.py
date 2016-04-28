#!/usr/bin/env python

import time
import json
import math

def serialize(c):
    return json.dumps(c, default=lambda o: vars(o))

def deserialize(s):
    return json.loads(s)

# class Header(dict):
#     def __init__(self):
#         dict.__init__(self)
#         self.update(stamp = time.time())

# class Point(dict):
#     def __init__(self,**kw):
#         dict.__init__(self)
#         default = {'x':0.0, 'y':0.0, 'z':0.0}
#         self.update(default)
#         if kw: self.update(kw)

class Vector(dict):
    def __init__(self,**kw):
        dict.__init__(self)
        default = {'x':0.0, 'y':0.0, 'z':0.0}
        self.update(default)
        if kw: self.update(kw)

    def norm(self):
        m = self.values()
        return math.sqrt(m[0]**2 + m[1]**2 + m[2]**2)


class Quaternion(dict):
    def __init__(self,**kw):
        dict.__init__(self)
        default = {'x':0.0, 'y':0.0, 'z':0.0, 'w':1.0}
        self.update(default)
        if kw:
            self.update(kw)
            m = self.values()
            d = math.sqrt(m[0]**2 + m[1]**2 + m[2]**2 + m[3]**2)
            # print d
            if d > 0.0:
                for k, v in self.items():
                    # print k,v
                    self.update({k : v/d})

# q=Quaternion(x=1,y=3,w=4); print q

class Twist(dict):
    def __init__(self):
        dict.__init__(self)
        self.update(linear=Vector())
        self.update(angular=Vector())

class Wrench(dict):
    def __init__(self):
        dict.__init__(self)
        self.update(force = Vector())
        self.update(torque = Vector())

class Pose(dict):
    def __init__(self):
        dict.__init__(self)
        self.update(position = Vector())
        self.update(orientation = Quaternion())

class PoseStamped(dict):
    def __init__(self):
        dict.__init__(self)
        self.update(stamp = time.time())
        self.update(position = Vector())
        self.update(orientation = Quaternion())

# def test_point():
#     p = Point(x=1.23,y=-1.23,z=32.1)
#     assert p == {'y': -1.23, 'x': 1.23, 'z': 32.1}

def test_vector():
    v = Vector(x=1.23,y=-1.23,z=32.1)
    assert v == {'y': -1.23, 'x': 1.23, 'z': 32.1}

def test_quaternion():
    q = Quaternion(x=0.5,y=0.5,z=0.5,w=0.5)
    assert q == {'w': 0.5, 'y': 0.5, 'x': 0.5, 'z': 0.5}

def test_twist():
    t = Twist()
    t['linear']['x'] = 55.0
    t['angular']['y'] = -56.7
    assert t == {'linear': {'y': 0.0, 'x': 55.0, 'z': 0.0}, 'angular': {'y': -56.7, 'x': 0.0, 'z': 0.0}}

def test_pose():
    p = Pose()
    assert p == {'position': {'y': 0.0, 'x': 0.0, 'z': 0.0}, 'orientation': {'y': 0.0, 'x': 0.0, 'z': 0.0, 'w': 1.0}}

def test_posestamped():
    ps = PoseStamped()
    ps['stamp'] = 1234567.89
    assert ps == {'stamp': 1234567.89, 'orientation': {'y': 0.0, 'x': 0.0, 'z': 0.0, 'w': 1.0}, 'position': {'y': 0.0, 'x': 0.0, 'z': 0.0}}

def test_wrench():
    w = Wrench()
    assert w == {'torque': {'y': 0.0, 'x': 0.0, 'z': 0.0}, 'force': {'y': 0.0, 'x': 0.0, 'z': 0.0}}

def test_serialize():
    ps = PoseStamped()
    ps['stamp'] = 1234567.89
    assert deserialize(serialize(ps)) == ps


if __name__ == '__main__':
    print 'run "nosetests -v ./Messages.py" to test'
