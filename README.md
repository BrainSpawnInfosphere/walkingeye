# Python Robot Controller

This is the second version of my soccer robot.

* Doesn't use [ROS](http://ros.org), ROS is a pain to install and maintain on OSX and various linux systems
	* Uses some of the same ideas, but not RPC-XML
* Uses [Mosquito](http://mosquitto.org) instead of `roscore` 
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

* python-forecastio - weather
* PyWit - text-to-speech
* PySDL2 - simulation and joystick
* twilio - SMS
* PyAudio - recording sound (had to build from scratch)
* PyYAML - read yaml config files
* phao-mqtt - python bindings for MQTT

## Sound Server

The robot uses [wit.ai](https://wit.ai) to understand the spoken word, turning speech in to text (stt). There are a bunch of plugins which act upon the text to perform different things:

 * Say current time
 * Say current date
 * Send a text message using [Twilio](https://www.twilio.com)
 * Tell a joke (most of the jokes are not funny)
 * Say a greeting
 * Tell you to stop being mean or cursing
 * Play random sound bites from movie and tv shows:
 	* Venture Brothers
 	* Blues Brothers
 	* Star Wars
 * Tell current or future weather forecast using [Forcast.io](http://forecast.io)
 * Grab news headlines
 * General help info
 
Additionally, the text-to-speech part uses [Google Translate](https://translate.google.com) (which sounds the best) or uses `say`.

## SSH Login Art

You can create ascii art from jpegs or text with the programs:

    jp2a --background=light -i --output='art.txt' <some_file.jpg>
    figlet 'hello world'

## Message Flow

Parts:

* RobotCmdServer - controls motors, leds, servos, etc
* RobotSensorServer - publishes processed/conditioned sensors readings
* RobotSoundServer - handles voice commands and sounds

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