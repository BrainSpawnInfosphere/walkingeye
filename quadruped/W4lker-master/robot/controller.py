import time
from robot.gaits import TrotGait, TrotGait2

__author__ = 'will'

import math
from math import radians as d2r
from robot.tranforms import rotate
from robot import robotData
# from robot.input.keylistener import KeyListener
# from robot.input.joystickinput import Joystick


class RobotController():
    def __init__(self, robot):
        self.joystick = None
        self.robot = robot
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.drot = [0, 0, -10]

#         self.keyListener = KeyListener()
        self.startTime = time.time()
        self.trotgait = TrotGait(self.robot)
        self.trotgait.reset()

    def keep_feet_horizontal(self):
        """
        attempts to move feet to horizontal position, using the IMU inputs.
        """
        self.robot.read_imu()
        # print "orientation:", self.orientation
        roll = self.robot.orientation[1]
        pitch = self.robot.orientation[0]
        sin = math.sin(math.radians(pitch))
        # self.move_leg_to_point('front_left', 80, 75, -50 + sin*30)
        # self.move_leg_to_point('front_right', -(80), 75, -50 - sin*30)
        self.robot.move_leg_to_point('front_left', *rotate([60,75,-50],'y',-d2r(roll)))
        self.robot.move_leg_to_point('front_right', *rotate([-60,75,-50],'y',-d2r(roll)))

    def keep_body_horizontal(self):
        """
        Attempts to move feet in order to keep the body horizontal
        """
        self.robot.read_imu()
        roll = self.robot.orientation[1]
        pitch = self.robot.orientation[0]
        sin = math.sin(math.radians(pitch))
        self.robot.move_leg_to_point('front_left', *rotate([0, 75, -50], 'y', d2r(roll)))
        self.robot.move_leg_to_point('front_right', *rotate([0, 75, -50], 'y', d2r(roll)))

    def start(self):
        """
        setup everything before main loop.
        """
        self.robot.start()

    def run(self):
        """
        main thread when running standalo
        :return:
        """
        for i in range(1, 1000):
            self.iterate()

    def trot(self):
        """
        executes a step of the "trot" gait.
        """
        self.trotgait.iterate([self.dx, self.dy, self.dz], self.drot)

    def move_legs_to_offset(self, offset):
        """
        move all legs to the same offset
        """
        self.move_legs_to_offsets(offset, offset, offset, offset)

    def move_legs_to_offsets(self, front_left_offset, front_right_offset, rear_left_offset, rear_right_offset):
        """
        moves each leg to specified offset
        """

        fl_rest, fr_rest, rr_rest, rl_rest = robotData.legs_resting_positions

        self.robot.move_leg_to_point('front_left', *(fl_rest + front_left_offset))
        self.robot.move_leg_to_point('front_right',*(fr_rest + front_right_offset))
        self.robot.move_leg_to_point('rear_left',  *(rl_rest + rear_left_offset))
        self.robot.move_leg_to_point('rear_right', *(rr_rest + rear_right_offset))

    def move_legs_to_angles(self, a, b, c):
        """
        attemprs to move all legs to the same angles [a, b, c] (shoulder, femure, tibia)
        """
        self.robot.move_legs_to_angles([a, b, c])

    def iterate(self):
        """
        runs one iteration of the code, usually called in a loop
        """
        try:
            self.read_joystick()
        except Exception, e:
            try:
                 self.read_keyboard()
            except Exception as e:
                 print("could not read keyboard:", e)

        self.trot()
        self.robot.finish_iteration()
        time.sleep(0.005)

    def read_joystick(self):
    	pass
#         if not self.joystick:
#             raise Exception("no joystick!")
#         self.dx = self.joystick.get_channel("throttle")
#         self.dy = self.joystick.get_channel("yaw")
#
#         if self.joystick.getButton("orientation"):
#             self.drot[0] = self.joystick.get_channel("roll")/300
#             self.drot[1] = self.joystick.get_channel("pitch")/300
#         else:
#             self.drot[2] = self.joystick.get_channel("roll")/200
#         # print self.dx, self.dy, self.drot


    def read_keyboard(self):
    	pass
#         """
#         processed key inputs into dx ,dy, dz, drot values.
#         :return:
#         """
#         if self.keyListener.get_key(119):
#             dx = 1
#         elif self.keyListener.get_key(115):
#             dx = -1
#         else:
#             dx = 0
#         if self.keyListener.get_key(97):
#             dy = 1
#         elif self.keyListener.get_key(100):
#             dy = -1
#         else:
#             dy = 0
#         if self.keyListener.get_key(114):
#             dz = 1
#         elif self.keyListener.get_key(102):
#             dz = -1
#         else:
#             dz = 0
#         if self.keyListener.get_key(116):
#             self.dx = self.dy = self.dz = self.drot[2] = 0
#         if self.keyListener.get_key(113):
#             self.drot[2] += 0.006
#         elif self.keyListener.get_key(101):
#             self.drot[2] -= 0.006
#
#         if self.keyListener.get_key(49):
#             self.robot.disconnect()
#         self.dx += dx
#         self.dy += dy
#         self.dz += dz

def run_with_real_robot():
    """
    used when running things standalone
    """
    from robot.robotInterfaces.realRobot.realRobot import RealRobot
    r = RealRobot()
    controller = RobotController(r)
    controller.start()
    controller.run()


if __name__ == "__main__":
    run_with_real_robot()
