#!/usr/bin/env python

import time
import json

# use dict as base class ... value?
#import UserDict
#
#class FancyDict(UserDict.UserDict):
#    def __init__(self, data = {}, **kw):
#        UserDict.UserDict.__init__(self)
#        self.update(data)
#        self.update(kw)
#
#>>> a=FancyDict(a=1.0,b=2.2,c=3.3)
#>>> a
#{'a': 1.0, 'c': 3.3, 'b': 2.2}

# w = Wrench()
# json.dumps(w, default=lambda o: vars(o))
# turn every class member to a json string

def serialize(c):
    return json.dumps(c, default=lambda o: vars(o))

class Header(object):
    def __init__(self):
        self.stamp = time.time()

class Point(object):
    def __init__(self,x=0.0,y=0.0,z=0.0):
        self.x = x
        self.y = y
        self.z = z


class Vector(object):
    def __init__(self,x=0.0,y=0.0,z=0.0):
        self.x = x
        self.y = y
        self.z = z


class Quaternion(object):
    __slots__ = ['x','y','z','w'] # reduce memory footprint
    def __init__(self,x=0.0,y=0.0,z=0.0,w=1.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    def __repr__(self):
        """
        Python displays class
        """
        return 'Quaternion[%.4f,%.4f,%.4f,%.4f]'%(self.x,self.y,self.z,self.w)
    def __str__(self):
        """
        Print
        """
        return '[%.4f,%.4f,%.4f,%.4f]'%(self.x,self.y,self.z,self.w)

class Twist(object):
    def __init__(self):
        self.linear = Vector()
        self.angular = Vector()


class Wrench(object):
    def __init__(self):
        self.force = Vector()
        self.torque = Vector()
    def __repr__(self):
        return 'repr string'
  
class Pose(object):
    def __init__(self):
        self.position = Point()
        self.orientation = Quaternion()

class PoseStamped(object):
    def __init__(self):
        self.stamp = Header()
        self.position = Point()
        self.orientation = Quaternion()
    def __repr__(self):
        return 'repr string'
    def __str__(self):
        return 'str string'


