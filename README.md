# Python Robot Controller

[![Travis](https://img.shields.io/travis/walchko/soccer2.svg)](https://travis-ci.org/walchko/soccer2)
[![Code Health](https://landscape.io/github/walchko/soccer2/master/landscape.svg?style=flat)](https://landscape.io/github/walchko/soccer2/master)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/walchko/soccer2/master/MIT_License.txt)


My robot software.

* Doesn't use [ROS](http://ros.org), ROS is a pain to install and maintain on OSX and various linux systems
	* Uses some of the same ideas, but not RPC-XML
* Uses [Zero MQ](http://http://zeromq.org/) instead of `roscore`
* Uses my PS4 controller with PySDL2
* Uses [wit.ai](http://wit.ai) for speech-to-text
* Uses OpenCV to process on-board or stream video off-board to remote
* All of this runs on [Raspberry Pi3](http://www.raspberrypi.org)

**Note:** This re-write is still very early and not fully running yet, just parts.

## Wiki Documentation

Documentation is on the [wiki](https://github.com/walchko/soccer2/wiki)

## Layout of software

* docs - various PDFs, latex, or whatever for background
* lib - my ros alternative core libraries
* pics - pictures
* plugins - plugin modules for the speech/audio capabilities
* quadruped - walking robot ... move this somehow and combine with my wheeled robot (soccer)
* soccer - nonholonomic robot code
* sounds - sound clips for the speech/audio capabilities
* test - nose test scripts
* tmp - various things I am testing that may or may not work or make it to my robots
* tools - tools for my ros alternative
	* topic - publish/subscribe to a topic
	* bag - save messages for a topic to a file
	* camera_calibrate
	* mjpeg_server - take images and allow any browser to view them
	* webserver - not done
	* servic - not done

Need to organize everything in the main directory

# Future

If I think it is useful, I might break the infrastructure out into its own thing:

Chi (need a better name)

* Core
	* Pub/Sub/Service
	* Messages
	* BaseNodeClass
* Video
	* Camera Calibrate
	* Image View
	* Video
	* Video Save
* Motion
	* Holonomic
	* Non-Holonomic
	* Quadraped
* Tools
	* Topic

## Software Development

* flake8 - check for errors according to PEP8 (automatically done in my atom editor)
* Landscape.io - on push, check code for errors
* travis.ci - on push, run unit tests on commit to github
* quantifiedcode - on push, check for errors and will submit auto fixes (pull requests) for simple errors
* srcclr - check code and associated libraries for licenses
