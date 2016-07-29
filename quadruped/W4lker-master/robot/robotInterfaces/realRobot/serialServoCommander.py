import struct
import serial
from threading import Thread
try:
    from Queue import Queue
except:
    from queue import Queue
import time


pos = 0

class SerialComms(Thread):
    """
    Class responsible for taking care of all serial communications, by using a queue of commands.
    """
    ser = None

    def __init__(self):
        print ("starting serial")
        Thread.__init__(self)
        self.ser = serial.Serial(port='/dev/ttyUSB0',
                                 baudrate=115200,
                                 timeout=0.0001)
        self.input_pins = 15
        self.running = True
        self.imu = [0, 0, 0]
        self.queue = Queue()
        print ("serial connection stabilished, starting thread")


    def run(self):
        """
        Runs the thread, the main loop waits until there's a function to call on the queue, and calls it. if it's empty,
        it just waits.
        """
        while self.running:

            if not self.queue.empty():
                f = self.queue.get()
                f()
            else:
                time.sleep(0.0006)
        self.ser.close()

    def read_pins(self):
        """
        Sends serial message regarding feet status, and waits for it's response. the response is saved on self.input_pins
        """
        self.serwrite(">$b")
        buff = ""
        start = time.time()
        while "pins:" not in buff:
            if time.time() - start > 0.05:
                return
            buff += self.ser.read(1)
        try:
            self.ser.read(1)
            data = ord(self.ser.read(1)) & 0b00001111
        except Exception, e:
            print("Serial error, ", e)
            return
        self.input_pins = data

    def read_imu(self):
        """
        Sends Imu read message, waits for answer, and saves the result on self.imu
        :return:
        """
        self.serwrite(">$c")
        buff = ""
        start = time.time()
        while "imu:" not in buff:
            if time.time() - start > 0.05:
                return
            buff += self.ser.read(1)

        buff = buff.split("imu:")[-1]
        while "!<" not in buff:
            if time.time() - start > 0.05:
                return
            try:
                data = self.ser.read(1)
                buff += data
            except:
                pass
        imu = buff.split("!<")[0]
        self.imu = imu.split(',')
        try:
            self.imu = [float(i)/10 for i in self.imu]
        except:
            self.imu = [0,0,0]


    def send_16(self, value):
        """
        sends 16bit values as 8bit bytes
        """

        def packIntegerAsULong(value):
            """Packs a python 4 byte unsigned integer to an arduino unsigned long"""
            return struct.pack('H', value)
        try:
            data = packIntegerAsULong(value)
            msg = bytearray()
            msg.extend(data)
            lrc = 0
            for b in msg:
                lrc ^= b
            msg.append(lrc)
            self.ser.write(msg)


        except Exception as e:
            print ("SERIAL ERROR!" , e)

    def serwrite(self, s):
        """
        writes serial data.
        """
        #self.ser.write(bytes(s, 'UTF-8'))
        self.ser.write(s)

    def move_servo_to(self, servo, pos):
        """
        sends serial servo move message, and waits for it's answer.
        """
        self.serwrite(">$a")
        self.serwrite(chr(servo))
        self.send_16(pos)
        for i in range(3):
            if 'a' in str(self.ser.read(1)):
                if '!' in str(self.ser.read(1)):
                    return
