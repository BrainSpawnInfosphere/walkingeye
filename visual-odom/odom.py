#! /usr/bin/env python

import numpy as np
import cv2
import argparse
import video
import time
import math

if 0:
    def draw(pts):
        a=1

    def drawKeyPoints(im,keypoints):
        # im2 = cv2.drawKeypoints(im,keypoints,im,color=(255,0,0))
        # cv2.imshow('keypoints',im2)
        # cv2.waitKey(10)

        im2 = im.copy()
        for i in keypoints:
            # print i
            cv2.circle(im2,(int(i[0][0]),int(i[0][1])),3,(0,255,0),-1)
        cv2.imshow('keypoints',im2)
        cv2.waitKey(10)

else:
    import matplotlib.pyplot as plt

    plt.ion()
    plt.show()
    # plt.title('image'), plt.xticks([]), plt.yticks([])
    # plt.axis("off")

    def drawKeyPoints(im,keypoints):
        a=1

    def draw(pts):
        x = []
        y = []
        z = []
        for i in pts:
            x.append(i[0])
            y.append(i[1])
            z.append(i[2])

        # li.set_ydata(y)
        # li.set_xdata(x)
        # fig.canvas.draw()
        plt.subplot(2,1,1)
        plt.plot(x,y)
        # plt.axis([0, 6, 0, 20])
        plt.grid(True)
        plt.ylabel('y')
        plt.xlabel('x')
        # plt.draw()
        # plt.pause(15)

        plt.subplot(2,1,2)
        yy = np.linspace(0,1,len(z))
        # plt.clf()
        plt.plot(yy,z)
        plt.grid(True)
        plt.ylabel('z')

        plt.draw()
        plt.pause(25)
        # time.sleep(5)

def featureDetection(im):
    # Initiate FAST object with default values
    # fast = cv2.FastFeatureDetector_create(20,True)
    # fast = cv2.FastFeatureDetector_create()
    # fast.setNonmaxSuppression(True)
    # fast.setThreshold(20)
    # # find and draw the keypoints
    # keypoints = fast.detect(im)
    # keypoints=np.array([[k.pt] for k in keypoints],dtype='f4')
    # print 'fast keypoints',keypoints.shape

    # orb = cv2.ORB_create()
    # keypoints = orb.detect(im,None)
    # keypoints=np.array([[k.pt] for k in keypoints],dtype='f4')
    # print 'orb shape',keypoints.shape

    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 500,
        qualityLevel = 0.3,
        minDistance = 7,
        blockSize = 7 )
    keypoints = cv2.goodFeaturesToTrack(im, mask = None, **feature_params)
    print 'goodFeaturesToTrack shape',keypoints.shape

    return keypoints

def cullBadPts(p0,p1,st,err):
    new = []
    old = []

    # print 'st',st
    # print 'err',err
    # print 'p1',p1
    # print 'p0',p0
    # exit()

    # Select good points
    for i in range(0,p1.shape[0]):
        # print 'st',st[i]
        # print 'p1',p1[i]
        if st[i][0] == 1 and p1[i][0][0] >= 0 and p1[i][0][1] >= 0:
            new.append(p1[i][0])
            old.append(p0[i][0])

    good_new = np.array([[k] for k in new],dtype=np.float32)
    good_old = np.array([[k] for k in old],dtype=np.float32)

    return good_old, good_new


def featureTrack(new_gray,old_gray,p0):
    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (10,10),
                  maxLevel = 3,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, new_gray, p0, None, **lk_params)

    p0,p1 = cullBadPts(p0,p1,st,err)

    return p0, p1


###############################################################################

cam = video.Camera('floor.mp4')
cam.setROI((0,479,210,639))
# cam.load('camera_params.npz')
# cameraMat = cam.data['camera_matrix']


pp = (240,220)
focal = 200.0
R_f = np.eye(3,3,dtype=np.float)
t_f = np.array([0,0,0],dtype=np.float)
# R = np.zeros((3,3),dtype=np.float)
R = R_f.copy()
t = np.array([0,0,0],dtype=np.float)
t_prev = t.copy()
dist = 0.0

# cv2.IMREAD_GRAYSCALE faster?
ret, old_im = cam.read(True)
ret, im = cam.read(True)
p0 = featureDetection(old_im)
# p0, p1 = featureTrack(im,old_im,p0)
# E, mask = cv2.findEssentialMat(p0,p1,focal,pp,cv2.FM_RANSAC, 0.999, 1.0)
# retval, R, t, mask = cv2.recoverPose(E,p0,p1,R,t,focal,pp,mask)

save_pts = []
while(cam.isOpened()):
    try:
        ret, im = cam.read(True)

        # end of video
        if not ret:
            print 'video end'
            draw(save_pts)
            break

        # Not enough old points, p0
        if p0.shape[0] < 50:
            print '------- reset --------'
            p0 = featureDetection(im)
            if p0.shape[0] == 0:
                print 'bad image'
                continue

        # p0 - old pts
        # p1 - new pts
        p0, p1 = featureTrack(im,old_im,p0)

        # not enough new points p1
        if p1.shape[0] < 50:
            print '------- reset p1 --------'
            continue

        drawKeyPoints(im,p1)

        # since these are rectified images, fundatmental (F) = essential (E)
        # E, mask = cv2.findEssentialMat(p0,p1,focal,pp,cv2.FM_RANSAC)
        # retval, R, t, mask = cv2.recoverPose(E,p0,p1,R_f,t_f,focal,pp,mask)

        E, mask = cv2.findEssentialMat(p0,p1,focal,pp,cv2.FM_RANSAC, 0.999, 1.0)
        retval, R, t, mask = cv2.recoverPose(E,p0,p1,R,t,focal,pp,mask)
        # print retval,R

        # Now update the previous frame and previous points
        old_im = im.copy()
        # p0 = p1.reshape(-1,1,2)
        p0 = p1

        # print 'p0 size',p0.shape
        # print 'p1 size',p1.shape
        # print 't',t
        # dt = t - t_prev
        # scale = np.linalg.norm(dt)
        # print scale
        scale = 1.0

        R_f = R.dot(R_f)
        # t_f = t
        t_f = t_f + scale*R_f.dot(t)

        # t_prev = t
        # t_f = t_f/t_f[2]
        # dist += np.linalg.norm(t_f[:2])

        # num = np.array([t_f[0]/t_f[2],t_f[1]/t_f[2]])
        # num = t_f
        # print 'position:', t_f
        # print 'distance:', dist
        # R_f = R*R_f
        # print 'R:',R_f,'t:',t_f
        # print t_f

        save_pts.append(t_f)
        # save_pts.append(t_f[:2])

    except KeyboardInterrupt:
        print 'captured interrupt'
        break

cam.release()
