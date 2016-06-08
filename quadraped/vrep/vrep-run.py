#!/usr/bin/env python
# import time
from robot import controller

# from robot.robotInterfaces.virtualRobot.virtualRobot import VirtualRobot
from robot.robotInterfaces.virtualRobot.virtualRobotVrep import VirtualRobotVrep as VirtualRobot
# from robot.robotInterfaces.realRobot.realRobot import RealRobot

# robot1 = VirtualRobot()

# try:
	# robot2 = RealRobot()
# except Exception, e:
	#  print e
	#  robot2 = None
# controller1 = controller.RobotController(robot1)
# controller1.start()

# controller2 = None
# if robot2:
	#  controller2 = controller.RobotController(robot2)
	#  controller2.start()

# print("script ready!")


def run():
	robot1 = VirtualRobot()
	controller1 = controller.RobotController(robot1)
	controller1.start()
	# global controller1, controller2
	controller1.iterate()
	# time.sleep(0.02)
	# if robot2:
		# controller2.iterate()

if __name__ == "__main__":
	while True:
		run()
