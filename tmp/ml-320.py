#!/usr/bin/env python
#
#
# Change log:
#    2016-08-16  init

from __future__ import print_function
import serial
from time import sleep

"""
This code uses:
http://support.robotis.com/en/product/dynamixel_pro/communication/instruction_status_packet.htm
"""


crc_table = [
	0x0000, 0x8005, 0x800F, 0x000A, 0x801B, 0x001E, 0x0014, 0x8011,
	0x8033, 0x0036, 0x003C, 0x8039, 0x0028, 0x802D, 0x8027, 0x0022,
	0x8063, 0x0066, 0x006C, 0x8069, 0x0078, 0x807D, 0x8077, 0x0072,
	0x0050, 0x8055, 0x805F, 0x005A, 0x804B, 0x004E, 0x0044, 0x8041,
	0x80C3, 0x00C6, 0x00CC, 0x80C9, 0x00D8, 0x80DD, 0x80D7, 0x00D2,
	0x00F0, 0x80F5, 0x80FF, 0x00FA, 0x80EB, 0x00EE, 0x00E4, 0x80E1,
	0x00A0, 0x80A5, 0x80AF, 0x00AA, 0x80BB, 0x00BE, 0x00B4, 0x80B1,
	0x8093, 0x0096, 0x009C, 0x8099, 0x0088, 0x808D, 0x8087, 0x0082,
	0x8183, 0x0186, 0x018C, 0x8189, 0x0198, 0x819D, 0x8197, 0x0192,
	0x01B0, 0x81B5, 0x81BF, 0x01BA, 0x81AB, 0x01AE, 0x01A4, 0x81A1,
	0x01E0, 0x81E5, 0x81EF, 0x01EA, 0x81FB, 0x01FE, 0x01F4, 0x81F1,
	0x81D3, 0x01D6, 0x01DC, 0x81D9, 0x01C8, 0x81CD, 0x81C7, 0x01C2,
	0x0140, 0x8145, 0x814F, 0x014A, 0x815B, 0x015E, 0x0154, 0x8151,
	0x8173, 0x0176, 0x017C, 0x8179, 0x0168, 0x816D, 0x8167, 0x0162,
	0x8123, 0x0126, 0x012C, 0x8129, 0x0138, 0x813D, 0x8137, 0x0132,
	0x0110, 0x8115, 0x811F, 0x011A, 0x810B, 0x010E, 0x0104, 0x8101,
	0x8303, 0x0306, 0x030C, 0x8309, 0x0318, 0x831D, 0x8317, 0x0312,
	0x0330, 0x8335, 0x833F, 0x033A, 0x832B, 0x032E, 0x0324, 0x8321,
	0x0360, 0x8365, 0x836F, 0x036A, 0x837B, 0x037E, 0x0374, 0x8371,
	0x8353, 0x0356, 0x035C, 0x8359, 0x0348, 0x834D, 0x8347, 0x0342,
	0x03C0, 0x83C5, 0x83CF, 0x03CA, 0x83DB, 0x03DE, 0x03D4, 0x83D1,
	0x83F3, 0x03F6, 0x03FC, 0x83F9, 0x03E8, 0x83ED, 0x83E7, 0x03E2,
	0x83A3, 0x03A6, 0x03AC, 0x83A9, 0x03B8, 0x83BD, 0x83B7, 0x03B2,
	0x0390, 0x8395, 0x839F, 0x039A, 0x838B, 0x038E, 0x0384, 0x8381,
	0x0280, 0x8285, 0x828F, 0x028A, 0x829B, 0x029E, 0x0294, 0x8291,
	0x82B3, 0x02B6, 0x02BC, 0x82B9, 0x02A8, 0x82AD, 0x82A7, 0x02A2,
	0x82E3, 0x02E6, 0x02EC, 0x82E9, 0x02F8, 0x82FD, 0x82F7, 0x02F2,
	0x02D0, 0x82D5, 0x82DF, 0x02DA, 0x82CB, 0x02CE, 0x02C4, 0x82C1,
	0x8243, 0x0246, 0x024C, 0x8249, 0x0258, 0x825D, 0x8257, 0x0252,
	0x0270, 0x8275, 0x827F, 0x027A, 0x826B, 0x026E, 0x0264, 0x8261,
	0x0220, 0x8225, 0x822F, 0x022A, 0x823B, 0x023E, 0x0234, 0x8231,
	0x8213, 0x0216, 0x021C, 0x8219, 0x0208, 0x820D, 0x8207, 0x0202
]


def crc16(data_blk):
	"""
	This is addapted from:
	http://support.robotis.com/en/product/dynamixel_pro/communication/crc.htm
	"""
	data_blk_size = len(data_blk)
	crc_accum = 0
	for j in range(data_blk_size):
		i = ((crc_accum >> 8) ^ data_blk[j]) & 0xFF
		# crc_accum = ((crc_accum << 8) ^ crc_table[i]) % (2 ** 16)  # original
		crc_accum = ((crc_accum << 8) ^ crc_table[i]) & 0xffff
		# crc_accum = ((crc_accum << 8) ^ crc_table[i])

	print('crc:', crc_accum)

	return crc_accum


def le(h):
	"""
	Little-endian, takes a 16b number and returns
	"""
	# return [h % 256, h >> 8]
	return [h & 0xff, (h >> 8) & 0xff]


# [0xFF, 0xFF, 0xFD, 0x00, ID, LEN_L, LEN_H, INST, PARAM 1, PARAM 2, ..., PARAM N, CRC_L, CRC_H]
def makeWritePacket(ID, reg, values):
	"""
	little-endian so 7 hex is 0x07 0x00 (L H)
	"""
	pkt = []
	header = [0xFF, 0xFF, 0xFD]
	reserved = [0x00]
	write_instr = [0x03]

	# pkt = header + reserved + ID
	pkt.extend(header)
	pkt.extend(reserved)
	pkt.extend([ID])

	# if values:
	# instr reg [values length] crc_l crc_h = values lenght + 4
	# length = le(len(values) + 5)  # calc length and put into little endian
	# pkt += length + write_instr
	pkt += [0x00, 0x00]  # length placeholder
	pkt += write_instr
	pkt += le(reg)
	pkt += values  # servo position

	length = le(len(pkt))
	pkt[5] = length[0]  # L
	pkt[6] = length[1]  # H

	crc = crc16(pkt)
	pkt += le(crc)

	print(pkt)

	return pkt


# [0xFF, 0xFF, 0xFD, 0x00, ID, LEN_L, LEN_H, INST, PARAM 1, PARAM 2, ..., PARAM N, CRC_L, CRC_H]
def makeReset(ID):
	reboot = 0x08
	pkt = [0xFF, 0xFF, 0xFD, 0x00, ID, 0x00, 0x00, reboot]

	length = le(len(pkt))
	pkt[5] = length[0]  # L
	pkt[6] = length[1]  # H

	crc = crc16(pkt)
	pkt += le(crc)

	print(pkt)

	return pkt


def moveServo(ID, angle):
	if not (0.0 < angle < 300.0):
		raise Exception('moveServo(), angle out of bounds: {}'.format(angle))
	val = int(angle/300*1024)
	pkt = makeWritePacket(ID, 0x30, le(val))
	return pkt


# http://forums.trossenrobotics.com/showthread.php?7489-Hard-Can-anyone-give-me-a-sample-packet-by-running-function-quot-Reading-Current-Position-quot-for-Dynamixel-Pro-Motors
# [0xFF, 0xFF, 0xFD, 0x00, ID, LEN_L, LEN_H, INST, PARAM 1, PARAM 2, ..., PARAM N, CRC_L, CRC_H]
# ----headers------
# 0xff 0xff 0xfd 0x00
# ----ID----
# 0x01
# ----Length----
# 0x07 0x00
# ----INST=READ----
# 0x02
# ----Address----
# 0x63 0x02
# ----Data Length---
# 0x04 0x00
# ----CRC_L -> CRC_H-----
# 0x1B 0xF9
# pro: current position is reg: 611 = (0x02<<8)+0x63 and is 4 bytes long
#     [ header       | res|  ID | len      | inst |  param1   | param 2  ]
# buf = [0xff,0xff,0xfd,0x00, 0x01, 0x07,0x00,  0x02,  0x63,0x02, 0x04,0x00]
# ans=crc16(buf)
# b=le(ans)
# print('new L 0x1B H 0xF9', hex(b[0]), hex(b[1]))
# print('new L 27 H 159', b[0], b[1])

def test_crc16():
	# http://forums.trossenrobotics.com/showthread.php?7489-Hard-Can-anyone-give-me-a-sample-packet-by-running-function-quot-Reading-Current-Position-quot-for-Dynamixel-Pro-Motors
	# [0xFF, 0xFF, 0xFD, 0x00, ID, LEN_L, LEN_H, INST, PARAM 1, PARAM 2, ..., PARAM N, CRC_L, CRC_H]
	# ----headers------
	# 0xff 0xff 0xfd 0x00
	# ----ID----
	# 0x01
	# ----Length----
	# 0x07 0x00
	# ----INST=READ----
	# 0x02
	# ----Address----
	# 0x63 0x02
	# ----Data Length---
	# 0x04 0x00
	# ----CRC_L -> CRC_H-----
	# 0x1B 0xF9
	# pro: current position is reg: 611 = (0x02<<8)+0x63 and is 4 bytes long
	#     [ header       | res|  ID | len      | inst |  param1   | param 2  ]
	buf = [0xff,0xff,0xfd,0x00, 0x01, 0x07,0x00,  0x02,  0x63,0x02, 0x04,0x00]
	ans = crc16(buf)
	b = le(ans)
	assert b[0] == 0x1B and b[1] == 0xF9


class DynamixelSerial(object):
	DD_WRITE = False  # data direction set to write
	DD_READ = True    # data direction set to read
	SLEEP_TIME = 0.0001

	def __init__(self, port):
		self.serial = serial.Serial()
		self.serial.baudrate = 1000000
		self.serial.port = port

	def __del__(self):
		self.serial.close()

	def open(self):
		self.serial.open()
		self.serial.setRTS(self.DD_WRITE)
		serial.time.sleep(self.SLEEP_TIME)

	def read(self):
		self.serial.setRTS(self.DD_READ)
		serial.time.sleep(self.SLEEP_TIME)
		data = self.serial.read()
		return data

	def write(self, data):
		self.serial.setRTS(self.DD_WRITE)
		serial.time.sleep(self.SLEEP_TIME)
		self.serial.write(data)
		# self.serial.flushOutput()

	def close(self):
		self.serial.close()


def main():
	s = serial.Serial()
	s.baudrate = 1000000
	s.port = "/dev/tty.usbserial-A5004Flb"
	s.open()
	s.setRTS(False)

	# pkt = makeWritePacket(0xfe, 0x30, le(512))  # move servo 1 to middle position
	pkt = moveServo(0xfe, 150)
	# pkt = makeReset(0xfe)

	s.flushInput()
	s.flushOutput()
	s.setRTS(False)
	pkt = bytearray(pkt)  # use to prep for transmition
	s.write(pkt)
	print(pkt)


if __name__ == '__main__':
	main()










##########################################################
# msg = [0xFF, 0xFF, 0xFD, 0x00, 0x01, 0x07, 0x00, 0x02, 0x00, 0x00, 0x00, 0x02]
# a = crc16(msg, len(msg))
# print(hex(a))


# set register values
# def setReg(ID,reg,values):
# 	length = 3 + len(values)
# 	checksum = 255-((index+length+AX_WRITE_DATA+reg+sum(values))%256)
# 	s.write(chr(0xFF)+chr(0xFF)+chr(ID)+chr(length)+chr(AX_WRITE_DATA)+chr(reg))
# 	for val in values:
# 		s.write(chr(val))
# 	s.write(chr(checksum))
#
# def getReg(index, regstart, rlength):
# 	s.flushInput()
# 	checksum = 255 - ((6 + index + regstart + rlength)%256)
# 	s.write(chr(0xFF)+chr(0xFF)+chr(index)+chr(0x04)+chr(AX_READ_DATA)+chr(regstart)+chr(rlength)+chr(checksum))
# 	vals = list()
# 	s.read()   # 0xff
# 	s.read()   # 0xff
# 	s.read()   # ID
# 	length = ord(s.read()) - 1
# 	s.read()   # toss error
# 	while length > 0:
# 		vals.append(ord(s.read()))
# 		length = length - 1
# 	if rlength == 1:
# 		return vals[0]
# 	return vals

# def prep(pkt):
# 	ans = ''
# 	for p in pkt:
# 		ans += chr(p)
# 	return ans

# t = bytearray((0xff, 0xff, 0xfd))
# print('bytearray', t)
# setReg(1, 30, ((512%256), (512>>8)))  # this will move servo 1 to centered position (512)
# print getReg(1,43,1)			   # get the temperature
# print('test', chr(0x10), chr(0xff))
