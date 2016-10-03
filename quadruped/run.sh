#!/bin/bash
# -----------------------
# this script is like a launch file, it:
# - starts up the bluetooth driver
# - joystick
# - robot
# and when the robot exits, it closes everything back down
# ----------------------
# change log:
# 2016-08-30 init

echo 'here we go!'

# fix issue
sudo chmod 0666 /dev/uinput

echo 'start bluetooth driver'
echo 'on PS4 controller, press PS button and share to sync'
ds4drv &

echo 'start joystick'
../chi/Joystick.py localhost 9000 &

echo 'start robot'
./Robot.py

echo 'ok ... shutting down now'
killall ds4drv
# killall Joystick
killall python
