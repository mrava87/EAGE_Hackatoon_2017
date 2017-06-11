#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 14:38:54 2017

@author: cebirnie
"""

### SCRIPT TO CREATE info.lst file and annotations folder and txt files

#cebirnie@Claires-MacBook-Air:imageRec$ head info/info.lst 
#info/annotations/0001_0022_0038_0023_0040.txt
#info/annotations/0002_0045_0053_0023_0040.txt
#info/annotations/0003_0005_0045_0023_0040.txt
#info/annotations/0004_0051_0035_0023_0040.txt
#info/annotations/0005_0048_0029_0023_0040.txt
#info/annotations/0006_0070_0025_0023_0040.txt
#info/annotations/0007_0017_0007_0023_0040.txt
#info/annotations/0008_0020_0051_0023_0040.txt
#info/annotations/0009_0057_0039_0023_0040.txt
#info/annotations/0010_0072_0035_0023_0040.txt

#cebirnie@Claires-MacBook-Air:imageRec$ head info/annotations/0001_0022_0038_0023_0040.txt 
#Image filename : "info/pos/0001_0022_0038_0023_0040.png"
#Bounding box for object 1 "PASperson" (Xmin, Ymin) - (Xmax, Ymax) : (22, 38) - (45, 78)


import glob
import os
import ntpath
from shutil import copyfile

figsize = [35,35]
model   = 'trap'
# Change to directory containing positive image folder
os.chdir("/Users/matteoravasi/Desktop/EAGE_Hackatoon_2017/datasets/seismic/synthetics/"+model+"/")
currentPath=os.getcwd()

positiveFPath=currentPath+'/*_stacksub.png'
annotationDir=currentPath+'/info/pos/'
posDir=currentPath+'/info/pos/'

infoLstFPath='./info/info.lst'

print currentPath

# Find all positions 
allPosFiles=glob.glob(positiveFPath)
print positiveFPath
print allPosFiles

# If pos dir does exist make it
if not os.path.exists(posDir):
    os.makedirs(posDir)

# If annotations dir does exist make it
if not os.path.exists(annotationDir):
    os.makedirs(annotationDir)
    
# Open info.lst file
infoF=open(infoLstFPath,'w')

# get filename
for file in allPosFiles:

    # Copy file
    figFile=ntpath.basename(file)
    copyfile(figFile, posDir+figFile)

    # Write list file
    annFile=posDir+figFile[:-4]+'.png'
    infoF.write(annFile[len(currentPath)+6:]+' 1 0 0 '+str(figsize[0])+' '+str(figsize[1]))
    infoF.write('\n')

    # Write annotation file
    #annFile = posDir + figFile[:-4] + '.png'
    # annF=open(annFile,'w')
    # annF.write('Image filename : "'+'info/pos/'+figFile+'"')
    # annF.write('\n')
    # annF.write('Bounding box for object 1 "PASperson" (Xmin, Ymin) - (Xmax, Ymax) : (0, 0) - (49, 49)')
    # annF.close()

infoF.close()
    

    