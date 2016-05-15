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
    """
    This is primarily used in path planning. The planner returns a position/orientation at a given time.
    """
    def __init__(self):
        dict.__init__(self)
        self.update(stamp = time.time())
        self.update(position = Vector())
        self.update(orientation = Quaternion())


class Range(dict):
    """
    Holds the ranges of the Sharp IR sensors. Note, currently, these are just digital and only return True (1) or False (0) and have a real distance of around 7 inches. This is because the analog signal is tied to a digital pin.
    """
    def __init__(self):
        dict.__init__(self)
        self.update(stamp = time.time())
        self.update(fov = 20.0) # need to fix this
        self.update(limits = (0.01,0.08))
        self.update(range = [0,0,0,0,0,0,0,0]) # this is for all 8 IR's 


class IMU(dict):
    def __init__(self, ranges):
        dict.__init__(self)
        self.update(stamp = time.time())
        self.update(linear_acceleration = Vector())
        self.update(angular_velocity = Vector())
        self.update(orientation = Quaternion())

class Odom(dict):
    def __init__(self):
        dict.__init__(self)
        self.update(stamp = time.time())
        self.update(position = Pose())
        self.update(velocity = Twist())

class Path(dict):
    """
    The returned path from a path planner which is an array of position/orientation at various times. These poses take the robot from the start to the stop position of the getPlan message.
    """
    def __init__(self):
        dict.__init__(self)
        self.update(stamp = time.time())
        self.update(poses = [])

class GetPlan(dict):
    """
    Define the start and stop position/orientation/time for a path planner 
    """
    def __init__(self):
        dict.__init__(self)
        self.update(start = PoseStamped())
        self.update(stop = PoseStamped())

class Text(dict):
    """
    Simple text message
    """
    def __init__(self):
        dict.__init__(self)
        self.update(stamp = time.time())
        self.update(message = '')


#########################################################################################################

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
