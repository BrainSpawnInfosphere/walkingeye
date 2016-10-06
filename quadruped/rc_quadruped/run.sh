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
./Robot.py &

# fix issue
sudo chmod 0666 /dev/uinput

# fix issue
sudo chmod 0666 /dev/uinput

echo 'start bluetooth driver'
<<<<<<< HEAD
echo 'on PS4 controller, press PS button and share to sync'
ds4drv &
=======
ds4drv &

echo 'wait 10 sec'
sleep 10s
>>>>>>> origin/master

echo 'start joystick'
../chi/Joystick.py localhost 9000 

# echo 'start robot'
# ./Robot.py

echo 'ok ... shutting down now'
killall ds4drv
<<<<<<< HEAD
# killall Joystick
killall python
=======
#killall Joystick
killall "Robot"
>>>>>>> origin/master
