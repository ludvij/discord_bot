import cv2
from sys import argv
import os

# Extracts frames from videos
# made a generator to not clutter dirs in images
# a frame is extracted a image is processed
def frame_capture(path):
	# path to the video
	vid = cv2.VideoCapture(path)
	# frame counter
	count = 0
	# checks wheter frames where extracted
	has_frame, frame = vid.read()
	while has_frame:
		# saves the frames
		path = fr"rcs\img\frames\frame{count}.jpg"
		saved = cv2.imwrite(path, frame)
		# extracts the frames
		has_frame, frame = vid.read()
		count += 1
		yield has_frame

def main():
	frame = frame_capture(argv[1])
	has_frame = True
	while has_frame:
		has_frame = next(frame, False)


if __name__=='__main__':
	main()