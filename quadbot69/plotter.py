from PIL import Image, ImageDraw
#graph completed
#origin = x=115, y=834
def graph(*args):
	graph1 = Image.open('graph.png')
	draw = ImageDraw.Draw(graph1)
	if len(args) >= 30:
		x1,y1 = 121,792-(args[0]*10)
		for y in list(args)[1:]:
			draw.line((x1,y1,x1+20,792-(y*10)), width=3, fill = (89,179,105)) #20= x-scale
			x1,y1 = x1+20,792-(y*10)
	else:
		x1,y1 = 121,792
		for y in list(args):
			draw.line((x1,y1,x1+20,792-(y*10)), width=2, fill = (89,179,105)) #20= x-scale
			x1,y1 = x1+20,792-(y*10)
	graph1 = graph1.resize((1500,1500),resample=Image.ANTIALIAS)
	graph1.save(r'processed.png', quality=100,optimize=True)