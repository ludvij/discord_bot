from sys import argv
import cv2
from PIL import Image
import numpy as np
import os

# Extracts frames from videos
# made a generator to not clutter dirs in images
# a frame is extracted a image is processed
def frame_capture(path):
	# path to the video
	vid = cv2.VideoCapture(path)
	# checks wheter frames where extracted
	has_frame, frame = vid.read()
	while has_frame:
		# saves the frames
		path = r"rcs\img\frames\frame.jpg"
		saved = cv2.imwrite(path, frame)
		# extracts the frames
		has_frame, frame = vid.read()
		yield has_frame


# size should be 60x60
def convert_to_ascii():
	path = rf"rcs\img\frames\frame.jpg"
	# open image and convert it to gray scale
	img = Image.open(path).convert("L")
	os.remove(path)

	# resize image to something more manageable ratio is used to respect img ratio
	ratio = img.size[0] / img.size[1]
	res_img = img.resize((80, int(80 / ratio)))

	width, height = res_img.size


	# since pixels in gray scale go from 0 to 255 we have to divide
	# in ranges to get the best char
	# so we have to darkness * len(chars) - 1 / 255  to get the best index
	# so if we have 10 chars and we have to convert a pixel of value 67 we
	# divide 9 / 255 to get 0.035 and the we mult 67 * 0.035 and we get 2.36
	# so we truncate it to 2, so the char would be ":"
	chars = " .:-=+*#%@"
	# store to ease computations
	divisor = (len(chars) - 1) / 255

	# numpy arrays are a pain to work with, but fast
	# for some reason its transposed ( I know why but still a pain)
	arr = np.chararray((height, width))

	# iterate through each pixel and asign each char
	for i in range(width):
		for j in range(height):
			px = res_img.getpixel((i,j))
			index = int(px * divisor)
			#print(px, index)
			arr[j, i] = chars[index]	

	printable_arr = "\n".join([''.join(row) for row in arr.decode('utf-8')])

	print(printable_arr)
	os.system("cls")

def main():
	frame = frame_capture(argv[1])
	has_frame = True
	count = 0
	while has_frame:
		has_frame = next(frame, False)
		convert_to_ascii()
		count += 1


async def process(vid_path):





if __name__=='__main__':
	main()