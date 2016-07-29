__author__ = 'will'

from math import radians as d2r
from math import *
import scipy.optimize as opt

def ik_solver(x, y, z):

    def forward_ik(args):
        shoulder, femur, tibia = args
        pos0 = [0, 0]
        femurLength = 50
        tibiaLength = 50

        femur = femur
        sinShoulder = sin(shoulder)
        cosShoulder = cos(shoulder)
        pos1 = [pos0[0] + cos(femur) * femurLength,
                pos0[1] + sin(femur) * femurLength, ]


        pos2 = [pos1[0] + cos(femur - (pi - tibia)) * tibiaLength,
                pos1[1] + sin(femur - (pi - tibia)) * tibiaLength, ]

        # print pos1, pos2
        #
        # pos1 = [pos1[0]*sinShoulder,
        #         pos1[0]*cosShoulder,
        #         pos1[1]]

        pos2 = [pos2[0]*sinShoulder,
                pos2[0]*cosShoulder,
                 pos2[1]]
        return pos2

    def error(args):
        x2,y2,z2 = forward_ik(args)
        return sqrt((x2-x)**2 +(y2-y)**2 +(z2-z)**2)

    return opt.fmin_slsqp(func=error,
            x0=[0,0,pi/2],
            bounds=[(-pi/2,pi/2),(-pi/2,pi/2),(0,pi)],
            iprint=2,
            acc=0.1)


print ik_solver(0,0,100)


    #
    # def ik_to2(self, x, y, z):
    #
    #     def triangle_angle(a, b, c):
    #         if c == 0:
    #             return 0
    #         a = abs(a)
    #         b = abs(b)
    #         c = abs(c)
    #
    #         cosA = (a ** 2 - b ** 2 - c ** 2) / (-2 * b * c)
    #         # print "triangle:",a,b,c , " cos: ", cos
    #         return math.acos(cosA)
    #
    #
    #     maxsize = self.femurLength + self.tibiaLength
    #     dx = dy = dz = 0
    #     coords = [x, y, z]
    #     if 'max' in coords or 'min' in coords:
    #         limit = 'max' if 'max' in coords else 'min'
    #         coords[coords.index(limit)] = 0
    #         length = None
    #         while not length or length < maxsize:
    #             coords[coords.index(limit)] += (1 if limit == 'max' else -1)
    #             dx, dy, dz = [coords[i] - self.position[i] for i in range(3)]
    #             length = (math.sqrt(dx ** 2 + dy ** 2 + dz ** 2) > self.femurLength + self.tibiaLength)
    #
    #     else:
    #         dx = float(x) - self.position[0]
    #         dy = float(y) - self.position[1]
    #         dz = float(z) - self.position[2]
    #
    #     while (math.sqrt(dx ** 2 + dy ** 2 + dz ** 2) > self.femurLength + self.tibiaLength):
    #         dx *= 0.995
    #         dy *= 0.995
    #         dz *= 0.995
    #
    #     distxyz = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)  # total distance
    #
    #     tibiaAngle = triangle_angle(distxyz, self.tibiaLength, self.femurLength)
    #
    #     xydist = math.sqrt(dx ** 2 + dy ** 2)
    #
    #     dist_vectorAngle = math.atan2(dz, xydist)
    #
    #     if "right" in self.name:
    #         if dx < 0:
    #             dist_vectorAngle = pi - dist_vectorAngle
    #
    #
    #
    #     # relevant, shoulder tilt angle
    #     AbsshoulderTiltAngle = triangle_angle(self.tibiaLength, self.femurLength, distxyz) + dist_vectorAngle
    #     AbsshoulderTiltAngle = math.degrees(AbsshoulderTiltAngle)
    #
    #     try:
    #         AbsshoulderPanAngle = math.degrees(math.atan(dy/dx))
    #     except:
    #         AbsshoulderPanAngle = pi/2
    #
    #     tibiaAngle = math.degrees(tibiaAngle)
    #
    #     if "right" in self.name:
    #
    #         AbsshoulderPanAngle = -AbsshoulderPanAngle
    #         print("dist_vector_angle:", r2d(dist_vectorAngle), dx, self.position[1], xydist)
    #
    #     # pos0 = [0, 0]
    #     # pos1 = [math.cos(math.radians(AbsshoulderTiltAngle)) * self.femurLength,
    #     #         math.sin(math.radians(AbsshoulderTiltAngle)) * self.femurLength, ]
    #     #
    #     # pos2 = [pos1[0] + math.cos(math.radians(AbsshoulderTiltAngle - (180 - tibiaAngle))) * self.tibiaLength,
    #     #         pos1[1] + math.sin(math.radians(AbsshoulderTiltAngle - (180 - tibiaAngle))) * self.tibiaLength, ]
    #     # viewer.update_lines([pos0, pos1, pos2])
    #     # print(AbsshoulderPanAngle, AbsshoulderTiltAngle, tibiaAngle)
    #     return AbsshoulderPanAngle, AbsshoulderTiltAngle, tibiaAngle - 90



def forward_ik(args):
    shoulder, femur, tibia = args

    #YZ plane first
    pos0 = [leg_root_y,leg_root_z]

    ## calculate with positive x
    pos0[1]*= self.direction
    shoulder = shoulder * self.direction
    ###
    femurLength = 46
    tibiaLength = 92

    pos1 = [cos(femur) * femurLength,
            sin(femur) * femurLength, ]

    pos2 = [pos1[0] + cos(femur - (pi - tibia)) * tibiaLength,
            pos1[1] + sin(femur - (pi - tibia)) * tibiaLength, ]

    pos2 = [pos0[0] + pos2[0]*sin(shoulder),
            pos0[1] + pos2[0]*cos(shoulder),
            self.position[2] + pos2[3dof1]]
    #print("pos2:", pos2, pos1)
    return pos2


    def ik_to3(self, x, y, z):

        y = y * self.direction

        import scipy.optimize as opt

        def error(args):
            x2,y2,z2 = forward_ik(args)
            return sqrt((x2-x)**2 +(y2-y)**2 +(z2-z)**2)

        result = opt.fmin_slsqp(func=error,
                x0=[0,0,pi/2],
                bounds=[(-pi/2,pi/2),(-pi/2,pi/2),(0,pi)],
                iprint=0,
                acc=0.01)

        print (self.name, forward_ik(result))
        return result

