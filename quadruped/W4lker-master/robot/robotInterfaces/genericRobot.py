__author__ = 'will'
import abc

class Robot(object):
    __metaclass__ = abc.ABCMeta
    legs = []
    orientation = [0, 0, 0]

    @abc.abstractmethod
    def load_legs(self):
        """
        Start the legs, init code
        """

    @abc.abstractmethod
    def read_feet(self):
        """
        return array of feet sensor values
        :return:
        """

    @abc.abstractmethod
    def read_imu(self):
        """
        returns orientation array
        :return:
        """

    @abc.abstractmethod
    def move_legs_to_angles(self, angles):
        pass

    @abc.abstractmethod
    def move_leg_to_point(self, leg, x, y, z):
        """
        move legs to absolute point
        :param leg: leg name
        :param x: body relative x pos
        :param y: body relative y pos
        :param z: body relative z pos
        :return:
        """

    def finish_iteration(self):
        pass

    def start(self):
        pass


