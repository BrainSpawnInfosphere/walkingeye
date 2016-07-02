#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
import time
from Adafruit_PCA9685 import PCA9685, software_reset
# from pca9685_driver import Device

# import Adafruit_GPIO.I2C as I2C
# i2c = I2C
# 
# software_reset(i2c)

channel = 3
mins = 200
maxs = 400
neutral = int((maxs+mins)/2)
# maxs = 600
# mins = 100


def angleToPWM(angle, min, max):
	servo_min = mins  # Min pulse length out of 4096
	servo_max = maxs  # Max pulse length out of 4096
	m = (servo_max - servo_min) / (max - min)
	b = servo_max - m * max
	pulse = m * angle + b  # y=mx+b
	return int(pulse)

pwm = PCA9685()
# pwm = Device(0x40)

print('Turn everything off')
pwm.set_all_pwm(0,0x1010)

pwm.set_pwm_freq(60)  # not sure why ... should be 50 Hz
# pwm.set_pwm_frequency(60)

# print('change all to {}'.format(neutral))
# for i in range(0,16):
# # 	pwm.set_pwm(i, neutral)
# 	pwm.set_pwm(i, 0, neutral)

# time.sleep(1)
# 
# print('here we go!')
# pwm.set_pwm(channel, 0, mins)
# # pwm.set_pwm(channel, mins)
# time.sleep(2)
# pwm.set_pwm(channel, 0, maxs)
# # pwm.set_pwm(channel, maxs)
# time.sleep(2)
# 
# angle = -90.0

# print('PWM freq: {}'.format(pwm.get_pwm_frequency()))

# while angle < 90.0:
# 	pulse = angleToPWM(angle, -90, 90)
# 	pwm.set_pwm(channel, 0, pulse)
# # 	pwm.set_pwm(channel, pulse)
# 	time.sleep(0.1)
# 	angle += 10.0

# pwm.set_pwm(channel, neutral)
pwm.set_pwm(channel, 0, neutral)

print('Turn everything off')
pwm.set_all_pwm(0,0x1010)