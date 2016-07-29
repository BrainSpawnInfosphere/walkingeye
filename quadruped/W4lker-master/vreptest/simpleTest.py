#!/usr/bin/env python
# Copyright 2006-2014 Coppelia Robotics GmbH. All rights reserved. 
# marc@coppeliarobotics.com
# www.coppeliarobotics.com
# 
# -------------------------------------------------------------------
# THIS FILE IS DISTRIBUTED "AS IS", WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY. THE USER WILL USE IT AT HIS/HER OWN RISK. THE ORIGINAL
# AUTHORS AND COPPELIA ROBOTICS GMBH WILL NOT BE LIABLE FOR DATA LOSS,
# DAMAGES, LOSS OF PROFITS OR ANY OTHER KIND OF LOSS WHILE USING OR
# MISUSING THIS SOFTWARE.
# 
# You are free to use/modify/distribute this file for whatever purpose!
# -------------------------------------------------------------------
#
# This file was automatically created for V-REP release V3.2.0 on Feb. 3rd 2015

# Make sure to have the server side running in V-REP: 
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

import vrep

def getChildren(object,clientID):
    children = []
    index = 0
    child = None
    while child != -1:
        child = vrep.simxGetObjectChild(clientID,object,index,vrep.simx_opmode_oneshot_wait)
        if child != -1:
            children.append(child)
    return children

print('Program started')
vrep.simxFinish(-1)  # just in case, close all opened connections
clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)
if clientID != -1:
    print('Connected to remote API server')
    # res, objs = vrep.simxGetObjects(clientID, vrep.sim_handle_all, vrep.simx_opmode_oneshot_wait)
    # if res == vrep.simx_return_ok:
    #     print('Number of objects in the scene: ', len(objs))
    # else:
    #     print('Remote API function call returned with error code: ', res)

    errorCode, handles, intData, floatData, array = vrep.simxGetObjectGroupData(clientID,vrep.sim_appobj_object_type,0,vrep.simx_opmode_oneshot_wait)

    data = dict(zip(array, handles))

    joints = {}
    for name in data:
        if "joint" in name:
            joints[name] = data[name]
    print joints

    fl_leg = dict((key,value) for key, value in data.iteritems() if "fl" in key)
    fr_leg = dict((key,value) for key, value in data.iteritems() if "fr" in key)
    rr_leg = dict((key,value) for key, value in data.iteritems() if "rr" in key)
    rl_leg = dict((key,value) for key, value in data.iteritems() if "rl" in key)


    vrep.simxFinish(clientID);
else:
    print('Failed connecting to remote API server')
print('Program ended')
