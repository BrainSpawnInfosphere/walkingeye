# Software

**Issue:** Anything that has opencv in it *can't* be derived from `process`, opencv
crashes. It has to be in it's own python script *or* be derived from `object`.

Simple layout of the code:

- ImageServer:
	- allows image processing to be done off-board
		- allows commands to also come from a completely different type of input
		(joystick) without robot modification
	- grabs image
	- searches for:
		- tennis ball
		- people's faces
	- publishes:
		- images
		- commands to robot

- Audio:
	- listen for speach
	- convert to wave format
	- send to service (wit or whatever)
	- 

- Quadruped:
	- Engine({serial})
	- AHRS() - compass
	- MCP3208() - ADC for IR and whatever else
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
