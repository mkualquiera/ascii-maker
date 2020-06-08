import string
import sys
import math
import os

import argparse

from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageStat, ImageOps, ImageColor

parser = argparse.ArgumentParser(description="Convert images to ascii art.")
parser.add_argument("filename",action='store', help="The filename of the image to be converted")
parser.add_argument("--width", "-w", action='store', type=int, help="The final width in characters")
parser.add_argument("--invert", "-i", action='store_true', help="Invert image brightness")
parser.add_argument("--colors", "-c", action='store_true', help="Use colors in the converted image")
parser.add_argument("--background", "-b", action='store_true', help="Also change background")

args = parser.parse_args()

# get the image
try:
	if args.colors:
		base = Image.open(args.filename).convert('RGB')
	else:
		base = Image.open(args.filename).convert('L')
except:
	print("Unable to read image file.")

base_w, base_h = base.size
font_size = 16
cell_width = 10
cell_height = 20

# base dimensions in pixels
base_w, base_h = base.size

# base dimensions in cells
width = math.floor(base_w / cell_width)
height = math.floor(base_h / cell_height)

# target dimension in cells
target_cw = width

# invert image ?
inverted = False

inverted = args.invert

if args.width:
	target_cw = args.width

if inverted:
	base = ImageOps.invert(base)

# scale image
target_pw = target_cw*cell_width
wpercent = (target_pw/float(base.size[0]))
target_ph = int((float(base.size[1])*float(wpercent)))
base = base.resize((int(target_pw), int(target_ph)), Image.ANTIALIAS)


# base dimensions in cells
width = math.floor(target_pw / cell_width)
height = math.floor(target_ph / cell_height)

# get a font
fnt = ImageFont.truetype('fira_code.ttf', font_size)

if args.colors:
	color_codes = [
		"#181818",
		"#b13c3d",
		"#78b13c",
		"#b1943c",
		"#3c48b1",
		"#963cb1",
		"#42a89c",
		"#cfcfcf",
		"#4f4f4f",
		"#ff5658",
		"#adff56",
		"#ffd556",
		"#5668ff",
		"#d856ff",
		"#64ffef",
		"#ffffff"
	]

	colors = []

	for color_code in color_codes:
		colors.append(ImageColor.getrgb(color_code))

dictionary = " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;?@[\\]^_`{|}~<=>"

print(len(dictionary))

exit()

images = []
for character in dictionary:
	if args.colors:
		for foreground_color_id in range(len(colors)):
			skip=False
			for background_color_id in range(len(colors)):
				if skip:
					continue
				if not args.background:
					background_color_id = 0
					skip=True
				new_image = Image.new('RGB', (int(cell_width), int(cell_height)), color=colors[background_color_id])
				new_draw = ImageDraw.Draw(new_image)
				new_draw.text((0,0), character, font=fnt, fill=colors[foreground_color_id])
				images.append((new_image,character,background_color_id,foreground_color_id))
				new_image.save("stamps/" + str(ord(character)).zfill(3) + "_" + str(background_color_id).zfill(2) + "_" + str(foreground_color_id).zfill(2) + ".png")
	else:
		new_image = Image.new('L', (int(cell_width), int(cell_height)), (255))
		new_draw = ImageDraw.Draw(new_image)
		new_draw.text((0,0), character, font=fnt, fill=(0))
		images.append((new_image,character))

exit()


def parse_setup(setup):
	result = ""
	if not setup[1] == 7:
		if setup[1] >= 0 and setup[1] <= 7:
			result += "\033[" + str(30 + setup[1]) + "m"
		else:
			result += "\033[" + str(82 + setup[1]) + "m"
	if not setup[2] == 0:
		if setup[2] >= 0 and setup[2] <= 7:
			result += "\033[" + str(40 + setup[2]) + "m"	
		else:
			result += "\033[" + str(92 + setup[2]) + "m"
	result += setup[0]
	result += "\033[0m"
	return result


def best_character_at(x, y):
	xx = x * cell_width
	yy = y * cell_height
	reference = base.crop((xx, yy, xx+cell_width, yy+cell_height))

	if not args.colors:
		best_score = sys.maxsize
		best_char = " "
		for i in images:
			c = i[1]
			difference = ImageChops.difference(reference, i[0])
			stat = ImageStat.Stat(difference)
			score = stat.sum[0]
			if score < best_score:
				best_score = score
				best_char = c
				if score == 0:
					return best_char
		return best_char

	else:
		best_score = sys.maxsize
		best_setup = (" ", 0, 0)
		for i in images:
			if i[3] == i[2]:
				if i[1] != " ":
					continue
			setup = (i[1], i[3], i[2])
			difference = ImageChops.difference(reference, i[0])
			stat = ImageStat.Stat(difference)
			score = stat.sum[0]*stat.sum[0] + stat.sum[1]*stat.sum[1] + stat.sum[2]*stat.sum[2]
			if score < best_score:
				best_score = score
				best_setup = setup
				if score == 0:
					return parse_setup(best_setup)
		return parse_setup(best_setup)
		



for y in range(height):
	for x in range(width):
		sys.stdout.write(best_character_at(x, y))
	sys.stdout.write("\n")

