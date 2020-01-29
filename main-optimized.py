from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageStat
# get an image
base = Image.open('input.jpg').convert('RGB')
import log

size=20
width=40
height=22


x_offset = 12.31
y_offset = 23

preview_text = ""
for i in range(height):
	for j in range(width):
		preview_text += "#"
	preview_text += "\n"

# get a font
fnt = ImageFont.truetype('fira_code.ttf', size)
# get a drawing context


log.pushOrigin("Ascii Maker")

dictionary = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;?@[\\]^_`{|}~ "

images = {}
log.printLogNormal("Pre-rendering images")
for character in dictionary:
	new_image = Image.new('RGB', (30, 30), (255, 255, 255))
	new_draw = ImageDraw.Draw(new_image)
	new_draw.text((0,0), character, font=fnt, fill=(0,0,0))
	images[character] = new_image

cached_image = None

def calculateScoreForText(evaluable_text, i, j):
	global cached_image
	x = j * x_offset
	y = i * y_offset
	if cached_image == None:
		cached_image = base.crop((x, y, x+30, y+30))
	difference = ImageChops.difference(cached_image, images[evaluable_text])
	score = 0
	stat = ImageStat.Stat(difference)
	score = stat.sum[0]
	return score

text_commited = ""

for i in range(height):
	for j in range(width):
		lowest_score = 9999999999999999999999999999999
		best_char = ""
		if cached_image:
			cached_image = None
		for character in dictionary:
			this_score = calculateScoreForText(character, i, j)
			if this_score < lowest_score:
				best_char = character
				lowest_score = this_score
		text_commited += best_char
	text_commited += "\n"
	print(text_commited)
	log.printLogNormal("Finished line " + str(i))

log.popOrigin()
