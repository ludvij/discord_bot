from PIL import Image, ImageDraw, ImageFont
from os import getenv
import textwrap

# Adds text to the image in a given rectangle
# Asynchronous funcion since it can be some time depending on the text to add 
# thanks to the length calculations
# TODO: find a better way to calculate the length
async def add_text(text, img_path, xy, dims, out_name="res.jpg", textsize=60):
	img = Image.open(img_path)
	img_edit = ImageDraw.Draw(img)
	# uncomment to test the position of the rectangle
	# img_edit.rectangle((xy[0], xy[1], xy[0] + dims[0], xy[1] + dims[1]), outline="#000000")

	font_path = getenv("FONT")
	font = ImageFont.truetype(font_path, textsize)

	# get a better configuration of the text
	textsize, lines = await _get_textsize_and_lines(text, font_path, textsize, dims)
	font = ImageFont.truetype(font_path, textsize)

	# Centering of the tet, just in vertical way
	y_centered = get_centered_dims(xy[1], dims[1], len(lines), textsize)
	xy = (xy[0], y_centered)
	
	for line in lines:
		img_edit.text(xy, line, font=font, fill="#000000")
		xy = (xy[0], xy[1] + textsize)

	img.save(out_name)

def get_centered_dims(y0, y1, lines, textsize):
	# put the starting point at the center of the rectangle
	start = int(y0 + y1 / 2)

	# if there is more than one line you add half the lines times the size up
	if lines > 1: start -= textsize * int(lines / 2)
	# if lines are even you add half the size up to center the middle line
	if lines % 2 != 0: start -= textsize / 2

	return start

# for a rectangle of lenght 230 13 linewrap is valid if size is 40
# then: if size is 20, linewrap should be 26
# ! magic numbers below
# ? so: linewrap shoud be length / size * 2.26 (eyed) should be rounded 
# for a rectangle of height 125 3 lines should be max with size 40
# then: if size is 20 we can fit 6 lines
# so: lines should be height / size
#
# size should be prioritized to the initial size,
# if it doesn't fit try wrapping
# if there are more lines than expected reduce size
async def _get_textsize_and_lines(text, font_path, original_size, dims):
	# ! Original algorithm, still works I think
	# size = original_size
	# font = ImageFont.truetype(font_path, original_size)
	# length = dims[0]
	# height = dims[1]
	# linewrap = int(round(length / size * 2.6, 0))

	# if font.getlenght(text) > length:
	# 	maxLines = font.getlenght(text) / size
	# 	lines = maxLines + 1

	# 	while lines > maxLines or (lines * size) > height:
	# 		size -= 1
	# 		linewrap = int(round(length / size * 2.6, 0))
	# 		lines = len(textwrap.wrap(text, linewrap))
	# else:
	# 	size = int(round(size / font.getlenght(text) * length, 0))
	
	font = ImageFont.truetype(font_path, original_size)
	curr_length = font.getlength(text)
	width = dims[0]
	height = dims[1]
	size = font.size

	# if text is longer than the side of the rectangle try wrapping
	if (curr_length > width):
		lines = curr_length / width
		# if the amount of lines times their size is greater than the height reduce font size and start again
		while (lines * size) > height:
			size -= 1
			font = ImageFont.truetype(font_path, size)
			curr_length = font.getlength(text)
			lines = curr_length / width
	else:
		max_size = int(round(size / font.getlength(text) * width, 0))
		size = min(height, max_size)
	# ? this is a magic number and to be honest I don't know where it came from
	# ? just circumstancial evidence 2.6 works only for robot light
	linewrap = int(round(width / size * 2.6, 0))

	return size, textwrap.wrap(text, linewrap)