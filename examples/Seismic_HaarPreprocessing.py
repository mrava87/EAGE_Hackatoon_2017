# Data preprocessing - to be run in datasets/seismic/synthetics
#
# Authors: C. Birnie, M. Ravasi

import os
import numpy as np
import scipy.misc as mc
from skimage import exposure

def resize(im, size=(50,50)):
    return mc.imresize(im,size)

def equalize(im):
    out = exposure.equalize_adapthist(im)
    out *= 255.0/ np.amax(out)
    return out.astype(np.uint8)


def preprocessing(models=['flat','dip','wedge','fault','trap'], basedir=None, size=(50,50)):
    """
    Preprocesses seismic images files (resizing + equalization)
    :param models: 	    Name of subdirs where models are located
    :param basedir: 	Directory where subdirs are located (if not provided, need to run script from that directory)
    :param size: 	    Size of output files
    """
    if basedir == None:
        basedir = os.getcwd()
    print basedir

    for model in models:
        print 'preprocessing '+model
        for imgfile in os.listdir('/'.join((basedir, model,))):
            if 'stack.png' in imgfile:
                # read file
                #print '/'.join((basedir,model,imgfile,))
                img = mc.imread('/'.join((basedir,model,imgfile,)),mode='L')
                #print img.shape

                # preprocess file
                #img = equalize(resize(img, size=size))
                img = resize(img, size=size)

                # save file
                #print '/'.join((model,imgfile[:-4],))+'sub.png'
                mc.toimage(img).save('/'.join((basedir,model,imgfile[:-4],))+'sub.png')



if __name__ == "__main__":
    models = ['flat','dip','wedge','fault','trap']
    preprocessing(models, size=(35,35))
