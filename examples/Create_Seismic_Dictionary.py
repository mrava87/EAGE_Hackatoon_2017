#!/usr/bin/env python2.7
# Create dictionary of seismic synthetics
import os, sys
sys.path.append(os.path.abspath('..'))

import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as sp

import seispy.GeologicalModelling as GM
import seispy.SeismicModelling2D  as SM



filepath = './datasets/seismic/synthetics/'
filename = 'dict'


for imod in range(50):

    if imod<25:

        # Make stochastic layered models
        dv   = [1500, 2000]
        drho = [1000, 1800]
        nint = 3
        dint = [20, 80]

        Layers = GM.LayeredModel({'dims': [100, 100], 'type': 'layer'})
        Layers.Stochastic(nint, dv, drho, dint=dint)
        Layers.Apply()
    else:

        # Make stochastic dipping models
        vback   = [1500, 1800]
        rhoback = [1000, 1200]
        nint    = 3
        dint    = [20, 80]
        p       = [0.1, 0.2]
        dv      = [-400, 400]
        drho    = [-600, 600]

        Layers = GM.DippingModel({'dims': [100, 100], 'type': 'dipping'})
        Layers.Stochastic(nint, p, vback, dv, rhoback, drho, dint=dint, flip=True)
        Layers.Apply()

    #Layers.Save(filepath=filepath, filename=filename+str(imod), normV=3000, normRho=3000)


    # Create seismic stack
    Seismod = SM.SeismicModelling2D({'V'      : Layers.V,
                                     'Rho'    : Layers.Rho,
                                     'dt'     : 0.004,
                                     'ot'     : 0,
                                     'ntrick' : 31,
                                     'f0'     : 10})

    Seismod.Apply()
    #Seismod.Visualize(cbarlims=[-4e12,4e12])
    Seismod.Save(filepath=filepath, filename=filename+str(imod), norm=6e12)

    #imgpng = sp.imread(filepath+filename+str(imod)+'_stack.png', flatten=True)
    #plt.figure()
    #plt.imshow(imgpng, cmap='gray',vmin=0, vmax=255)

#plt.show()



