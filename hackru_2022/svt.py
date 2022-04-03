import requests
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from io import BytesIO

meta_base = 'https://maps.googleapis.com/maps/api/streetview/metadata?'
pic_base = 'https://maps.googleapis.com/maps/api/streetview?'
api_key = 'AIzaSyBb234wgmcoVlFYlKGwwZjM4QjzS5mPw-I'

location = "55 Morrell St, New Brunswick, NJ 08901"

# define the params for the metadata reques
meta_params = {'key': api_key,
               'location': location}
# define the params for the picture request
pic_params = {'key': api_key,
              'location': location,
              'size': "640x640"}

# obtain the metadata of the request (this is free)
meta_response = requests.get(meta_base, params=meta_params)

# display the contents of the response
# the returned value are in JSON format
print((meta_response.json()['location']['lat']))



exit()
pic_response = requests.get(pic_base, params=pic_params)

print(type(pic_response))

for key, value in pic_response.headers.items():
	print(f"{key}: {value}")

"""
with open('test.jpg', 'wb') as file:
    file.write(pic_response.content)
"""
img = pic_response.content
img = Image.open(BytesIO(img))


# remember to close the response connection to the API
pic_response.close()


# using matpltolib to display the image
plt.figure(figsize=(10, 10))
#img=mpimg.imread('test.jpg')
imgplot = plt.imshow(img)
plt.show()
