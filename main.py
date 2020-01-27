from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageStat
# get an image
base = Image.open('input.jpg').convert('RGBA')
import log

size=20
width=40
height=22


# make a blank image for the text, initialized to transparent text color
preview_image = Image.new('RGBA', base.size, (255,255,255,0))

preview_text = ""
for i in range(height):
	for j in range(width):
		preview_text += "#"
	preview_text += "\n"	

# get a font
fnt = ImageFont.truetype('fira_code.ttf', size)
# get a drawing context
d = ImageDraw.Draw(preview_image)

def calculateScoreForText(evaluable_text):
	temporal_image = Image.new('RGBA', base.size, (255,255,255,255))
	draw_context = ImageDraw.Draw(temporal_image)
	draw_context.text((0,0), evaluable_text, font=fnt, fill=(0,0,0,255))
	difference = ImageChops.difference(base.convert('RGB'), temporal_image.convert('RGB'))
	width, height = difference.size
	score = 0
	stat = ImageStat.Stat(difference)
	score = stat.sum[0]
#	for i in range(width):
#		for j in range(height):
#			score += difference.getpixel((i,j))[0]
	return score
	

# draw text, half opacit
d.text((0,0), preview_text, font=fnt, fill=(0,0,0,255))

changed_image = Image.alpha_composite(base, preview_image)

out = ImageChops.difference(base.convert('RGB'), changed_image.convert('RGB'))

log.pushOrigin("Ascii Maker")

log.printLogNormal("Showing preview image")
out.show()
log.printLogNormal("Score of preview text is " + str(calculateScoreForText(preview_text)))

dictionary = " ABCDEFGHIJLKMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890~\{}[]()./-><|!@$#%^&*'_"

text_commited = ""

for i in range(height):
	for j in range(width):
		lowest_score = 9999999999999999999999999999999
		best_char = ""		
		for character in dictionary:
			this_score = calculateScoreForText(text_commited + character)
			if this_score < lowest_score:
				best_char = character
				lowest_score = this_score
		text_commited += best_char
		log.printLogNormal("Finished row " + str(j))
	text_commited += "\n"
	print(text_commited)
	log.printLogNormal("Finished line " + str(i))
	
log.popOrigin()
