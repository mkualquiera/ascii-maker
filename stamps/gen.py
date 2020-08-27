#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont

dictionary = " 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;?@[\\]^_`{|}~<=>"

fnt = ImageFont.truetype('font.ttf', 11)
cell_width=5
cell_height=11

images = {}
for character in dictionary:
    new_image = Image.new('L', (int(cell_width), int(cell_height)), (0))
    new_draw = ImageDraw.Draw(new_image)
    new_draw.text((0,0), character, font=fnt, fill=(255))
    images[character] = new_image

res = "unsigned char stamps[] = {"

for i in range(ord(' '),ord(' ')+95):
    c = chr(i)
    for y in range(cell_height):
        for x in range (cell_width):
            v = images[c].getpixel((x,y))
            if v == 255: v = 1
            res += str(v) + ","

res = res[:-1] + "};"
print(res)
