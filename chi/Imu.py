#! /usr/bin/env python

from __future__ import print_function
from __future__ import division
# import argparse
import time
import logging
import multiprocessing as mp
import lib.Messages as Msg
import lib.zmqclass as Zmq
from otherLibs.BNO055 import BNO055
from math import cos, sin, atan2, asin, sqrt
from math import radians as d2r
from math import degrees as r2d

"""
serial port fix
https://frillip.com/raspberry-pi-3-uart-baud-rate-workaround/

Fucking cell phones!!!!
https://developer.android.com/reference/android/hardware/SensorEvent.html
https://msdn.microsoft.com/en-us/library/dn433240(v=vs.85).aspx
https://source.android.com/devices/sensors/sensor-types.html
https://blogs.msdn.microsoft.com/b8/2012/01/24/supporting-sensors-in-windows-8/
y is roll - wtf
x is pitch - wtf
z is yaw/heading

magnometers
http://www51.honeywell.com/aero/common/documents/myaerospacecatalog-documents/Defense_Brochures-documents/Magnetic__Literature_Application_notes-documents/AN203_Compass_Heading_Using_Magnetometers.pdf

pitch/roll
http://cache.freescale.com/files/sensors/doc/app_note/AN4248.pdf

attitude
https://www.astro.rug.nl/software/kapteyn/_downloads/attitude.pdf
https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles

accellerometers
http://www.instructables.com/id/Accelerometer-Gyro-Tutorial/
http://physics.rutgers.edu/~aatish/teach/srr/workshop3.pdf
"""


def acceleration2Euler(x, y, z):
	"""
	Given an accelerometer reading, it returns the roll and pitch of an euler
	angle. Note, this does not return yaw because gravity alone doesn't provide
	enough info to do that.

	Note: this assumes accel's give +1 g when the z-axis is pointing up (opposite
	of what it should give, but cell phones want that)
	"""
	# x, y, z = bno.read_gravity()
	roll = atan2(y, z)
	pitch = atan2(-x, sqrt(y**2+z**2))
	# print('roll {:.2f}, pitch {:.2f}'.format(r2d(roll), r2d(pitch)))
	return roll, pitch


def quaternion2Euler(w, x, y, z):
	"""
	Convert quaterion (w,x,y,z) into a euler angle (r,p,y)

	https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
	"""
	roll = atan2(2.0*(w*x+y*z), 1.0-2.0*(x**2+y**2))
	pitch = asin(2.0*(w*y-z*x))
	yaw = atan2(2.0*(w*z+x*y), 1.0-2.0*(y**2+z**2))
	# print('r {:.2f} p {:.2f} y {:.2f}'.format(r2d(roll), r2d(pitch), r2d(yaw)))
	return roll, pitch, yaw


class IMUError(Exception):
	pass


class Imu(mp.Process):
	def __init__(self, host="localhost", port='9000'):
		mp.Process.__init__(self)

		# logging.basicConfig(level=logging.DEBUG)
		self.logger = logging.getLogger(__name__)

		self.pubinfo = (host, port)

	def init(self, USB_SERIAL_PORT):  # FIXME: 20160605 put these into logging
		try:
			self.bno = BNO055(serial_port=USB_SERIAL_PORT)
			if not self.bno.begin():
				raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

			status, self_test, error = self.bno.get_system_status()
			self.logger.debug('System status: {0}', status)
			self.logger.debug('Self test result (0x0F is normal): 0x{0:02X}', self_test)
			# Print out an error if system status is in error mode.
			if status == 0x01:
				self.logger.debug('System error: {0}', error)
				self.logger.debug('See datasheet section 4.3.59 for the meaning.')

			# Print BNO055 software revision and other diagnostic data.
			sw, bl, accel, mag, gyro = self.bno.get_revision()
			self.logger.debug('Software version:   {0}', sw)
			self.logger.debug('Bootloader version: {0}', bl)
			self.logger.debug('Accelerometer ID:   0x{0:02X}', accel)
			self.logger.debug('Magnetometer ID:	0x{0:02X}', mag)
			self.logger.debug('Gyroscope ID:	   0x{0:02X}\n', gyro)

			# ans = self.bno.get_axis_remap()
			# ans = self.bno._read_byte(0x3B)  # android is default
			# print('ans', ans)
			# exit()
			# self.bno._read_vector(BNO055_UNIT_SEL_ADDR, 1)


			# Axis remap values
			# AXIS_REMAP_X                         = 0x00
			# AXIS_REMAP_Y                         = 0x01
			# AXIS_REMAP_Z                         = 0x02
			# AXIS_REMAP_POSITIVE                  = 0x00
			# AXIS_REMAP_NEGATIVE                  = 0x01
			# self.bno.set_axis_remap(AXIS_REMAP_Y, AXIS_REMAP_X, AXIS_REMAP_Z)

		except Exception as err:
			raise IMUError('IMU init error: {0}'.format(err))

	def run(self):
		bno = self.bno

		pub = Zmq.Pub(self.pubinfo)

		while True:
			msg = Msg.IMU()

			try:
				# Read the Euler angles for heading, roll, pitch (all in degrees).
				# fucking cell phones use y-roll, x-pitch, z-yaw
				# this seems to be hard coded, but quaternions and gyro rates are correct
				heading, pitch, roll = bno.read_euler()
				# msg['heading'] = heading
				msg['heading'] = [heading, -pitch, -roll]
				# Read the calibration status, 0=uncalibrated and 3=fully calibrated.
				# sys, gyro, accel, mag = bno.get_calibration_status()
				# Print everything out.
				# print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}'.format(heading, roll, pitch))
				# print('Sys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(sys, gyro, accel, mag))
				# Other values you can optionally read:
				# Orientation as a quaternion:
				x, y, z, w = bno.read_quaternion()
				msg['orientation'].update({'x': x, 'y': y, 'z': z, 'w': w})
				# https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
				# roll = atan2(2.0*(w*x+y*z), 1.0-2.0*(x**2+y**2))
				# pitch = asin(2.0*(w*y-z*x))
				# yaw = atan2(2.0*(w*z+x*y), 1.0-2.0*(y**2+z**2))
				# print('r {:.2f} p {:.2f} y {:.2f}'.format(r2d(roll), r2d(pitch), r2d(yaw)))

				# print('quat[x,y,z,w]: {0:0.2F}\t{1:0.2F}\t{2:0.2F}\t{3:0.2F}'.format(x, y, z, w))
				# Sensor temperature in degrees Celsius:
				temp_c = bno.read_temp()
				msg['temperature'] = temp_c
				# print('temp[C]: {0:0.2F}'.format(temp_c))
				# Magnetometer data (in micro-Teslas):
				# x, y, z = bno.read_magnetometer()
				# print('mag[x,y,z]: {0:0.2F}\t{1:0.2F}\t{2:0.2F}'.format(x, y, z))
				# Gyroscope data (in degrees per second):
				x, y, z = bno.read_gyroscope()
				msg['angular_velocity'].update({'x': x, 'y': y, 'z': z})
				# print('gyro[x,y,z]: {0:0.2F}\t{1:0.2F}\t{2:0.2F}'.format(x, y, z))
				# Accelerometer data (in meters per second squared):
				# x, y, z = bno.read_accelerometer()
				# acceleration2Euler(x,y,z)
				# msg['linear_acceleration'].update({'x': x, 'y': y, 'z': z})
				# print('accel[x,y,z]: {0:0.2F}\t{1:0.2F}\t{2:0.2F}'.format(x, y, z))

				# gx, gy, gz = bno.read_gravity()
				# print('me[x,y,z]: {0:0.2F}\t{1:0.2F}\t{2:0.2F}'.format(gx-x, gy-y, gz-z))
				# Linear acceleration data (i.e. acceleration from movement, not gravity--
				# returned in meters per second squared):
				x, y, z = bno.read_linear_acceleration()
				msg['linear_acceleration'].update({'x': x, 'y': y, 'z': z})
				# acceleration2Euler(x,y,z)
				# print('linaccel[x,y,z]: {0:0.2F}\t{1:0.2F}\t{2:0.2F}'.format(x, y, z))
				# Gravity acceleration data (i.e. acceleration just from gravity--returned
				# in meters per second squared):
				# x, y, z = bno.read_gravity()
				# x *= -1
				# y *= -1
				# z *= -1
				# acceleration2Euler(x, y, z)
				"""
				https://developer.android.com/reference/android/hardware/SensorEvent.html

				fucking phones!!!

				Examples:
				- When the device lies flat on a table and is pushed on its left side toward the
				  right, the x acceleration value is positive.
				- When the device lies flat on a table, the acceleration value is +9.81, which
				  correspond to the acceleration of the device (0 m/s^2) minus the force of
				  gravity (-9.81 m/s^2).
				- When the device lies flat on a table and is pushed toward the sky with an
				  acceleration of A m/s^2, the acceleration value is equal to A+9.81 which
				  correspond to the acceleration of the device (+A m/s^2) minus the force of
				  gravity (-9.81 m/s^2).
				"""
				# print('gravity[x,y,z]: {0:0.2F}\t{1:0.2F}\t{2:0.2F}'.format(-x, -y, -z))
				# roll = atan2(z,y)
				# pitch = atan2(y*sin(roll)+z*cos(roll), -x)
				# roll = atan2(y, z)
				# pitch = atan2(-x, y*sin(roll)+z*cos(roll))
				# pitch = atan2(-x, sqrt(y**2+z**2))
				# print('roll {:.2f}, pitch {:.2f}'.format(r2d(roll), r2d(pitch)))
				# print('gravity[x,y,z]: {0:0.2F}\t{1:0.2F}\t{2:0.2F}'.format(x, y, z))
				# Sleep for a second until the next reading.
				# print('-----------------------------------\n\n')
				self.logger.debug(msg)
				pub.pub('imu', msg)
				# print('imu', msg)

			except RuntimeError as e:
				self.logger.error(e)
				continue

			time.sleep(0.1)


def main():
	serialPort = None
	import platform
	os = platform.system().lower()
	if os == 'linux':
		serialPort = ''
	elif os == 'darwin':
		serialPort = '/dev/tty.usbserial-A4004Qzg'
	else:
		serialPort = raw_input('please enter serial port name')

	imu = Imu()
	imu.init(serialPort)
	imu.start()

if __name__ == "__main__":
	main()
