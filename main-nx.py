import string
import sys
import math
import os

from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageStat

import log

args = sys.argv[1:]

# get the image
if len(args) >= 1:
	base = Image.open(args[0]).convert('RGB')
else:
	sys.exit()

base_w, base_h = base.size
font_size = 16
cell_width = 8
cell_height = 16

width = math.floor(base_w / cell_width)
height = math.floor(base_h / cell_height)
# get a font
fnt = ImageFont.truetype('fira_code.ttf', font_size)

log.pushOrigin("Ascii Maker")

dictionary = string.printable
for c in string.whitespace:
	dictionary.replace(c, "")
dictionary += " "

images = {}
log.printLogNormal("Rendering stamps")
for character in dictionary:
	new_image = Image.new('RGB', (cell_width, cell_height), (255, 255, 255))
	new_draw = ImageDraw.Draw(new_image)
	new_draw.text((-1,-2), character, font=fnt, fill=(0,0,0))
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

	return best_char


log.printLogNormal("Rendering image")
for y in range(height):
	for x in range(width):
		sys.stdout.write(best_character_at(x, y))
	sys.stdout.write("\n")

log.popOrigin()
