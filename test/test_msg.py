#!/usr/bin/env python


import os
import sys
# import multiprocessing as mp
sys.path.insert(0, os.path.abspath('..'))

# import lib.zmqclass as zmq
import lib.Messages as msg


def test_vector():
    v = msg.Vector(x=1.23, y=-1.23, z=32.1)
    assert v == {'y': -1.23, 'x': 1.23, 'z': 32.1}


def test_quaternion():
    q = msg.Quaternion(x=0.5, y=0.5, z=0.5, w=0.5)
    assert q == {'w': 0.5, 'y': 0.5, 'x': 0.5, 'z': 0.5}


def test_twist():
    t = msg.Twist()
    t['linear']['x'] = 55.0
    t['angular']['y'] = -56.7
    assert t == {'linear': {'y': 0.0, 'x': 55.0, 'z': 0.0}, 'angular': {'y': -56.7, 'x': 0.0, 'z': 0.0}}


def test_pose():
    p = msg.Pose()
    assert p == {'position': {'y': 0.0, 'x': 0.0, 'z': 0.0}, 'orientation': {'y': 0.0, 'x': 0.0, 'z': 0.0, 'w': 1.0}}


def test_posestamped():
    ps = msg.PoseStamped()
    ps['stamp'] = 1234567.89
    assert ps == {'stamp': 1234567.89, 'orientation': {'y': 0.0, 'x': 0.0, 'z': 0.0, 'w': 1.0}, 'position': {'y': 0.0, 'x': 0.0, 'z': 0.0}}


def test_wrench():
    w = msg.Wrench()
    assert w == {'torque': {'y': 0.0, 'x': 0.0, 'z': 0.0}, 'force': {'y': 0.0, 'x': 0.0, 'z': 0.0}}


def test_serialize():
    ps = msg.PoseStamped()
    ps['stamp'] = 1234567.89
    assert msg.deserialize(msg.serialize(ps)) == ps
