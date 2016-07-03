#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
# import time
import robot.controller as Controller

from robot.robotInterfaces.virtualRobot.virtualRobotVrep import VirtualRobotVrep as VirtualRobot


def run():
	robot = VirtualRobot()
	cntlr = Controller.RobotController(robot)
	cntlr.start()

	while True:
		cntlr.iterate()

if __name__ == "__main__":
	run()
