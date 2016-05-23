#!/usr/bin/env python

import logging
import sys
import time
import BNO055


# Create and configure the BNO sensor connection.  Make sure only ONE of the
# below 'bno = ...' lines is uncommented:
# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
# bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)
# BeagleBone Black configuration with default I2C connection (SCL=P9_19, SDA=P9_20),
# and RST connected to pin P9_12:
bno = BNO055.BNO055()


# Enable verbose debug logging if -v is passed as a parameter.
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if something went wrong.
if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

# Print system status and self test result.
status, self_test, error = bno.get_system_status()
print('System status: {0}'.format(status))
print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
# Print out an error if system status is in error mode.
if status == 0x01:
    print('System error: {0}'.format(error))
    print('See datasheet section 4.3.59 for the meaning.')

# Print BNO055 software revision and other diagnostic data.
sw, bl, accel, mag, gyro = bno.get_revision()
print('Software version:   {0}'.format(sw))
print('Bootloader version: {0}'.format(bl))
print('Accelerometer ID:   0x{0:02X}'.format(accel))
print('Magnetometer ID:    0x{0:02X}'.format(mag))
print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

print('Reading BNO055 data, press Ctrl-C to quit...')

data = []
start = time.time()
now = start
limit = 10
while (now-start)<limit:
	# Read the Euler angles for heading, roll, pitch (all in degrees).
	# heading, roll, pitch = bno.read_euler()
	# Read the calibration status, 0=uncalibrated and 3=fully calibrated.
	#    sys, gyro, accel, mag = bno.get_calibration_status()
	# Print everything out.
	#     print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
	#           heading, roll, pitch, sys, gyro, accel, mag))
	# Other values you can optionally read:
	# Orientation as a quaternion:
	qx,qy,qz,qw = bno.read_quaternion()
	#print('quat[x,y,z,w]: {0:0.2F}\t{1:0.2F}\t{2:0.2F}\t{3:0.2F}'.format(qx,qy,qz,qw))
	# Sensor temperature in degrees Celsius:
	#temp_c = bno.read_temp()
	# Magnetometer data (in micro-Teslas):
	mx,my,mz = bno.read_magnetometer()
	# Gyroscope data (in degrees per second):
	gx,gy,gz = bno.read_gyroscope()
	# Accelerometer data (in meters per second squared):
	ax,ay,az = bno.read_accelerometer()
	# print('accel[x,y,z]: {0:0.2F}\t{1:0.2F}\t{2:0.2F}'.format(ax,ay,az))
	# Linear acceleration data (i.e. acceleration from movement, not gravity--
	# returned in meters per second squared):
	#x,y,z = bno.read_linear_acceleration()
	# Gravity acceleration data (i.e. acceleration just from gravity--returned
	# in meters per second squared):
	#x,y,z = bno.read_gravity()
	# Sleep for a second until the next reading.

	sample = {time.time(),ax,ay,az,gx,gy,gz,mx,my,mz,qx,qy,qz,qw}
	data.append(sample)
	time.sleep(0.1)
	now = time.time()

np.save('imu-data',data)
