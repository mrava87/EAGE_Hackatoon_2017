#!/usr/bin/env python2./
# Haar cascade creation of background files for recognition - to be run in datasets/seismic/synthetics
#
# Authors: C. Birnie, M. Ravasi, F. Broggini

#import urllib
#import cv2
#import numpy as np
import os
from random import shuffle



def create_bg(pos_model, basedir=None, n=100):
    """
    Create bg.txt file
    :param pos_model: 	Name of subfolders of positive model to be excluded
    :param basedir: 	Directory where subdirs are located (if not provided, need to run script from that directory)
    :param n: 	        number of files for each subfolder to be used
    """

    print 'Create bg.txt for positive '+pos_model

    models = ['dip', 'fault', 'flat', 'trap', 'wedge']

    if basedir==None:
        basedir=os.getcwd()

    if pos_model not in models:
        print 'LOL! ' + pos_model + ' does not exist'

    # Models list withou the positive
    neg_models = [model for model in models if model != pos_model]

    # Open file
    with open('/'.join((basedir,pos_model,'bg.txt')),'w') as f:
        for model in neg_models:
            #file_type = 'neg'
            images = [img for img in os.listdir('/'.join((basedir,model,))) if 'stacksub' in img]
            shuffle(images)
            #print images
            for img in images[:n]:
                line = '../'+'/'.join((model,img,))
                f.write(line + '\n')


if __name__ == "__main__":
    create_bg('dip',   n=600)
    create_bg('fault', n=600)
    create_bg('flat',  n=600)
    create_bg('trap',  n=600)
    create_bg('wedge', n=600)

