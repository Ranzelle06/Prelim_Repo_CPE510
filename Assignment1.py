import numpy as np
from scipy.misc import imread, imresize, imsave
from scipy.ndimage import rotate
from scipy.misc import face
import matplotlib.pyplot as plt
import os
import fnmatch
import scipy.misc
import argparse

parser=argparse.ArgumentParser()
parser.add_argument('--folder',help='put the directory of the image')
parser.add_argument('--resize',help='put resolution size you want here Format=20x20')
parser.add_argument('--rotate',help='put rotate degree value you want here.')
parser.add_argument('--grayscale',choices = ['True','False'], help = "put bool values to enable grayscale ethier true or False. Format: <True>")
args=parser.parse_args()

#get the parameters
folder=args.folder
dim=args.resize
if dim != 0:
    dim=dim.split('x')
    x_dim=int(dim[0])
    y_dim=int(dim[1])
gray=args.grayscale
gray2=str(gray.lower())
gray3="true"
if gray2==gray3:
    gray=True
else:
    gray=False

rot=int(args.rotate)

#get all image addresses
extensions_list = ['.jpg', '.jpeg', '.png', '.tif', '.tiff']
images=[]
temp=[]
for root, dirs, files in os.walk(folder):
    for extension in extensions_list:
        for file in files:
            if file.endswith(extension):
                images=images+[os.path.join(root, file)]

for image in images:
    
    img=imread(image)
    #RESIZE
    aug_img=imresize(img,(x_dim,y_dim))

    #GRAYSCALE
    if gray==True:
        x,y,z=aug_img.shape
        aug_img[:]=aug_img.mean(axis=-1,keepdims=1)

    #ROTATE
    aug_img=rotate(aug_img,rot)
    
    head, sep, tail = image.partition('.')
    temp=head+'-Augmented.jpg'
    scipy.misc.imsave(temp, aug_img)
    
print("DONE")