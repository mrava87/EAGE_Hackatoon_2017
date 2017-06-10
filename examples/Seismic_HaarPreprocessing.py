# Data preprocessing
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


def preprocessing(models, basedir=None, size=(50,50)):

    if basedir == None:
        basedir = os.getcwd()

    for model in models:
        for imgfile in os.listdir('/'.join((basedir, model,))):
            if 'stack' in imgfile:
                #print '/'.join((model,imgfile,))
                img = mc.imread('/'.join((model,imgfile,)),mode='L')
                #print img.shape
                #img = equalize(resize(img, size=size))
                img = resize(img, size=size)

                #print '/'.join((model,imgfile[:-4],))+'sub.png'
                mc.toimage(img).save('/'.join((model,imgfile[:-4],))+'sub.png')


if __name__ == "__main__":
    models = ['dip', 'fault', 'flat', 'trap', 'wedge']
    preprocessing(models, size=(50,50))
