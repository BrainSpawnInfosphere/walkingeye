#! /usr/bin/env python

from __future__ import print_function
from __future__ import division
# import argparse
import time
# import datetime as dtm
# import math
import logging
import multiprocessing as mp
import lib.Messages as Msg
import lib.zmqclass as Zmq

# import platform
# if platform.system().lower() == 'linux':
from lib.BNO055 import BNO055
# else:
# 	class BNO055(object):
# 		def __init__(self, a): pass
# 		def begin(self): pass
# 		def get_system_status(self): return 1, 0x0F, 0
# 		def read_euler(self): return 0, 0, 0


class IMUError(Exception):
	pass


class Imu(mp.Process):
	def __init__(self, host="localhost", port='9000'):
		mp.Process.__init__(self)

		logging.basicConfig(level=logging.DEBUG)
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

		except Exception as err:
			raise IMUError('IMU init error: {0}'.format(err))

	def run(self):
		bno = self.bno

		pub = Zmq.Pub(self.pubinfo)

		while True:
			msg = Msg.IMU()

			# Read the Euler angles for heading, roll, pitch (all in degrees).
			heading, roll, pitch = bno.read_euler()
			msg['heading'] = heading
			# Read the calibration status, 0=uncalibrated and 3=fully calibrated.
			# sys, gyro, accel, mag = bno.get_calibration_status()
			# Print everything out.
			# print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}'.format(heading, roll, pitch))
			# print('Sys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(sys, gyro, accel, mag))
			# Other values you can optionally read:
			# Orientation as a quaternion:
			x, y, z, w = bno.read_quaternion()
			msg['orientation'].update({'x': x, 'y': y, 'z': z, 'w': w})
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
			# ax, ay, az = bno.read_accelerometer()
			# msg['linear_acceleration'].update({'x': x, 'y': y, 'z': z})
			# print('accel[x,y,z]: {0:0.2F}\t{1:0.2F}\t{2:0.2F}'.format(ax, ay, az))
			# Linear acceleration data (i.e. acceleration from movement, not gravity--
			# returned in meters per second squared):
			x, y, z = bno.read_linear_acceleration()
			msg['linear_acceleration'].update({'x': x, 'y': y, 'z': z})
			# print('linaccel[x,y,z]: {0:0.2F}\t{1:0.2F}\t{2:0.2F}'.format(x, y, z))
			# Gravity acceleration data (i.e. acceleration just from gravity--returned
			# in meters per second squared):
			# x, y, z = bno.read_gravity()
			# print('gravity[x,y,z]: {0:0.2F}\t{1:0.2F}\t{2:0.2F}'.format(x, y, z))
			# Sleep for a second until the next reading.
			# print('-----------------------------------\n\n')
			self.logger.debug(msg)

			pub.pub('imu', msg)

			time.sleep(0.1)


def main():
	serialPort = None
	import platform
	if platform.system().lower() == 'linux':
		serialPort = ''
	else:
		serialPort = '/dev/tty.usbserial-A4004Qzg'

	imu = Imu()
	imu.init(serialPort)
	imu.start()

if __name__ == "__main__":
	main()
