import requests
from PIL import Image
from io import BytesIO
import sys, pygame
import math
from pynput.keyboard import Key, Listener
from PIL import ImageWin,Image,ImageTk
from network import Network
import time
import threading
import random
import hiders_win as hw

pygame.init()

img = None

meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
pic_base = 'https://maps.googleapis.com/maps/api/streetview?'
api_key = 'AIzaSyBb234wgmcoVlFYlKGwwZjM4QjzS5mPw-I'
pic_base = 'https://maps.googleapis.com/maps/api/streetview?'

angle = 18

n = Network()

def pass_position():
	global latitude, longitude, n
	while 1:
		n.send(str((latitude,longitude)))
		print("sent message")
		time.sleep(5)

def get_image(lat, lon, heading):
	loc = "{},{}".format(lat, lon)
	pic_params = {'key': api_key,
              'location': loc,
              'size': "640x640",
              'heading': heading}
	meta_params = {'key': api_key,
    		  'location': loc}
	response = requests.get(pic_base, pic_params)
	img = response.content
	response.close()
	response = requests.get(meta_base, params=meta_params)
	lat = str(response.json()['location']['lat'])
	lon = str(response.json()['location']['lng'])
	
	return img, lat, lon

def on_press(key):
	global img, heading, latitude, longitude, center
	if key == Key.left:
		heading -= angle
		if heading > 360:
			heading -= 360
		if heading < 0:
			heading += 360
	if key == Key.right:
		heading += angle
		if heading > 360:
			heading -= 360
		if heading < 0:
			heading += 360
	if key == Key.up:
		ang = math.radians(-1 * (heading+90))
		la = dist * math.sin(ang)
		lo = dist * math.cos(ang)

		t_la = float(latitude) - la
		t_lo = float(longitude) - lo

		if ((center[0] - t_la) ** 2 + (center[1] - t_lo) ** 2) ** .5 < radius:
			latitude = str(t_la)
			longitude = str(t_lo)
		else:
			print("Boundary reached")
	if key == Key.down:

		ang = math.radians(-1 * (heading+90))
		la = dist * math.sin(ang)
		lo = dist * math.cos(ang)

		t_la = float(latitude) + la
		t_lo = float(longitude) + lo

		if ((center[0] - t_la) ** 2 + (center[1] - t_lo) ** 2) ** .5 < radius:
			latitude = str(t_la)
			longitude = str(t_lo)
		else:
			print("Boundary reached")


size = width, height = 640, 640

locs = [("40.513687226583706", "-74.45652391447264"),("40.50285845847937", "-74.45213582052482"),
("40.50466949297072", "-74.45277955068839"),("40.499603368097", "-74.44779064192072"),
("40.49761075553259", "-74.44684436456073"),("40.50434828270026", "-74.4491383887266"),
("40.5201934173375", "-74.46054867724386"),("40.52359983851521", "-74.45814027724539"),
("40.519608155813316", "-74.45502120183758"),("40.52275950404587", "-74.4627596674064"),
("40.52370487964106", "-74.46733957560025"),("40.522504400458956", "-74.47203792969569"),
("40.52379491465693", "-74.43725431660272"),("40.525295481449746", "-74.43583296578394"),
("40.52223428960536", "-74.43476695266988"),("40.52016340408309", "-74.4340167952933"),
("40.521318906068295", "-74.43087797890183"),("40.484963576373715", "-74.43682001496367"),
("40.4827113597643", "-74.43711612971758"),("40.4820807255716", "-74.43164787726202"),
("40.4798434278722", "-74.43535918217772")
]
latitude, longitude = random.choice(locs)
#latitude, longitude = locs[0]
# latitude = "40.501510"
# longitude = "-74.454230"
heading = 0
dist = .0001
radius = .02
center = (40.508301, -74.458466)
#circle = [get_image(latitude,longitude,h) for h in range(0,360,angle)]

img, latitude, longitude = get_image(latitude, longitude, heading)
with open("test.jpg", "wb") as f:
	f.write(img)

def run():
	print('run')
	global latitude, longitude, heading, dist, radius, center, img,size
	screen = pygame.display.set_mode(size)
	# Collect events until released
	listener = Listener(on_press=on_press)

	#img, latitude, longitude = get_image(latitude, longitude, heading)

	img = pygame.image.load("test.jpg")

	listener.start()

	lkla = latitude
	lklo = longitude
	lh = heading

	thread = threading.Thread(target=pass_position)
	thread.start()

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				thread.join()
				n.disconnect()
				sys.exit()

		if lkla != latitude or lklo != longitude or lh != heading:
			img, latitude, longitude  = get_image(latitude, longitude, heading)
			with open("test.jpg", "wb") as f:
				f.write(img)
			img = pygame.image.load("test.jpg")
			lkla = latitude
			lklo = longitude
			lh = heading

		screen.fill((0,0,0))
		screen.blit(img, (0,0))
		pygame.display.flip()

if __name__ == "__main__":
	run()