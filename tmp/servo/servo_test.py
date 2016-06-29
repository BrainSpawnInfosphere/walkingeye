
from __future__ import print_function
from __future__ import division
import time
from Adafruit_PCA9685 import PCA9685


def angleToPWM(angle, min, max):
	servo_min = 150  # Min pulse length out of 4096
	servo_max = 600  # Max pulse length out of 4096
	m = (servo_max - servo_min) / (max - min)
	b = servo_max - m * max
	pulse = m * angle + b  # y=mx+b
	return int(pulse)

channel = 3
pwm = PCA9685()
pwm.set_pwm_freq(60)  # not sure why ... should be 50 Hz

pwm.set_pwm(channel, 0, 150)
time.sleep(3)
pwm.set_pwm(channel, 0, 600)
time.sleep(3)

angle = -90.0

while angle < 90.0:
	pulse = angleToPWM(angle, -90, 90)
	pwm.set_pwm(channel, 0, pulse)
	time.sleep(0.1)  # 50 Hz update rate
	angle += 5.0
