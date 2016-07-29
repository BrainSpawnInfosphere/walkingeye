__author__ = 'will'



import serial
import time

ser = serial.Serial(port='/dev/ttyUSB0',
                    baudrate=115200,
                    timeout=0.0001)


pos = 0

def send_16(value):
    high = chr(value >> 8)
    low = chr(value%256)
    ser.write(low)
    ser.write(high)

def move_servo_to(servo,pos):
    #ser.write(">$c")
    ser.write(">$a")
    ser.write(chr(servo))
    send_16(pos)

while True:
    value = 1000
    while(value < 2000):
        value +=1
        move_servo_to(3, value)
        time.sleep(0.01)
        print(ser.read(1000))
    while(value > 1000):
        value -=1
        move_servo_to(3, value)
        time.sleep(0.01)
        print(ser.read(1000))