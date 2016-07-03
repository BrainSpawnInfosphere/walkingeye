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


lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )


class OpticalFlow:
	def __init__(self):
		self.track_len = 10
		self.detect_interval = 5
		self.tracks = []
		self.frame_idx = 0

	"""
	in: gray image
	out: none
	"""
	def initOldFrame(self,frame):
		self.prev_gray = frame


	"""
	p0 - points from last picture that we are tracking
	p1 - points found in new image we are tracking
	in: gray image
	out:
	"""
	def calc(self,frame_gray):
		vis = frame_gray.copy()

		if len(self.tracks) > 0:
			img0, img1 = self.prev_gray, frame_gray
			p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
			p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
			p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
			d = abs(p0-p0r).reshape(-1, 2).max(-1)
			good = d < 1
			new_tracks = []
			for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
				if not good_flag:
					continue
				tr.append((x, y))
				if len(tr) > self.track_len:
					del tr[0]
				new_tracks.append(tr)
				cv2.circle(vis, (x, y), 2, (0, 255, 0), -1)
			self.tracks = new_tracks
			cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))
			#draw_str(vis, (20, 20), 'track count: %d' % len(self.tracks))
			print 'track count: {0:d}'.format(len(self.tracks))

		if self.frame_idx % self.detect_interval == 0:
			mask = np.zeros_like(frame_gray)
			mask[:] = 255
			for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
				cv2.circle(mask, (x, y), 5, 0, -1)
			p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
			if p is not None:
				for x, y in np.float32(p).reshape(-1, 2):
					self.tracks.append([(x, y)])


		self.frame_idx += 1
		self.prev_gray = frame_gray

		return vis


def main():

	# Source: 0 - built in camera  1 - USB attached camera
	#cap = cv2.VideoCapture('output.mp4v')
	cap = cv2.VideoCapture(1)

	save = False
	loop_video = True

	ret, frame = cap.read()
	h,w,d = frame.shape

	of = OpticalFlow()
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	of.initOldFrame(gray)

	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()

		if ret == True:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

			flow = of.calc(gray.copy())

			# Display the resulting frame
			cv2.imshow('frame2',flow)

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
		elif (key & 0xFF) == 27: #Esc
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':
	main()
	print 'bye ...'
