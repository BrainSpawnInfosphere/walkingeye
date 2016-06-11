#!/usr/bin/env python

import time
import robot.controller as Controller

from robot.robotInterfaces.virtualRobot.virtualRobotVrep import VirtualRobotVrep as VirtualRobot


def run():
	robot = VirtualRobot()
	cntlr = Controller.RobotController(robot)
	cntlr.start()

	while True:
		cntlr.iterate()
		time.sleep(0.05)

if __name__ == "__main__":
	run()
