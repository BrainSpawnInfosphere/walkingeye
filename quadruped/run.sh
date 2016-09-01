#!/usr/local/bin/bash
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

echo 'start bluetooth driver'
dsdrv &

echo 'start joystick'
../chi/Joystick.py localhost 9000 &

echo 'start robot'
./Robot.py

echo 'ok ... shutting down now'
killall dsdrv
killall Joystick
