from __future__ import division
from __future__ import print_function

from math import sin, cos, pi, sqrt, fabs
from math import radians as d2r
import time
from robot import robotData
import numpy as np
import numpy
import math
from robot.tranforms import rotateAroundCenter, distance


class Gait():
	def __init__(self, robot):
		self.lasttime = time.time()
		self.robot = robot

	def height_at_progression(self, prog):
		pass

	def reset(self):
		pass

	def iterate(self, delta, deltaRot):
		pass

def rot_z(t, c):
	"""
	t - theta [radians]
	c - [x,y,z]
	"""
	return [c[0]*cos(t)-c[1]*sin(t), c[0]*sin(t)+c[1]*cos(t), c[2]]


class newTrotGait(Gait):
	phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]
	maxl = 0.2
	minl = 0.1
	E = [0/9, 3/9, 6/9, 9/9, 6/9, 3/9, 0/9, -3/9, -6/9, -9/9, -6/9, -3/9]
	z = [minl, maxl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

	def __init__(self, robot):
		Gait.__init__(self, robot)

		self.legOffset = [0, 6, 3, 9]
		self.legs = [
			robot.legs['front_left'],
			robot.legs['front_right'],
			robot.legs['rear_right'],
			robot.legs['rear_left']
		]
		self.i = 0

	def eachLeg(self, legNum, index, cmd):
		"""
		robot paper
		"""
		phi = self.phi
		offset = self.legOffset
		z = self.z
		E = self.E
		zrot = d2r(float(cmd[2]))

		rests = robotData.legs_resting_positions
		rest = rests[legNum]
		# print('rest[{}]:'.format(legNum), rest)

		i = (index + offset[legNum]) % 12  # len(self.z)

		# get rotation distance: dist = rot_z(angle, rest) - rest
		# this just reduces the function calls and math
		c = cos(zrot)
		s = sin(zrot)
		rot = [
			c*rest[0] - s*rest[1] - rest[0],
			s*rest[0] + c*rest[1] - rest[1],
			0.0  # need this for subtraction
		]

		# rot -= rest  # make rot a delta rotation

		# rot = [0,0]

		# combine delta move and delta rotation (add vectors)
		# delta is the length of the step
		# add together the linear distance and rotation distance
		# FIXME: there needs to be a limit (max length) otherwise you can command too much
		xx = cmd[0] + rot[0]
		yy = cmd[1] + rot[1]

		# create new move command
		move = np.array([
			# xx/2 - phi[i]*xx,
			# yy/2 - phi[i]*yy,
			xx/2 - phi[i]*xx + xx*E[i]/3,
			yy/2 - phi[i]*yy + yy*E[i]/3,
			-rest[2]*z[i]
		])

		# new foot position: newpos = rest + move
		newpos = rest + move

		if legNum in [0]:
			# print('Rot [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, rot[0], rot[1], rot[2]))
			# print('Move [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, move[0], move[1], move[2]))
			print('leg {} Newpos [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(legNum, i, newpos[0], newpos[1], newpos[2]))

		# now move leg/servos
		# self.robot.moveFoot(legNum, newpos)
		# print('newpos[{}]:'.format(legNum), newpos)
		self.legs[legNum].move_to_pos(*newpos)

	def iterate(self, linear_speed, angular_speed):
		"""
		This gets called once then an update to vrep is called, can't do all
		12 steps here
		"""
		cmd = [linear_speed[0], linear_speed[1], angular_speed[2]]
		# frame rotations for each leg
		# frame = [pi/4, -pi/4, -3*pi/4, 3*pi/4]
		# VRep frame is not rotated like mine!!!!!!!!!
		# frame = [0, 0, 0, 0]

		# only calc this 4 times, not 12*4 times!
		# rot_cmd = []
		# for i in range(0, 4):
		# 	rc = rot_z(frame[i], cmd)
		# 	rot_cmd.append(rc)
			# print('cmd[{}]: {:.2f} {:.2f} {:.2f}'.format(i, rc[0], rc[1], rc[2]))

		# for i in range(0, 12):  # iteration, there are 12 steps in gait cycle
		# 	for legNum in [0, 2, 1, 3]:  # order them diagonally
		# 		# rcmd = rot_z(frame[legNum], cmd)
		# 		rcmd = rot_cmd[legNum]
		# 		self.eachLeg(legNum, i, rcmd)  # move each leg appropriately
		# 	# self.eachLeg(0, i, cmd)
		# 	# time.sleep(0.05)  # 20 Hz, not sure of value
		# 	# time.sleep(0.5)
		i = self.i
		for legNum in [0, 2, 1, 3]:  # order them diagonally
			# rcmd = rot_z(frame[legNum], cmd)
			# rcmd = rot_cmd[legNum]
			rcmd = cmd
			self.eachLeg(legNum, i, rcmd)  # move each leg appropriately
		self.i = (i + 1)%12
		# time.sleep(0.25)
		# time.sleep(0.25)

##########################################################################
##########################################################################

class TrotGait(Gait):

	# z_profile = [0, 0, 0, 0, 0, 10, 40, 40, 30, 7] #leg height x time

	phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]
	maxl = 0.50
	minl = 0.25
	z = [minl, maxl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

	def __init__(self, robot):
		Gait.__init__(self, robot)
		# self.z_profile.append(self.z_profile[0])
		# self.robot = robot
		# self.legs = robot.legs
		# self.group1 = [self.legs["front_left"], self.legs["rear_right"]]
		# self.group2 = [self.legs["front_right"], self.legs["rear_left"]]

		self.legOffset = [0, 6, 3, 9]
		self.legs = [
			robot.legs['front_left'],
			robot.legs['front_right'],
			robot.legs['rear_right'],
			robot.legs['rear_left']
		]
		self.i = 0


	def eachLeg(self, legNum, index, cmd):
		"""
		robot paper
		"""
		phi = self.phi
		offset = self.legOffset
		z = self.z
		# offset = [0, 6, 3, 9]
		# phi = [9/9, 6/9, 3/9, 0/9, 1/9, 2/9, 3/9, 4/9, 5/9, 6/9, 7/9, 8/9]
		# # z = [minl, maxl, maxl, minl, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
		# z = [minl, maxl, maxl, minl, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		# delta = sqrt(cmd[0]**2 + cmd[1]**2)
		zrot = d2r(float(cmd[2]))
		# rest = self.robot.getFoot0(legNum)
		rests = robotData.legs_resting_positions
		rest = rests[legNum]
		print('rest[{}]:'.format(legNum), rest)

		i = (index + offset[legNum]) % 12  # len(self.z)
		c = cos(zrot)
		s = sin(zrot)
		rot = np.array([
			c*rest[0]-s*rest[1],
			s*rest[0]+c*rest[1],
			rest[2]  # need this for subtraction
		])

		rot -= rest  # make rot a delta rotation

		# combine delta move and delta rotation (add vectors)
		xx = cmd[0] + rot[0]
		yy = cmd[1] + rot[1]
		move = np.array([
			xx - 2*phi[i]*xx,
			yy - 2*phi[i]*yy,
			-rest[2]*z[i]
		])
		newpos = rest + move

		# if legNum in [0]:
			# print('Rot [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, rot[0], rot[1], rot[2]))
			# print('Move [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(i, move[0], move[1], move[2]))
			# print('leg {} Newpos [{}](x,y,z): {:.2f}\t{:.2f}\t{:.2f}'.format(legNum, i, newpos[0], newpos[1], newpos[2]))

		# now move leg/servos
		# self.robot.moveFoot(legNum, newpos)
		print('newpos[{}]:'.format(legNum), newpos)
		self.legs[legNum].move_to_pos(*newpos)

	# def height_at_progression(self, prog):
	#	 """
	#	 returns the foot height at prog[0-1] of the foot movement overall
	#	 """
	#	 index = math.floor(prog*self.z_points)
	#	 diff = prog * self.z_points - index
	#	 value = self.z_profile[int(index)] + (self.z_profile[int(index+1)] - self.z_profile[int(index)])*diff
	#
	#	 prog = (prog if prog <= 0.5 else 1-prog)
	#	 speed = -0.5+ ( prog * 2)
	#
	#	 return value, speed


	def iterate(self, linear_speed, angular_speed):
		"""
		This gets called once then an update to vrep is called, can't do all
		12 steps here
		"""
		cmd = [linear_speed[0], linear_speed[1], angular_speed[2]]
		# frame rotations for each leg
		# frame = [pi/4, -pi/4, -3*pi/4, 3*pi/4]
		# VRep frame is not rotated like mine!!!!!!!!!
		frame = [0, 0, 0, 0]

		# only calc this 4 times, not 12*4 times!
		rot_cmd = []
		for i in range(0, 4):
			rc = rot_z(frame[i], cmd)
			rot_cmd.append(rc)
			# print('cmd[{}]: {:.2f} {:.2f} {:.2f}'.format(i, rc[0], rc[1], rc[2]))

		# for i in range(0, 12):  # iteration, there are 12 steps in gait cycle
		# 	for legNum in [0, 2, 1, 3]:  # order them diagonally
		# 		# rcmd = rot_z(frame[legNum], cmd)
		# 		rcmd = rot_cmd[legNum]
		# 		self.eachLeg(legNum, i, rcmd)  # move each leg appropriately
		# 	# self.eachLeg(0, i, cmd)
		# 	# time.sleep(0.05)  # 20 Hz, not sure of value
		# 	# time.sleep(0.5)
		i = self.i
		for legNum in [0, 2, 1, 3]:  # order them diagonally
			# rcmd = rot_z(frame[legNum], cmd)
			rcmd = rot_cmd[legNum]
			self.eachLeg(legNum, i, rcmd)  # move each leg appropriately
		self.i = (i + 1)%12
		# time.sleep(1)
		# time.sleep(0.25)




class TrotGait2(Gait):

	 z_profile = [0, 0, 0, 0, 0, 10, 40, 40, 30, 7] #leg height x time

	 z_points = len(z_profile)
	 startTime = 0
	 stepDistance = 5000
	 lastDelta = numpy.array([0, 0, 0])
	 currentDistance = 0

	 def __init__(self, robot):
		 Gait.__init__(self, robot)
		 self.z_profile.append(self.z_profile[0])
		 self.robot = robot
		 self.legs = robot.legs
		 self.group1 = [self.legs["front_left"], self.legs["rear_right"]]
		 self.group2 = [self.legs["front_right"], self.legs["rear_left"]]


	 def height_at_progression(self, prog):
		 """
		 returns the foot height at prog[0-1] of the foot movement overall
		 """
		 index = math.floor(prog*self.z_points)
		 diff = prog * self.z_points - index
		 value = self.z_profile[int(index)] + (self.z_profile[int(index+1)] - self.z_profile[int(index)])*diff

		 prog = (prog if prog <= 0.5 else 1-prog)
		 speed = -0.5+ ( prog * 2)

		 return value, speed

	 def iterate(self, linear_speed, angular_speed):
		 """
		 do all the calculation to move feet to next location
		 """
		 rests = robotData.legs_resting_positions
		 rotationalDistance = distance(rests[0], rotateAroundCenter(rests[0], 'z', angular_speed[2]))
		 thisDistance = math.sqrt(linear_speed[0]**2 + linear_speed[1]**2 + linear_speed[2]**2) + rotationalDistance
		 self.currentDistance = (self.currentDistance + thisDistance) % self.stepDistance

		 #### current feet height depends on distance (maybe shoudl depend on time? )
		 step_progression = self.currentDistance / self.stepDistance
		 step_progression_alternate = (step_progression + 0.5) % 1.0

		 height_pair1, speed_direction_pair1 = self.height_at_progression(step_progression)
		 height_pair2, speed_direction_pair2 = self.height_at_progression(step_progression_alternate)

		 for leg in self.group1:
			 angular_offset = rotateAroundCenter(leg.resting_position, 'z', angular_speed[2]) - leg.resting_position
			 total_offset = angular_offset - linear_speed
			 offset = speed_direction_pair1*total_offset
			 offset[2] = height_pair1
			 rotated_position = self.get_rotated_leg_resting_positions(leg,angular_speed)
			 leg.move_to_pos(*(rotated_position + offset))

		 for leg in self.group2:
			 angular_offset = rotateAroundCenter(leg.resting_position, 'z', angular_speed[2]) - leg.resting_position
			 total_offset = angular_offset - linear_speed
			 offset = speed_direction_pair2*total_offset
			 offset[2] = height_pair2
			 rotated_position = self.get_rotated_leg_resting_positions(leg,angular_speed)
			 leg.move_to_pos(*(rotated_position + offset))


		 #print time.time()

	 def get_rotated_leg_resting_positions(self,leg,drot):
		 rotx = rotateAroundCenter(leg.resting_position,"x",drot[0])
		 return rotateAroundCenter(rotx,"y",drot[1])
