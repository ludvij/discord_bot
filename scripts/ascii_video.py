from sys import argv
import cv2
from PIL import Image
import numpy as np
import os

# Extracts frames from videos
# made a generator to not clutter dirs in images
# a frame is extracted a image is processed
def frame_capture(path, out_path):
	# path to the video
	vid = cv2.VideoCapture(path)
	# checks wheter frames where extracted
	has_frame, frame = vid.read()
	while has_frame:
		# saves the frames
		saved = cv2.imwrite(out_path, frame)
		# extracts the frames
		has_frame, frame = vid.read()
		yield has_frame


# size should be 60x60
def convert_to_ascii(path, pwidth=None, pheight=None, reverse=False):
	# open image and convert it to gray scale
	img = Image.open(path).convert("L")

	# if size is provide it will be resized to pwidth x pwidth / ratio
	# resize image to something more manageable ratio is used to respect img ratio
	if pheight != None and pwidth != None: 
		img = img.resize((pwidth, pheight))
	elif pwidth != None:
		ratio = img.size[0] / img.size[1]
		img = img.resize((pwidth, int(pwidth / ratio)))
	elif pheight != None:
		ratio = img.size[0] / img.size[1]
		img = img.resize((int(pheight * ratio), pheight))

	width, height = img.size

	# since pixels in gray scale go from 0 to 255 we have to divide
	# in ranges to get the best char
	# so we have to darkness * len(chars) - 1 / 255  to get the best index
	# so if we have 10 chars and we have to convert a pixel of value 67 we
	# divide 9 / 255 to get 0.035 and the we mult 67 * 0.035 and we get 2.36
	# so we truncate it to 2, so the char would be ":"
	# since this operation is length dependant we can add whatever char we like 
	# and it will be added to its range, a char hue if you like
	chars = " .,_-~=+*:;!?#%@"
	if reverse: chars = chars[::-1]
	# store to ease computations
	divisor = (len(chars) - 1) / 255

	# numpy arrays are a pain to work with, but fast
	# for some reason its transposed (I know why but still a pain)
	arr = np.chararray((height, width))

	# iterate through each pixel and assign each char
	for i in range(width):
		for j in range(height):
			px = img.getpixel((i,j))
			index = int(px * divisor)
			#print(px, index)
			arr[j, i] = chars[index]	

	# np char arrays are encoded by defautl, so if you want a nice printable output you
	# have to do this
	printable_arr = "\n".join([''.join(row) for row in arr.decode('utf-8')])

	return printable_arr

def main():
	out_path = r"rcs\img\frame.jpg"
	continue_loop = False
	loop = True
	if (len(argv) > 3 and argv[3] == '-l'):
		continue_loop = True
	while loop:
		frame = frame_capture(argv[1], out_path)
		has_frame = True
		while has_frame:
			has_frame = next(frame, False)

			res = convert_to_ascii(out_path, pwidth=int(argv[2]))
			print(f'\033[H{res}')
			os.remove(out_path)
			
		if continue_loop:
			loop = True
		else: loop = False



async def process(vid_path, pwidth, pheight):
	out_path = r"rcs\img\frame.jpg"
	frame = frame_capture(vid_path, out_path)
	has_frame = True
	while has_frame:
		has_frame = next(frame, False)
		res = convert_to_ascii(out_path, pwidth=pwidth, pheight=pheight)
	pass





if __name__=='__main__':
	main()