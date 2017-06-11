#!/usr/bin/env python2./
# Haar cascade creation of positive and info files for recognition - to be run in datasets/seismic/synthetics
#
# Authors: C. Birnie, M. Ravasi



import glob
import os
import ntpath
from shutil import copyfile

def makeInfoLst(pos_model='flat', basedir=None, figsize = [35,35]):
    """
    Create info.list file
    :param pos_model: 	Name of subfolders of positive model to be excluded
    :param basedir: 	Directory where subdirs are located (if not provided, need to run script from that directory)
    :param figsize: 	Size of positive files
    """

    print 'Create info.list for positive '+pos_model

    if basedir == None:
        basedir = os.getcwd()

    # Change to directory containing positive image folder
    os.chdir('/'.join((basedir,pos_model,)))
    currentPath=os.getcwd()
    # print currentPath

    positiveFPath = currentPath+'/*_stacksub.png'
    annotationDir = currentPath+'/info/pos/'
    posDir        = currentPath+'/info/pos/'

    infoLstFPath='./info/info.lst'


    # Find all positions
    allPosFiles=glob.glob(positiveFPath)
    #print allPosFiles

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
    

if __name__ == "__main__":
    makeInfoLst(pos_model='flat',  figsize=[35, 35])
    makeInfoLst(pos_model='fault', figsize=[35, 35])
    makeInfoLst(pos_model='flat',  figsize=[35, 35])
    makeInfoLst(pos_model='trap',  figsize=[35, 35])
    makeInfoLst(pos_model='wedge', figsize=[35, 35])

