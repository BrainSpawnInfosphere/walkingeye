# Robotis Quadruped

This is my second one after the RC version, which didn't work as nicely as I wanted it too.

## Software

* Robot - pyGecko driver
* Quadruped - basic wrapper around leg and gait algorithms
* Leg - forward/reverse kinematics
* Gait - syncronization of how the 4 legs walk

## Hardware

### Raspberry Pi

![RPI 3](https://www.raspberrypi.org/wp-content/uploads/2016/02/Pi_3_Model_B.png)

I am currently using a 1.2 GHz quad core [RPi 3](https://www.adafruit.com/products/3055) (ARMv8) as the main board running the lite version of Raspbian. It has on-board:

* 802.11n Wifi
* Bluetooth 4.1 BLE

### Camera Interface (CSI)

* [PiCamera](https://www.adafruit.com/products/3099) is used for video odometry

### USB

* A [Logitech c270 camera](http://www.logitech.com/en-us/product/hd-webcam-c270) provides video and microphone capabilities

## Cost

Here is a parts list of **key components** that I am using. I am not listing wires, bread boards, cables, etc. Also note,
I have rounded up the costs (i.e., $4.95 => $5). Also, lot of the body is 3d printed, the costs for that are not shown here.

| Part | Source | Number | Item Cost | Sum | Notes |
| ---  | ---    | ---    | ---       | --- | ---   |
| RPi v3    | [Adafruit](https://www.adafruit.com) | 1 | $40 | $40 | Main board, has wifi and bluetooth already |
| Pi Camera | [Adafruit](https://www.adafruit.com) | 1 | $30 | $30 | 8 Mpixel |
| 9-DOF IMU (BNO055) | [Adafruit](https://www.adafruit.com) | 1 | $35 | $35 | It is an AHRS, works over I2C |
| 5V, 5A Buck Converter (D24V50F5)  | [Adafruit](https://www.adafruit.com) | 4 | $15 | $15 | For powering my electronics |
| Dynamixel xl-320 smart servo | [RobotShop](https://www.robotshop.com) | 12 | $22 | $264 |  |
| PS4 Controller   | [Walmart](http://www.walmart.com) | 1 | $54 | $54 | |
| Micro SD (32 GB) | [Walmart](http://www.walmart.com) | 1 | $12 | $12 | |
| Logitech C270 | [Walmart](http://www.walmart.com) | 1 | $30 | $30 | Connected via USB, also use the on board microphone |

# License

## Software

The MIT License (MIT)
Copyright (c) 2016 Kevin J. Walchko

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Hardware

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">
	<img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" />
</a>
<br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.