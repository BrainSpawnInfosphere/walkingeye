from __future__ import print_function
from __future__ import division
import time
from Adafruit_PCA9685 import PCA9685


#!/usr/bin env python
from __future__ import print_function
from __future__ import division
import math


class Servo(object):
	"""
	Keeps info for servo.
	"""
	def __init__(self, pin, pos0, rate, limits=None):
		"""
		pin [int ]- pin number the servo is attached too
		pos0 [angle] - initial or neutral position
		rate - ???
		limits [angle, angle] - [optional] set the angular limits of the servo
		"""
		self.pos0 = pos0
		self.rate = rate
		self.pin = pin

		if limits:
			self.setServoLimits(*limits)
		else:
			self.maxAngle = 90
			self.minAngle = -90

		# self.serial = serial
		self.angle = 0

	def clamp(self, angle):
		"""
		clamps angle between min/max angle range
		"""
		return max(min(self.maxAngle, angle), self.minAngle)

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

	# def getServoAngle(self):
	# 	"""
	# 	Return the current commanded servo angle
	# 	in: None
	# 	out: servo angle [degrees]
	# 	"""
	# 	return self.angle

	def moveToAngle(self, angle):
		"""
		Moves the sevo to desired angle
		in: angle [radians]
		out: None
		"""
		angle = math.degrees(angle)

		# clamp to limits
		newAngle = clamp(angle, self.minAngle, self.maxAngle)

		if newAngle != self.angle:
			self.angle = newAngle


class ServoController(object):
	servos = []
	pwm_max = 600  # Max pulse length out of 4096
	pwm_min = 200  # Min pulse length out of 4096
	minAngle = -90  # not sure the right way to do this!
	maxAngle = 90

	def __init__(self, freq=60):
		self.pwm = PCA9685()
		self.pwm.set_pwm_freq(freq)
		for i in range(0, 16): self.servos[i] = Servo(i, 0, 0)

	def moveAllServos(self):
		for i, servo in enumerate(self.servos):
			pulse = self.angleToPWM(servo.angle, servo.minAngle, servo.maxAngle)
			self.pwm.set_pwm(i, 0, pulse)

	def moveServo(self, i):
		servo = self.servos[i]
		pulse = self.angleToPWM(servo.angle, servo.minAngle, servo.maxAngle)
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

	def allStop(self):
		self.pwm.set_all_pwm(0,0x1010)

def testRange(servo):
	sc = ServoController()

def handleArgs():
	parser = argparse.ArgumentParser(description='A simple zero MQ publisher for joystick messages')
	parser.add_argument('servo', help='servo number to tune: 0-15')
	parser.add_argument('-l', 'limits', nargs=2, help='servo angular limits: -90 90', default=[-90, 90])
	parser.add_argument('-v', '--verbose', help='display info to screen', action='store_true')
	args = vars(parser.parse_args())
	return args

# channel = 3
# pwm = PCA9685()
# pwm.set_pwm_freq(60)  # not sure why ... should be 50 Hz
#
# pwm.set_pwm(channel, 0, 150)
# time.sleep(3)
# pwm.set_pwm(channel, 0, 600)
# time.sleep(3)
#
# angle = -90.0
#
# while angle < 90.0:
# 	pulse = angleToPWM(angle, -90, 90)
# 	pwm.set_pwm(channel, 0, pulse)
# 	time.sleep(0.1)  # 50 Hz update rate
# 	angle += 5.0

def main():
	args = handleArgs()
	mins, maxs = args['limits']
	pwm = PCA9685()
	pwm.set_pwm_freq(60)

if __name__ == "__main__":
	main()
