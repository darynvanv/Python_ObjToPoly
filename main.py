import sys
from PIL import Image, ImageDraw
import numpy as np

vertices = []
faces = []

with open('Test.obj') as obj_file:
    for line in obj_file:
        if(line.startswith('v ')):
            vertices.append(line.split(' '))
            
        if(line[0] == 'f'):
            faces.append(line.split(' '))



dir = "LEFT"


layers = []
faces_full = []

for item in faces:
    item.pop(0)
    new_item = []
    for set in item:
        new_item.append( [int(x) for x in set.split('/')] )
    
    faces_full.append( new_item )

print(faces_full)

for line in faces_full:
    this_face = []
    for set in line:
        if(dir == "TOP"):
            index = int(set[0]) - 1
            vertice = vertices[index]
            this_face.append(vertice[1].strip('\n'))
            this_face.append(vertice[3].strip('\n'))
                
        if(dir == "LEFT"):
            index = int(set[0]) - 1
            vertice = vertices[index]
            this_face.append(vertice[1].strip('\n'))
            this_face.append(vertice[2].strip('\n'))
                
        if(dir == "FRONT"):
            index = int(set[0]) - 1
            vertice = vertices[index]
            this_face.append(vertice[2].strip('\n'))
            this_face.append(vertice[3].strip('\n'))

    layers.append("L " + ','.join(this_face))

print(layers)

f = open("output.plf", "w")
f.write('\n'.join(layers))
f.close()

width = 2000
height = 2000

im = Image.new(mode="RGB", size=(width, height))

draw = ImageDraw.Draw(im)

scale = 200

for layer in layers:
    this_layer = []
    type = layer.split(' ')[0]
    points = layer.split(' ')[1]
    points = [(float(x) + 2) * scale for x in points.split(',')]
    this_layer = points
    if(len(this_layer) > 2):
        draw.polygon(this_layer, "white", "black")

im.show()