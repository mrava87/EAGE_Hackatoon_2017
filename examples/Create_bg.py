#!/usr/bin/env python2./

# Face recognition example from https://www.youtube.com/watch?v=88HdqNDQsEk
# and https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/
#
# Haar cascade creation for recognition
#
# Authors: C. Birnie, M. Ravasi, F. Broggini

#import urllib
#import cv2
#import numpy as np
import os
from random import shuffle

models = ['dip','fault','flat','trap','wedge']

def create_bg(pos_model, basedir=None, n=0):

    if basedir==None:
        basedir=os.curdir()

    if n==0:
        n=100

    if pos_model not in models:
        print 'LOL! ' + pos_model + ' does not exist'

    # Models list withou the positive
    neg_models = [model for model in models if model != pos_model]

    # Open file
    with open('/'.join((basedir,'bg.txt')),'w') as f:
        for model in neg_models:
            #file_type = 'neg'
            images = [img for img in os.listdir('/'.join((basedir,model,))) if 'stack' in img]
            shuffle(images)
            #print images
            for img in images[:n]:
                line = '/'.join((model,img,))
                f.write(line + '\n')

create_bg('dip', '/home/bfilippo/Work/EAGE_Hackatoon_2017/datasets/seismic/synthetics')
