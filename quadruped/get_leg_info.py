#!/usr/bin/env python

##############################################
# The MIT License (MIT)
# Copyright (c) 2017 Kevin Walchko
# see LICENSE for full details
##############################################

from __future__ import print_function, division
from pyxl320 import ServoSerial
from pyxl320.Packet import le, makeReadPacket
from pyxl320.xl320 import ErrorStatusMsg
import argparse
import simplejson as json
from serial import SerialException
import sys
# from pprint import pprint


class PacketDecoder(object):
	F = 0
	C = 1

	def __init__(self, pkt, offset=0):
		self.id = pkt[4]  # save servo ID
		self.instr = pkt[7]  # should be 0x55 (85) for status packet
		self.len = self.get16b(pkt[5], pkt[6]) - 4  # don't count: instr, error, crc[0,1]
		self.pkt = pkt[9:-2]  # remove header, crc, and other stuff ... keep only data section
		self.offset = offset
		self.error = pkt[8]  # should be 0 if all is well

		# print('data len', self.len)
		# print('len', len(self.pkt))
		# print('type', self.type)

	def checkError(self):
		"""
		Does the return status packet say there is an error?

		return:
			True: there is an error and prints info to std out
			False: all is good with the world ... turtles all the way down
		"""
		# ID = pkt[4]
		# instr = pkt[7]
		# err = pkt[8]
		if self.instr == 0x55:
			if self.error == 0x00:
				return False
			else:
				print('Servo[{}]: {}'.format(self.id, ErrorStatusMsg[self.error]))
				return True
		else:
			print('Servo[{}]: did not give a status message'.format(self.id))
			return True
		return True

	@staticmethod
	def check_base(base):
		if base < 0:
			raise Exception('PacketDecoder::base < 0')

	@staticmethod
	def get16b(low, high):
		return (high << 8) + low

	def getBase(self, reg):
		base = reg - self.offset

		if base < 0:
			raise Exception('PacketDecoder::base < 0')

		if base >= self.len:
			raise Exception('PacketDecoder::packet not long enough to access this packet')

		return base

	def voltage(self):
		base = self.getBase(45)
		return self.pkt[base]/10

	def angle(self):
		base = self.getBase(37)
		return self.get16b(self.pkt[base], self.pkt[base+1])/1023 * 300.0

	def load(self):
		base = 41-self.offset
		self.check_base(base)
		load = self.get16b(self.pkt[base], self.pkt[base+1])
		direction = 'CW' if (load & 1024) == 1024 else 'CCW'
		percent = (load & 1023)/1023 * 100
		return percent, direction

	def temperature(self, scale=0):
		base = 46-self.offset
		self.check_base(base)
		temp = 0.0
		if scale == self.F:
			temp = self.pkt[base]*9/5+32
		else:
			temp = self.pkt[base]*1.0
		return temp

	def hw_error(self):
		base = 50-self.offset
		self.check_base(base)
		return self.pkt[base]


def returnPktError(pkt):
	"""
	Does the return status packet say there is an error?

	return:
		True: there is an error and prints info to std out
		False: all is good with the world ... turtles all the way down
	"""
	ID = pkt[4]
	instr = pkt[7]
	err = pkt[8]
	if instr == 0x55:
		if err == 0x00:
			return False
		else:
			print('Servo[{}]: {}'.format(ID, ErrorStatusMsg[err]))
			return True
	else:
		print('Servo[{}]: did not get a status message')
		return True
	return True


def writeToFile(data, filename='data.json'):
	with open(filename, 'w') as outfile:
		json.dump(data, outfile)


# def get16b(l, h):
# 	return (h << 8) + l


def pktToDict(p):
	# print('pkt', pkt)
	# print('len(pkt)', len(pkt))
	ans = {}
	ans['ID'] = p.id
	ans['Present Position'] = p.angle()
	ans['Present Voltage'] = p.voltage()
	ans['Present Load'] = '{:>5.1f}% {}'.format(*p.load())
	ans['Present Temperature'] = p.temperature(PacketDecoder.F)
	ans['Hardware Error Status'] = p.hw_error()

	return ans


DESCRIPTION = """
Returns limited info for each leg servo.

./get_leg_info.py /dev/tty.usbserial-AL034G2K
Opened /dev/tty.usbserial-AL034G2K @ 1000000

Servos: 1 - 12
--------------------------------------------------
Servo: 1  		HW Error: 0
Position [deg]: 139.6  Load:   0.0% CCW
Voltage [V]  7.0     Temperature [F]:  80.6
--------------------------------------------------
Servo: 2  		HW Error: 0
Position [deg]: 178.9  Load:   4.5% CW
Voltage [V]  7.1     Temperature [F]:  86.0
--------------------------------------------------
Servo: 3  		HW Error: 0
Position [deg]: 119.1  Load:   0.0% CCW
Voltage [V]  7.1     Temperature [F]:  80.6
--------------------------------------------------
Servo: 4  		HW Error: 0
Position [deg]: 146.6  Load:   0.8% CCW
Voltage [V]  7.3     Temperature [F]:  80.6
--------------------------------------------------
Servo: 5  		HW Error: 0
Position [deg]: 275.4  Load:   0.8% CCW
Voltage [V]  7.1     Temperature [F]:  80.6
--------------------------------------------------
Servo: 6  		HW Error: 0
Position [deg]: 104.1  Load:   0.0% CCW
Voltage [V]  7.3     Temperature [F]:  82.4
--------------------------------------------------
Servo: 7  		HW Error: 0
Position [deg]: 163.9  Load:   0.0% CCW
Voltage [V]  7.2     Temperature [F]:  80.6
--------------------------------------------------
Servo: 8  		HW Error: 0
Position [deg]: 279.5  Load:   0.0% CCW
Voltage [V]  7.1     Temperature [F]:  80.6
--------------------------------------------------
Servo: 9  		HW Error: 0
Position [deg]: 100.3  Load:   0.0% CCW
Voltage [V]  7.1     Temperature [F]:  84.2
--------------------------------------------------
Servo: 10  		HW Error: 0
Position [deg]: 156.3  Load:   0.0% CCW
Voltage [V]  7.1     Temperature [F]:  82.4
--------------------------------------------------
Servo: 11  		HW Error: 0
Position [deg]: 280.6  Load:   0.0% CCW
Voltage [V]  7.2     Temperature [F]:  80.6
--------------------------------------------------
Servo: 12  		HW Error: 0
Position [deg]:  97.7  Load:   0.0% CCW
Voltage [V]  7.1     Temperature [F]:  84.2
--------------------------------------------------
"""


def handleArgs():
	parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('port', help='serial port  or \'dummy\' for testing', type=str)
	parser.add_argument('-j', '--json', metavar='FILENAME', help='save info to a json file: --json my_file.json', type=str)

	args = vars(parser.parse_args())
	return args


def getSingle(ID, ser):
	pkt = makeReadPacket(ID, 37, le(50-37+1))
	# print('made packet:', pkt)

	ans = ser.sendPkt(pkt)
	if ans:
		ans = ans[0]
		pd = PacketDecoder(ans, 37)  # data packet starts at register 37
		if pd.checkError():
			raise Exception('Crap!')
		ans = pktToDict(pd)

	return ans


def printServo(s):
	print('-'*50)
	print('Servo: {}  \t\tHW Error: {}'.format(s['ID'], s['Hardware Error Status']))
	print('Position [deg]: {:5.1f}  Load: {}'.format(s['Present Position'], s['Present Load']))
	print('Voltage [V] {:4.1f}     Temperature [F]: {:5.1f}'.format(s['Present Voltage'], s['Present Temperature']))


def main():
	args = handleArgs()
	port = args['port']

	s = ServoSerial(port=port)

	# open serial port
	try:
		s.open()
	except SerialException as e:
		print('-'*20)
		print(sys.argv[0], 'encountered an error')
		print(e)
		exit(1)

	ids = range(1, 13)

	resp = {}
	for k in ids:
		resp[k] = None

	# get servo data
	try:
		for i in ids:
			data = getSingle(i, s)
			resp[i] = data
	except Exception as e:
		print(e)
		exit(1)

	cnt = 10
	while cnt:
		cnt = 0
		for k, v in resp.items():
			# search through and find servos w/o responses (i.e., None)
			if v is None:
				cnt += 1  # found a None
				ans = getSingle(k, s)
				resp[k] = ans

	print('')
	print('Servos: 1 - 12')
	for i in range(1, 13):
		printServo(resp[i])
	print('-' * 50)
	print('')

	if args['json']:
		print('Saving servo angle info to {}'.format(args['json']))
		writeToFile(resp, args['json'])

	s.close()


if __name__ == '__main__':
	main()
