#!/usr/bin/env python

# from __future__ import print_function
# from __future__ import division
from __future__ import print_function
from __future__ import division
import time
from Adafruit_PCA9685 import PCA9685
import math


class Servo(object):
	_angle = 0.0
	_pos0 = 0.0
	maxAngle = 90.0
	minAngle = -90.0
	
	"""
	Keeps info for servo. This only holds angle info.
	"""
	def __init__(self, pos0=0.0, limits=None):
		"""
		pin [int ]- pin number the servo is attached too
		pos0 [angle] - initial or neutral position
		rate - ???
		limits [angle, angle] - [optional] set the angular limits of the servo to avoid collision
		"""
		self.pos0 = pos0
		self.angle = pos0

		if limits: self.setServoLimits(*limits)

	@property
	def angle(self):
# 		print('@property angle')
		return self._angle
		
	@angle.setter
	def angle(self, angle):
		self._angle = max(min(self.maxAngle, angle), self.minAngle)
# 		print('@angle.setter: {} {}'.format(angle, self._angle))
	
	@property
	def pos0(self):
# 		print('@property pos0')
		return self._pos0
		
	@angle.setter
	def pos0(self, angle):
		self._pos0 = max(min(self.maxAngle, angle), self.minAngle)
# 		print('@pos0.setter: {} {}'.format(angle, self._angle))
		
	def setServoLimits(self, minAngle, maxAngle):
		"""
		sets maximum and minimum achievable angles.
		in:
			minAngle - degrees
			maxAngle - degrees
		"""
		self.maxAngle = maxAngle
		self.minAngle = minAngle

	def reset(self):
		"""
		Move servo to initial/neutral position
		in: None
		out: None
		"""
		self.angle = self.pos0

	def moveToAngle(self, angle):
		"""
		Moves the sevo to desired angle
		in: angle [radians]
		out: None
		"""
		self.angle = math.degrees(angle)


class ServoController(object):
	"""
	Tried to optimize pwm params for TG9e servos.
	TG9e = [130, 655]
	"""
	servos = []
	pwm_max = 655  # Max pulse length out of 4096
	pwm_min = 130  # Min pulse length out of 4096
	minAngle = -90  # not sure the right way to do this!
	maxAngle = 90

	def __init__(self, freq=60):
		self.pwm = PCA9685()
		self.pwm.set_pwm_freq(freq)
		for i in range(0, 16): self.servos.append(Servo())

	def moveAllServos(self, angle=None):
		for i, servo in enumerate(self.servos):
			if angle is None:
				angle = servo.angle
			pulse = self.angleToPWM(angle, servo.minAngle, servo.maxAngle)
			self.pwm.set_pwm(i, 0, pulse)

	def moveServo(self, i, angle=None):
		servo = self.servos[i]
		if angle is None:
			angle = servo.angle
		pulse = self.angleToPWM(angle, servo.minAngle, servo.maxAngle)
		self.pwm.set_pwm(i, 0, pulse)

	def angleToPWM(self, angle, mina, maxa):
		"""
		in:
			- angle: angle to convert to pwm pulse
			- mina: min servo angle
			- maxa: max servo angle
		out: pwm pulse size (0-4096)
		"""
		mina = self.minAngle
		maxa = self.maxAngle
		# servo_min = 150  # Min pulse length out of 4096
		# servo_max = 600  # Max pulse length out of 4096
		m = (self.pwm_max - self.pwm_min) / (maxa - mina)
		b = self.pwm_max - m * maxa
		pulse = m * angle + b  # y=m*x+b
		return int(pulse)

	def allStop(self):  # FIXME: 20160702 can i stop individual servos too?
		self.pwm.set_all_pwm(0,0x1000)
		
	def checkPwmRange(self, channel):
		self.allStop()
		for i in range(0, 700, 10):
			print('pos: {}'.format(i))
			self.pwm.set_pwm(channel, 0, i)
			time.sleep(1)
			# towerpro 100-660
			# tg9e 130-650
		self.allStop()


def handleArgs():
	parser = argparse.ArgumentParser(description='A simple zero MQ publisher for joystick messages')
	parser.add_argument('servo', help='servo number to tune: 0-15')
	parser.add_argument('-l', 'limits', nargs=2, help='servo angular limits: -90 90', default=[-90, 90])
	parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
	args = vars(parser.parse_args())
	return args
	

def main():
	channel = 15
	sc = ServoController()
	sc.allStop()
# 	sc.test(channel)
# 	for angle in range(-90,90,10): 
# 		sc.moveServo(channel, angle)
# 		time.sleep(1)
	sc.servos[channel].angle = 145.0
	sc.moveServo(channel)
	time.sleep(1)
	sc.servos[channel].angle = -90.0
	sc.moveServo(channel)
	time.sleep(1)
	
	sc.allStop()
	
	
if __name__ == "__main__":
	main()
