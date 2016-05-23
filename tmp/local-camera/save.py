#!/usr/bin/env python

import cv2

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



def main():

	# Source: 0 - built in camera  1 - USB attached camera
	cap = cv2.VideoCapture(1)

	img_width = 320
	img_height = 240
	ret = cap.set(3,img_width)
	ret = cap.set(4,img_height)

	ret, frame = cap.read()
	h,w,d = frame.shape

	# create a video writer to same images
	sv = SaveVideo('output.mp4v',(w,h))


	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()

		if ret == True:
			#frame = cv2.circle(frame,(147,63), 30, (150,0,0), 1)
			# Our operations on the frame come here
			# for some reason cv2.COLOR_BGR2GRAY seems to crash this
			#hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			#cv2.circle(hsv,(147,63), 30, (50,50,30), -1)

			# Display the resulting frame
			cv2.imshow('frame',frame)
			# sv.write(frame)

		key = cv2.waitKey(10)
		if key == ord('q'):
			break

	# When everything done, release the capture
	cap.release()
	sv.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()
