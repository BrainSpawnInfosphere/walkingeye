#!/usr/bin/env python

# from __future__ import print_function
# from __future__ import division
# from Servo import Servo
# import time
# import logging
# # logging.basicConfig(level=logging.ERROR)
# logging.getLogger("Adafruit_I2C").setLevel(logging.ERROR)
#
#
# def loop(s0, s1, s2):
# 	dt = 0.5
# 	s0.angle = 45
# 	s1.angle = -60
# 	s2.angle = -70
# 	time.sleep(dt)
#
# 	s0.angle = 0
# 	s1.angle = -10
# 	s2.angle = 0
# 	time.sleep(dt)
#
# 	s0.angle = -45
# 	s1.angle = 10
# 	s2.angle = 0
# 	time.sleep(dt)
#
# def main():
# 	s0 = Servo(0)
# 	s1 = Servo(1)
# 	s2 = Servo(2)
# 	s0.all_stop()
#
# 	for i in range(0, 2):
# 		loop(s0, s1, s2)
#
# 	s0.all_stop()
#
# if __name__ == "__main__":
# 	main()
