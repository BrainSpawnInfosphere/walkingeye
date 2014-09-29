#!/usr/bin/env python
#
# by Kevin J. Walchko 26 Aug 2014
#
# PS4 has 6 axes, 14 buttons, 1 hat
# This program doesn't grab all buttons, just the most useful :)

import cv2
import numpy as np

kf = cv2.KalmanFilter(3,3,0)
z = [0,0,0]
x