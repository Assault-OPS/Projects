from PIL import Image, ImageDraw,ImageFont
from datetime import datetime
import pytz
#graph completed
#origin = x=115, y=834
def time_gen():
	IST = pytz.timezone('Asia/Kolkata')
	time = datetime.now(IST)
	five = []
	hour = int(time.strftime('%I'))
	for i in range(5):
		five.append(str(hour)+':'+time.strftime("%M")[:1]+'0')
		hour -= 1
		hour = 12 if hour < 1 else hour
	return five[::-1]

def graph(*args):
	graph1 = Image.open('graph.png')
	draw = ImageDraw.Draw(graph1)
	font = ImageFont.truetype("fonts/ubuntu.ttf", 25)
	if len(args) >= 30:
		x1,y1 = 121,792-(args[0]*10)
		for y in list(args)[1:]:
			draw.line((x1,y1,x1+20,792-(y*10)), width=3, fill = (89,179,105)) #20= x-scale
			x1,y1 = x1+20,792-(y*10)
		tx,ty = 242,821
		for i in range(5):
			h = time_gen()[i].split(":")[0]
			m = time_gen()[i].split(":")[1]
			draw.text((tx, ty), ":", (255, 255, 255), font=font)
			draw.text((tx-(3+font.getsize(h)[0]),ty),h,(255,255,255),font=font)
			draw.text((tx+(3+font.getsize(":")[0]), ty), m, (255, 255, 255), font=font)
			tx += 119
	else:
		x1,y1 = 121,792
		for y in list(args):
			draw.line((x1,y1,x1+20,792-(y*10)), width=2, fill = (89,179,105)) #20= x-scale
			x1,y1 = x1+20,792-(y*10)
		tx,ty=230,821
		for i in range(5):
			draw.text((tx, ty), str(i+1)+'h', (255, 255, 255), font=font)
			tx += 119
	graph1 = graph1.resize((1500,1500),resample=Image.ANTIALIAS)
	graph1.save(r'processed.png', quality=100,optimize=True)