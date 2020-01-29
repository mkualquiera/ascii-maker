import string
import sys
import math
import os

from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageStat, ImageOps

import log

args = sys.argv[1:]
# get the image
if len(args) >= 1:
	base = Image.open(args[-1]).convert('L')
else:
	sys.exit()

base_w, base_h = base.size
font_size = 16
cell_width = 9.1
cell_height = 19

# base dimensions in pixels
base_w, base_h = base.size

# base dimensions in cells
width = math.floor(base_w / cell_width)
height = math.floor(base_h / cell_height)

# target dimension in cells
target_cw = width

# invert image ?
inverted = False

for a in args[:-1]:
	# print(a)
	if a == "--invert":
		inverted = True
	elif a.startswith("--width="):
		segs = a.split("=", 1)
		target_cw = int(segs[1])
	# elif a.startswith("--height="):
	# 	segs = a.split("=", 1)
	# 	target_ch = int(segs[1])

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

log.pushOrigin("Ascii Maker")

dictionary = " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;?@[\\]^_`{|}~<=>"

images = {}
log.printLogNormal("Rendering stamps")
for character in dictionary:
	new_image = Image.new('L', (int(cell_width), int(cell_height)), (255))
	new_draw = ImageDraw.Draw(new_image)
	new_draw.text((0,0), character, font=fnt, fill=(0))
	images[character] = new_image


def best_character_at(x, y):
	best_score = sys.maxsize
	best_char = " "
	xx = x * cell_width
	yy = y * cell_height
	reference = base.crop((xx, yy, xx+cell_width, yy+cell_height))

	for c in dictionary:
		difference = ImageChops.difference(reference, images[c])
		stat = ImageStat.Stat(difference)
		score = stat.sum[0]
		if score < best_score:
			best_score = score
			best_char = c
			if score == 0:
				return best_char

	return best_char


log.printLogNormal("Rendering image")
for y in range(height):
	for x in range(width):
		sys.stdout.write(best_character_at(x, y))
	sys.stdout.write("\n")

log.popOrigin()
