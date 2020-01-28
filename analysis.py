from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageStat
import matplotlib.pyplot as plt
import log

dictionary = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;?@[\\]^_`{|}~ " * 8

size = 20
fnt = ImageFont.truetype('fira_code.ttf', size)

image_size = (500, 500)

line_width = 40

text_to_test = ""

for i in range(len(dictionary)):
    text_to_test += dictionary[i]
    if (i+1) % line_width == 0:
        text_to_test += "\n"

base_image = Image.new('RGB', image_size, (255,255,255))

draw_context = ImageDraw.Draw(base_image)

draw_context.text((0,0), text_to_test, font=fnt, fill=(0,0,0))

x_offset = 12.31
y_offset = 23

currline = 0
currrow = 0

new_image = Image.new('RGB', image_size, (255, 255, 255))
new_draw = ImageDraw.Draw(new_image)
text_to_test += "[fake]"
for character in text_to_test:
    if character == '\n':
        currline += 1
        currrow = 0
    else:
        x_pos = x_offset * currrow
        y_pos = y_offset * currline
        currrow += 1
        new_draw.text((x_pos,y_pos), character, font=fnt, fill=(0,0,0))

base_image.show()
new_image.show()
difference = ImageChops.difference(new_image, base_image)
difference.show()
