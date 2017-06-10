#!/usr/bin/env python2.7
# Create dictionary of seismic synthetics
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)


import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as sp

import seispy.GeologicalModelling as GM
import seispy.SeismicModelling2D  as SM


filepath = os.path.join(parentdir, 'datasets/seismic/synthetics/')
filename = 'dict'

if(os.path.isdir(filepath)==False):
    os.mkdir(filepath)

for imod in range(100):

    if imod<25:

        # Make stochastic layered models
        dv   = [1500, 2000]
        drho = [1000, 1800]
        nint = 3
        dint = [20, 80]

        GeoMod = GM.LayeredModel({'dims': [100, 100], 'type': 'layer'})
        GeoMod.Stochastic(nint, dv, drho, dint=dint)
        GeoMod.Apply()

    elif imod<50:

        # Make stochastic dipping models
        vback   = [1500, 1800]
        rhoback = [1000, 1200]
        nint    = 3
        dint    = [20, 80]
        p       = [0.1, 0.2]
        dv      = [-400, 400]
        drho    = [-600, 600]

        GeoMod = GM.DippingModel({'dims': [100, 100], 'type': 'dipping'})
        GeoMod.Stochastic(nint, p, vback, dv, rhoback, drho, dint=dint, flip=True)
        GeoMod.Apply()

    elif imod < 75:

        # Make stochastic wedge models
        vback = [1500, 1800]
        rhoback = [1000, 1200]
        p = [0.1, 0.2]
        dv = [-400, 400]
        drho = [-600, 600]

        GeoMod = GM.WedgeModel({'dims': [100, 100], 'type': 'dipping'})
        GeoMod.Stochastic(p, vback, dv, rhoback, drho, flip=True)
        GeoMod.Apply()

    else:

        # Make stochastic trap models
        perc = 0
        nint = 3
        center_x = 50
        dcenter_z = [50, 180]
        dv = [1500, 2000]
        drho = [1000, 1800]

        GeoMod = GM.TrapModel({'dims': [100, 100], 'type': 'trap'})
        GeoMod.Stochastic(nint, center_x, dcenter_z, dv, drho, perc=0)
        GeoMod.Apply()

    GeoMod.Save(filepath=filepath, filename=filename + str(imod), normV=3000, normRho=3000)


    # Create seismic stack
    Seismod = SM.SeismicModelling2D({'V'      : GeoMod.V,
                                     'Rho'    : GeoMod.Rho,
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



