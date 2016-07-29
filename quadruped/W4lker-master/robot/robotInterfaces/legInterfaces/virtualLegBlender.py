from robot.robotInterfaces.legInterfaces.genericLeg import Leg
import bge

source = bge.logic.getCurrentScene().objects

class VirtualLegBlender(Leg):
    """
    Virtual Leg implementation for use with blender game engine.
    """
    def __init__(self, name, position, resting_position):
        Leg.__init__(self, name, position, resting_position)
        self.armature = source.get("armature")
        
        self.channels = []
        for channel in self.armature.channels:
            if self.name in str(channel):
                self.channels.append(channel)
        self.direction = -1 if "right" in self.name else 1


    def move_to_angle(self, shoulderAngle, femurAngle, tibiaAngle):
        """
        Move legs joints to the specified angles, in radians.
        """
        self.check_limits(shoulderAngle,femurAngle,tibiaAngle)
        shoulder = self.armature.channels[0]
        shoulder.rotation_mode = bge.logic.ROT_MODE_XYZ
        shoulder.rotation_euler = (0, -shoulderAngle, 0)

        femur = self.armature.channels[2]
        femur.rotation_mode = bge.logic.ROT_MODE_XYZ
        femur.rotation_euler = (-femurAngle, 0, 0)

        tibia = self.armature.channels[3]
        tibia.rotation_mode = bge.logic.ROT_MODE_XYZ
        tibia.rotation_euler = (0, 0, -tibiaAngle*self.direction)

        self.armature.update()

