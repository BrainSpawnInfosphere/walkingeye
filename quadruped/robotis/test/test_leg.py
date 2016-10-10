#!/usr/bin/env python

# from __future__ import print_function
# from __future__ import division
# from ..Servo import Servo
# from ..Leg import Leg
# import numpy as np
#
# def test_fk_ik():
# 	length = {
# 		'coxaLength': 26,
# 		'femurLength': 42,
# 		'tibiaLength': 63
# 	}
# 	channels = [0, 1, 2]
# 	leg = Leg(length, channels)
#
# 	angles = [0, -70, -90]
#
# 	pts = leg.fk(*angles)
# 	angles2 = leg.ik(*pts)
# 	pts2 = leg.fk(*angles2)
# 	# angles2 = [r2d(a), r2d(b), r2d(c)]
# 	print('angles (orig):', angles)
# 	print('pts from fk(orig): {:.2f} {:.2f} {:.2f}'.format(*pts))
# 	print('angles2 from ik(pts): {:.2f} {:.2f} {:.2f}'.format(*angles2))
# 	print('pts2 from fk(angle2): {:.2f} {:.2f} {:.2f}'.format(*pts2))
# 	# print('diff:', np.linalg.norm(np.array(angles) - np.array(angles2)))
# 	print('diff [mm]: {:.2f}'.format(np.linalg.norm(pts - pts2)))
# 	# time.sleep(1)
# 	# assert(np.linalg.norm(np.array(angles) - np.array(angles2)) < 0.00001)
#
#
# def printError(pts, pts2, angles, angles2):
# 	print('angles (orig):', angles)
# 	print('angles2 from ik(pts): {:.2f} {:.2f} {:.2f}'.format(*angles2))
# 	print('pts from fk(orig): {:.2f} {:.2f} {:.2f}'.format(*pts))
# 	print('pts2 from fk(angle2): {:.2f} {:.2f} {:.2f}'.format(*pts2))
# 	# print('diff:', np.linalg.norm(np.array(angles) - np.array(angles2)))
# 	print('diff [mm]: {:.2f}'.format(np.linalg.norm(pts - pts2)))
#
#
# def test_full_fk_ik(c=[0, 1, 2]):
# 	length = {
# 		'coxaLength': 26,
# 		'femurLength': 42,
# 		'tibiaLength': 63
# 	}
# 	channels = c
# 	leg = Leg(length, channels)
#
# 	servorange = [[-90, 90], [-90, 90], [-180, 0]]
# 	for s in range(0, 3):
# 		leg.servos[s].setServoRangeAngle(*servorange[s])
#
# 	for i in range(1, 3):
# 		for a in range(-70, 70, 10):
# 			angles = [0, 0, -10]
# 			if i == 2: a -= 90
# 			angles[i] = a
# 			pts = leg.fk(*angles)
# 			angles2 = leg.ik(*pts)
# 			pts2 = leg.fk(*angles2)
#
# 			angle_error = np.linalg.norm(np.array(angles) - np.array(angles2))
# 			pos_error = np.linalg.norm(pts - pts2)
# 			# print(angle_error, pos_error)
#
# 			if angle_error > 0.0001:
# 				print('Angle Error')
# 				printError(pts, pts2, angles, angles2)
# 				exit()
#
# 			elif pos_error > 0.0001:
# 				print('Position Error')
# 				printError(pts, pts2, angles, angles2)
# 				exit()
#
# 			else:
# 				print('Good: {} {} {}  error(deg,mm): {} {}'.format(angles[0], angles[1], angles[2], angle_error, pos_error))
# 				leg.move(*pts)
# 				# time.sleep(0.1)
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


# 
# if __name__ == "__main__":
# 	main()
