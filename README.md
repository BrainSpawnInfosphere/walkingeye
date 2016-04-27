# Python Robot Controller

This is the second version of my soccer robot.

* Doesn't use [ROS](http://ros.org), ROS is a pain to install and maintain on OSX and various linux systems
	* Uses some of the same ideas, but not RPC-XML
* Uses [Zero MQ](http://http://zeromq.org/) instead of `roscore`
* Uses my PS4 controller with PySDL2
* Uses [wit.ai](http://wit.ai) for speech-to-text
* Uses OpenCV to process on-board or stream video off-board to remote
* All of this runs on [Raspberry Pi B+](http://www.raspberrypi.org)

**Note:** This re-write is still very early and not fully running yet, just parts.

## Libraries Used

You need the following key python libraries installed:

* PySDL2 - simulation and joystick
* PyYAML - read yaml config files
* pyzmq - interprocess communication library
* smbus-cffi - [I2C](https://pypi.python.org/pypi/smbus-cffi) support
* Adafruit - various libraries

## Wiki

Documentation is on the [wiki](https://github.com/walchko/soccer2/wiki)

## Install

### Adafruit

**TODO** Sort out this adafruit library mess ... there are so many and they are duplicates!

You will need the following libraries from Adafruit for:

####[GPIO](https://github.com/adafruit/Adafruit_Python_GPIO)

	sudo apt-get update
	sudo apt-get install build-essential python-pip python-dev python-smbus git
	git clone https://github.com/adafruit/Adafruit_Python_GPIO.git
	cd Adafruit_Python_GPIO
	python setup.py install

####[LED Matrix](https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code):

	git clone https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code.git

Have a look at the LEDBackpack 8x8_pixel example
	
####[IMU](https://github.com/adafruit/Adafruit_Python_BNO055):

	git clone git@github.com:adafruit/Adafruit_Python_BNO055.git
	cd Adafruit_Python_BNO055
	python setup.py install


### RPi

	sudo apt-get install build-essential libi2c-dev i2c-tools python-dev libffi-dev
	sudo apt-get install libsdl2-dev
	sudo apt-get install libzmq3-dev
	sudo apt-get install gnustep-gui-runtime
	pip install cffi smbus-cffi
	pip install pysdl2
	pip install pyzmq

