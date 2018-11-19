def readPlotimage(imgs,imgResize, imgRotate, imgGrayscale):
    from scipy.misc import imread, imresize, imsave
    from scipy.ndimage import rotate
    import matplotlib.pyplot as plt
    import string
    import errno
    import os

    imgPath = imgs
    imgRoot,imgName=(os.path.split(imgPath))
    imgRead = imread(imgs)
    
    str_imgResize_x,str_imgResize_y = imgResize.split("x")
    imgResize_x=int(str_imgResize_x)
    imgResize_y=int(str_imgResize_y)
    
    imgOut= imresize(imgRead,(imgResize_x, imgResize_y))
    
    if any("True" in item for item in imgGrayscale):
        imgOut[:]= imgOut.mean(axis=-1,keepdims=1)
        
    imgRoot=str(imgRoot)
    imgName=str(imgName)
    imgName_name, imgName_ext=imgName.split(".")
    imsave((imgRoot+'/'+'+augmented'+'.'+imgName_name+'.'+imgName_ext),imgOut)

    
import argparse
import fnmatch
import os
    
parser=argparse.ArgumentParser()
parser.add_argument('--directory',help='put the directory of the image')
parser.add_argument('--resize',help='put resolution size you want here Format=20x20')
parser.add_argument('--grayscale',choices = ['True','False'], help = "put bool values to enable grayscale ethier true or False. Format: <True>")
args=parser.parse_args()


imgDIRs = args.directory
imgResize = args.resize
imgGrayscale = [args.grayscale]

images = ['*.png', '*.jpg','*.jpeg', '*.tif', '*.tiff',]
matches = []

for root, dirnames, filenames in os.walk(imgDIRs):
    for extension in images:
        for filename in fnmatch.filter(filenames,extension):
            matches.append(os.path.join(root,filename).replace("\\'.'/"))

matches = [x for x in matches if not 'augmented' in x]

for img in matches:
    readPlotimage(img,imgResize,imgGrayscale)


        