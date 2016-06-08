# Python Robot Controller

[![Travis](https://img.shields.io/travis/walchko/soccer2.svg)](https://travis-ci.org/walchko/soccer2)
[![Code Health](https://landscape.io/github/walchko/soccer2/master/landscape.svg?style=flat)](https://landscape.io/github/walchko/soccer2/master)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/walchko/soccer2/master/MIT_License.txt)

This is the second version of my soccer robot.

* Doesn't use [ROS](http://ros.org), ROS is a pain to install and maintain on OSX and various linux systems
	* Uses some of the same ideas, but not RPC-XML
* Uses [Zero MQ](http://http://zeromq.org/) instead of `roscore`
* Uses my PS4 controller with PySDL2
* Uses [wit.ai](http://wit.ai) for speech-to-text
* Uses OpenCV to process on-board or stream video off-board to remote
* All of this runs on [Raspberry Pi B+](http://www.raspberrypi.org)

**Note:** This re-write is still very early and not fully running yet, just parts.

## Wiki Documentation

Documentation is on the [wiki](https://github.com/walchko/soccer2/wiki)

## Layout of software

* config - config files
* docs - various PDFs, latex, or whatever for background
* IMU[old] - old inertial measurement software, need to remove
* lib - my ros alternative core libraries
* node[old] - human machine interface, most likely stick with all python, need to remove
* pic - pictures
* plugins - plugin modules for the speech/audio capabilities
* quadruped - walking robot ... move this somehow and combine with my wheeled robot
* sim[old] - used pygame, not really completely running, need to remove
* sound - sound clips for the speech/audio capabilities
* test - nose test scripts
* tmp - various things I am testing that may or may not work or make it to my robot
* tools - tools for my ros alternative

# Future

If I think it is useful, I might break the infrastructure out into its own thing:

MyRos (need a better name)

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

* flake8 - check for errors according to PEP8
* Landscape.io - check code for errors
* travis.ci - run unit tests on commit to github
