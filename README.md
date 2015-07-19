# Python Robot Controller

This is the second version of my soccer robot.

* Doesn't use [ROS](http://ros.org), ROS is a pain to install and maintain on OSX and various linux systems
	* Uses some of the same ideas, but not RPC-XML
* Uses [Zero MQ](http://http://zeromq.org/) instead of `roscore` 
* Uses my PS4 controller with PySDL2
* Uses [wit.ai](http://wit.ai) for speech-to-text
* Uses Google-translate to for text-to-speech
* Uses OpenCV to compress and send video stream off-board
	* Might use a separate IP camera to reduce CPU usage and get faster performance
* All of this runs on [Raspberry Pi B+](http://www.raspberrypi.org)

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

## Libraries Used

You need the following key python libraries installed:

* PySDL2 - simulation and joystick
* PyYAML - read yaml config files
* pyzmq - interprocess communication library

## SSH Login Art

You can create ascii art from jpegs or text with the programs:

    jp2a --background=light -i --output='art.txt' <some_file.jpg>
    figlet 'hello world'

Use `brew` to install::
	
	brew install jp2a

## Message Flow

Parts:

* RobotHardwareServer - controls motors, leds, servos, etc
* RobotCameraServer - publishes images from USB camera, streams base64 encoded images

Message Flow:

```
    js(twist/cmd) ----> RobotCmdServer <--(twist/cmd)-- ai
                                    ^                  | ^  
    RobotSoundServer(twist/cmd) ----+                  | |
                ^                                      | |
                +-------------------------(sound)------+ |
                     RobotSensorServer(sensor/image) ----+ 
```

Here is simple layout of message formate to support the flow shown above.

Messages:

| Header | Format                                 |
|--------|----------------------------------------|
|header  | {time_stamp}                           |
|vec     | {x,y,z}                                |
|twist   | {linear[vec],angular[vec]}             |
|wrench  | {force[vec],torque[vec]}               |
|cmd     | {motors:[1,2,3,4],servo[1,2], ...}     |
|sound   | {sound}                                |
|imu     | {accel[vec],gyro[vec],comp[vec],temp}  |
|sensor  | {header,[imu], ...}                    |
|image   | {header,image}                         |
|pose    | {x,y,heading}                          |


## To Do's

* put it all together :)