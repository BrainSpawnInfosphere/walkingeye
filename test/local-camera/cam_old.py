#!/usr/bin/env python
#
# This so doesn't work right :P




import cv2
import numpy as np

"""
Simple class to save frames to video (mp4v)
"""
class SaveVideo:
	def __init__(self,fn,image_size,fps=20):
		mpg4 = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
		self.out = cv2.VideoWriter()
		self.out.open(fn,mpg4,fps, image_size)
		
	def write(self,image):
		self.out.write(image)
	
	def release(self):
		self.out.release()

def writeMsg(frame,msg):
	font = cv2.FONT_HERSHEY_SIMPLEX
	font_scale = 1
	font_color = (155,0,0)
	cv2.putText(frame, 'OpenCV',(100,100),font,font_scale,font_color,2)



class OpticalFlow:
	def __init__(self):
		# params for ShiTomasi corner detection
		self.feature_params = dict( maxCorners = 100,
							   qualityLevel = 0.3,
							   minDistance = 7,
							   blockSize = 7 )
		
		# Parameters for lucas kanade optical flow
		self.lk_params = dict( winSize  = (15,15),
						  maxLevel = 2,
						  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
	"""
	in: gray image
	out: none
	"""
	def initOldFrame(self,frame):
		h,w = frame.shape
		self.oldFrame = frame
		self.p0 = cv2.goodFeaturesToTrack(frame, mask = None, **self.feature_params)
		#self.p0 = cv2.goodFeaturesToTrack(frame, mask = None, **self.feature_params)
	
	"""
	p0 - points from last picture that we are tracking
	p1 - points found in new image we are tracking
	in: gray image
	out:
	"""
	def calc(self,frame):
		h,w = frame.shape
		
		roi = frame
		roi_old = self.oldFrame
		
		# Create a mask image for drawing purposes
		mask = np.zeros_like(frame)
		
        #flow = cv2.calcOpticalFlowFarneback(self.oldFrame, frame, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        
		# calculate optical flow for the bottom half of the image
		p1, st, err = cv2.calcOpticalFlowPyrLK(roi_old, roi, self.p0, None, **self.lk_params)
		#p1, st, err = cv2.calcOpticalFlowPyrLK(self.oldFrame, frame, self.p0, None, **self.lk_params)
		
		#print '>>',p1
		#print '>>',p1,st,err
		
		#if p1 == None:
		#	print 'p1 == 0'
		#	return -1
		
		# Select good points based on status from above
		good_new = p1[st==1]
		good_old = self.p0[st==1]
		
		color = np.random.randint(0,255,(100,3))
		
		# draw the tracks
		for i,(new,old) in enumerate(zip(good_new,good_old)):
			a,b = new.ravel()
			c,d = old.ravel()
			mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
			frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
		
		img = cv2.add(frame,mask)
		#cv2.imshow('img',img)
		
		#end -- clean up
		# if there are not enough points to track, then get more
		if len(self.p0) < 10:
			self.initOldFrame(frame.copy())
		else:
			self.oldFrame = frame.copy()
			self.p0 = good_new.reshape(-1,1,2)
		
		return img

# CV_CAP_PROP_POS_FRAMES = 28

def main():
	
	# Source: 0 - built in camera  1 - USB attached camera
	#cap = cv2.VideoCapture('output.mp4v')
	cap = cv2.VideoCapture(1)
	
	save = False
	loop_video = False
	
	ret, frame = cap.read()
	h,w,d = frame.shape
	
	# create a video writer to same images
	#sv = SaveVideo('output.mp4v',(w,h))
	
	of = OpticalFlow()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
	of.initOldFrame(gray[h/2:h,0:w])
	
# none of these work	
# 	cap.set(28,0.5)
# 	print 'focus:',cap.get(28) #CV_CAP_PROP_FOCUS
# 	print 'fps:',cap.get(5) #CV_CAP_PROP_FPS
# 	print 'gain:',cap.get(14)
# 	print 'autoexposure:',cap.get(21)
	
	while(True):
		# Capture frame-by-frame 
		ret, frame = cap.read()
		
		if ret == True:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
			
			half = gray[h/2:h,0:w]
			flow = of.calc(half.copy())
			
			# Display the resulting frame
			cv2.imshow('frame1',half)
			cv2.imshow('frame2',flow)
	
			
			#if save:
			#	sv.write(frame)
			
		elif (ret == False) and (loop_video): 
			print 'loop reset'
			cap.set(1,0) # CV_CAP_PROP_POS_FRAMES
			pass
		
		elif ret == False:
			print 'could not read video'
			break
		
		key = cv2.waitKey(10)
		if key == ord('q'):
			break
		#elif key == ord('s'):
		#	save = not save
		
	# When everything done, release the capture
	cap.release()
	#sv.release()
	cv2.destroyAllWindows() 


if __name__ == '__main__':
	main()
	print 'bye ...'
