#!/usr/bin/env python
# rungekutta.py
# 
# Copyright (C) 2009 Qiqi Wang
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or (at
# your option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor,
# Boston, MA 02110-1301, USA.
#

class FE:
    n = 1
    a = [[]]
    b = [1.]
    c = []
    d = None

class RK3:
    n = 3
    a = [[0.5, 0.],
         [-1., 2.]]
    b = [1./6, 2./3, 1./6]
    c = [0.5, 1.]
    d = None

class RK4:
    n = 4
    a = [[0.5, 0.,  0.],
         [0.,  0.5, 0.],
         [0.,  0.,  1.]]
    b = [1./6, 1./3, 1./3, 1./6]
    c = [0.5, 0.5, 1.]
    d = None

class ODE45:
    n = 7
    a = [[1./5,       0.,             0.,        0.,         0.,          0.],
         [3./40,      9./40,          0.,        0.,         0.,          0.],
         [44./45,     -56./15, 32./9, 0.,        0.,         0.,          0.],
         [19372./6561,-25360./2187, 64448./6561, -212./729,  0.,          0.],
         [9017./3168, -355./33,     46732./5247, 49./176,  -5103./18656,  0.],
         [35./384,    0.,           500./1113,   125./192, -2187./6784, 11./84]]
    d = [5179./57600, 0, 7571./16695, 393./640,-92097./339200, 187./2100, 1./40]
    c = [1./5, 3./10, 4./5, 8./9, 1., 1.]
    b = [35./384, 0, 500./1113, 125./192, -2187./6784, 11./84, 0]


import unittest
import numpy

def dxdt(x, t):
    return -x + numpy.sin(t + numpy.pi / 4)

def calcOrder(rk):
    DT = [0.02, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0]
    ERR = []
    for dt in DT:
        t, x = 0, 0
        traj = []
        for i in range(100):
            while t < i - 1E-8:
                x0, t0 = x, t
                dx = [dxdt(x, t)]
                for k in range(rk.n - 1):
                    t = t0 + dt * rk.c[k]
                    x = x0 + dt * numpy.dot(dx, rk.a[k][:k+1])
                    dx.append(dxdt(x, t))
                x = x0 + dt * numpy.dot(dx, rk.b)
                t = t0 + dt
            traj.append([t, x])
        
        traj = numpy.array(traj)
        err = numpy.abs(traj[:,1] - \
                        numpy.sqrt(0.5) * numpy.sin(traj[:,0])).mean()
        ERR.append(err)
    return numpy.log(max(ERR) / min(ERR)) / numpy.log(max(DT) / min(DT))

class TestRK(unittest.TestCase):
    def testFE(self):
        order = calcOrder(FE)
        print 'Forward Euler has order ', order
        self.assert_(0.8 < order < 1.3)

    def testRK3(self):
        order = calcOrder(RK3)
        print 'Runge Kutta 3 has order ', order
        self.assert_(2.5 < order < 3.5)

    def testRK4(self):
        order = calcOrder(RK4)
        print 'Runge Kutta 4 has order ', order
        self.assert_(3.5 < order < 4.5)

    def testODE45(self):
        order = calcOrder(ODE45)
        print 'ODE45 scheme has order ', order
        self.assert_(4.5 < order < 5.5)

if __name__ == '__main__':
    unittest.main()