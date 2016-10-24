#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import sys
from pyxl320 import DummySerial
# from ..Servo import Servo
sys.path.insert(0, '..')
from Servo import Servo
from Leg import Leg
import numpy as np
from kinematics import DH
from math import pi

def test_fk_ik():
	length = {
		'coxaLength': 26,
		'femurLength': 42,
		'tibiaLength': 63
	}
	channels = [0, 1, 2]
	limits = [[-90, 90], [-90, 90], [-180, 0]]
	offsets = [150, 150, 150+90]
	leg = Leg(length, channels, DummySerial('test_port'), limits, offsets)

	# angles = [45, 70, -90]
	angles = [0, 45, -145]

	pts = leg.fk(*angles)
	angles2 = leg.ik(*pts)
	pts2 = leg.fk(*angles2)
	# angles2 = [r2d(a), r2d(b), r2d(c)]
	print('angles (orig):', angles,'deg')
	print('pts from fk(orig): {:.2f} {:.2f} {:.2f} mm'.format(*pts))
	print('angles2 from ik(pts): {:.2f} {:.2f} {:.2f} deg'.format(*angles2))
	print('pts2 from fk(angle2): {:.2f} {:.2f} {:.2f} mm'.format(*pts2))
	# print('diff:', np.linalg.norm(np.array(angles) - np.array(angles2)))
	print('diff [mm]: {:.2f}'.format(np.linalg.norm(pts - pts2)))
	# time.sleep(1)
	# assert(np.linalg.norm(np.array(angles) - np.array(angles2)) < 0.00001)


def printError(pts, pts2, angles, angles2):
	print('****************************************************')
	print('angles (orig):', angles)
	print('angles2 from ik(pts): {:.2f} {:.2f} {:.2f}'.format(*angles2))
	print('pts from fk(orig): {:.2f} {:.2f} {:.2f}'.format(*pts))
	print('pts2 from fk(angle2): {:.2f} {:.2f} {:.2f}'.format(*pts2))
	# print('diff:', np.linalg.norm(np.array(angles) - np.array(angles2)))
	print('diff [mm]: {:.2f}'.format(np.linalg.norm(pts - pts2)))
	print('\nExiting\n')
	print('****************************************************')


def test_full_fk_ik(c=[0, 1, 2]):
	length = {
		'coxaLength': 26,
		'femurLength': 42,
		'tibiaLength': 63
	}
	channels = c
	serial = DummySerial('test_port')
	limits = [[-90,90], [-90,90], [-180,0]]
	offset = [150, 150, 150+90]
	leg = Leg(length, channels, serial, limits, offset)

	# servorange = [[-90, 90], [-90, 90], [-180, 0]]
	# for s in range(0, 3):
	# 	leg.servos[s].setServoRangeAngle(*servorange[s])

	for i in range(1, 3):
		print('------------------------------------------------')
		for a in range(limits[i][0],limits[i][1], 10):
			angles = [0, 0, -10]
			# if i == 2: a -= 90
			angles[i] = a
			pts = leg.fk(*angles)
			angles2 = leg.ik(*pts)
			pts2 = leg.fk(*angles2)

			angle_error = np.linalg.norm(np.array(angles) - np.array(angles2))
			pos_error = np.linalg.norm(pts - pts2)
			# print(angle_error, pos_error)

			if angle_error > 0.0001:
				print('Angle Error')
				printError(pts, pts2, angles, angles2)
				exit()

			elif pos_error > 0.0001:
				print('Position Error')
				printError(pts, pts2, angles, angles2)
				exit()

			else:
				print('Good: {} {} {}  error(deg,mm): {:.4} {:.4}\n'.format(angles[0], angles[1], angles[2], angle_error, pos_error))
				leg.move(*pts)
				# time.sleep(0.1)
#
# 	Servo.all_stop()


# def check_range():
# 	length = {
# 		'coxaLength': 26,
# 		'femurLength': 42,
# 		'tibiaLength': 63
# 	}
#
# 	channels = [0, 1, 2]
# 	# limits = [[-45, 45], [-45, 45], [-90, 0]]
#
# 	leg = Leg(length, channels)
# 	time.sleep(1)
# 	for servo in range(0, 3):
# 		leg.servos[0].angle = 45; time.sleep(0.01)
# 		leg.servos[1].angle = 0; time.sleep(0.01)
# 		leg.servos[2].angle = -90; time.sleep(0.01)
# 		for angle in range(-45, 45, 20):
# 			# if servo == 2: angle -= 90
# 			print('servo: {} angle: {}'.format(servo, angle))
# 			leg.servos[servo].angle = angle
# 			time.sleep(1)

def test_DH():
	coxa = 20
	femur = 50
	tibia = 100
	offset = 0
	t1 = 0
	t2 = 45
	t3 = -90-45
	# a, alpha, d, theta
	params = [
		[ coxa, 90,       0, t1],
		[femur,  0,       0, t2],
		[tibia, -90, offset, t3]
	]
	dh = DH()
	t = dh.fk(params)
	print(t)
	print('1 2 3: {:.2f} {:.2f} {:.2f}'.format(t[0,3],t[1,3],t[2,3]))

def test_fk_ik2():
	length = {
		'coxaLength': 26,
		'femurLength': 42,
		'tibiaLength': 63
	}
	channels = [0, 1, 2]
	limits = [[-90, 90], [-90, 90], [-180, 0]]
	offsets = [150, 150, 150+90]
	leg = Leg(length, channels, DummySerial('test_port'), limits, offsets)

	# angles = [45, 70, -90]
	angles = [0, 45, -145]

	pts = leg.fk(*angles)
	angles2 = leg.ik(*pts)
	pts2 = leg.fk(*angles2)
	# angles2 = [r2d(a), r2d(b), r2d(c)]
	print('angles (orig):', angles,'deg')
	print('pts from fk(orig): {:.2f} {:.2f} {:.2f} mm'.format(*pts))
	print('angles2 from ik(pts): {:.2f} {:.2f} {:.2f} deg'.format(*angles2))
	print('pts2 from fk(angle2): {:.2f} {:.2f} {:.2f} mm'.format(*pts2))
	# print('diff:', np.linalg.norm(np.array(angles) - np.array(angles2)))
	print('diff [mm]: {:.2f}'.format(np.linalg.norm(pts - pts2)))
	# time.sleep(1)
	# assert(np.linalg.norm(np.array(angles) - np.array(angles2)) < 0.00001)


if __name__ == "__main__":
	# main()
	# test_fk_ik()
	# test_full_fk_ik()
	# test_DH()
	test_fk_ik2()
