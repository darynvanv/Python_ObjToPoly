import sys
import os
import glob
from PIL import Image, ImageDraw
import numpy as np

input_path = ""
output_path = ""
dir = "LEFT"

# Handle Command Line Inputs
args = sys.argv
for index, arg in enumerate(args):
    if arg == '-d':
        if len(args) > index + 1:
            dir = args[index + 1]
        else:
            print("Invald or Empty Direction. Possible values are 'FRONT', 'LEFT', 'TOP'")
            exit(1)

    if arg == '-i':
        if len(args) > index + 1:
            input_path = args[index + 1]
        else:
            print("Invald or Empty input path.")
            exit(1)
    
    if arg == '-o':
        if len(args) > index + 1:
            output_path = args[index + 1]
        else:
            print("Invald or Empty output path.")
            exit(1)

if(output_path == ""):
    print("No output path provided. Input path will be used.")
    output_path = input_path

print("Direction: " + dir)
print("Input Path: " + input_path)
print("Output Path: " + output_path)

if(os.path.isdir(input_path)):
    print("Input Path is a Folder. Scanning for OBJs")

if(os.path.isfile(input_path)):
    print("Input Path is a File. Using as Input file")


print("Found " + str(len(glob.glob(input_path + "*.obj"))) + " files.")

for file_name in glob.glob(input_path + "*.obj"):

    vertices = []
    faces = []


    print("Parsing " + file_name)

    with open(file_name) as obj_file:
        for line in obj_file:
            if(line.startswith('v ')):
                vertices.append(line.split(' '))
                
            if(line[0] == 'f'):
                faces.append(line.split(' '))

    if(len(vertices) == 0):
        print("No Vertices to Parse. Skipping")
        continue

    print("Loaded " + str(len(vertices)) + " vertices")
    print("Loaded " + str(len(faces)) + " faces")


    layers = []
    faces_full = []

    for item in faces:
        item.pop(0)
        new_item = []
        for set in item:
            new_item.append( [int(x) for x in set.split('/')] )
        
        faces_full.append(new_item)
        
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


    input_name = os.path.basename(file_name)

    f = open(output_path + input_name.split(".")[0] + ".plf", "w")
    f.write('########################\n')
    f.write('# Generated by OBJ2PLF #\n')
    f.write('#     Version 0.1      #\n')
    f.write('########################\n')
    f.write('\n'.join(layers))
    f.close()