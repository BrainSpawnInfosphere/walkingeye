# Python Robot Controller

This is the second version of my soccer robot.

* Doesn't use [ROS](http://ros.org), ROS is a pain to install and maintain on OSX and various linux systems
	* Uses some of the same ideas, but instead of RPC-XML, simple sockets
	* Want to re-write to get rid of pickle and replace with json (faster, better)
* Uses my PS4 controller with PySDL2
* Uses Google-translate to for TTS
* Uses OpenCV to compress and send video stream off-board
	* Might use a separate IP camera to reduce CPU usage and get faster performance
* All of this runs on Raspberry Pi B+

This is still in development, but various parts are working.

## Basic Diagram
                
```                
AI ---+---> robot.py <--- sensors
      |        | |
PS4 --+        | +---> actuators
Sensor Proc <--+
```
(I need a better diagram)

**Note:** This re-write is still very early and not fully running yet, just parts. 

## To Do's

* 