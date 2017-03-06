# Software

Simple layout of the code:

- Quadruped:
	- Engine({serial})
	- I2C()
	- IR()
	- movement_states['walk', 'climb', 'animate', 'sit', 'stand']
		- these are used to call movements[] functions using command()
	- movements[]
		- Gait:
			- command(x, func_move_foot) - moves all feet through 1 gait cycle (12 steps)
			- eachLeg(x,y,z)
		- Pose:
			- command(func_move_foot) - sends all feet through an animation sequence to final position
			- eachLeg(x,y,z)

- Engine({serial}): - handles movement hardware
	- legs[4]
		- servos[3]
			- angle
			- setServoLimits()
			- bulkWrite() - change to sync
		- coxa, femur, tibia
		- fk()
		- ik()
		- moveFoot(x,y,z)
		- moveFootAngle(a,b,c)
	- moveFoot(x,y,z) - gaits need a function to call
