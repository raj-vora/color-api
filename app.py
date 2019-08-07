from flask import Flask,request,jsonify
#import cv2
import numpy as np
import urllib.parse,base64
from PIL import Image
import io,webcolors

app = Flask(__name__)

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name



@app.route('/',methods=['POST'])
def color_detection_center():
    data = request.get_json()
    image_urlencoded = data['data']
    image_base64 = urllib.parse.unquote(image_urlencoded)
    image_not_in_format = base64.b64decode(image_base64)
    image_in_format = Image.open(io.BytesIO(image_not_in_format))
    a = np.array(image_in_format)
    color_here = []
    center_x = round(a.shape[0]/2)
    center_y = round(a.shape[1]/2)
    for i in range(center_y-50,center_y+50,10):
    	for j in range(center_x-50,center_x+50,10):
    		color_here.append(a[i][j].tolist())

    color_here_final = max(color_here,key=color_here.count)
    requested_colour = color_here_final#[::-1]
    actual_name, closest_name = get_colour_name(requested_colour)

    #print ("Actual colour name:", actual_name, ", closest colour name:", closest_name)
    return closest_name
    
    
if __name__ == '__main__':
    app.run(debug=True)
