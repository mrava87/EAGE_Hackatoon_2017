import numpy as np
import scipy.misc as sp

import matplotlib.pyplot as plt


class GeologicalModelling:
    """
    Class for creating simple parametric geological models

    inputs:
    ------

    type:         'Layered', 'Trap', 'Fault'...
    dims:         Dimensions of model

    functions:
    ----------

    Returns: a GeologicalModelling object

    """

    def __init__(self, par):

        self.type = par['type']
        self.nz   = par['dims'][0]
        self.nx   = par['dims'][1]

        return


    def Visualize(self, figsize=(12, 7)):
        """
        Visualize models
        :param figsize: 	Figure size
        """

        fig, ax = plt.subplots(1, 2, figsize=figsize)
        cax = ax[0].imshow(self.V)
        ax[0].set_title('V')
        ax[0].axis('tight')

        cax = ax[1].imshow(self.Rho)
        ax[1].set_title('Rho')
        ax[1].axis('tight')

        return


    def Save(self, filepath='./', filename='test', normV=1, normRho=1):
        """
        Save models in png files
        :param filepath: 	Path to save .png files
        :param filename: 	Prefix to give to .png files
        """

        V = (self.V / normV) * (255.)
        sp.toimage(V, cmin=0, cmax=255).save(filepath + filename + 'V.png')

        Rho = (self.Rho / normRho) * (255.)
        sp.toimage(Rho, cmin=0, cmax=255).save(filepath + filename + 'Rho.png')

        return



class LayeredModel(GeologicalModelling):
    """
    Class for creating layered model

    Returns: a GeologicalModelling object

    """
    def __init__(self, par):
        par['type'] = 'layer'
        GeologicalModelling.__init__(self, par)


    def Deterministic(self, ints, v, rho=np.array([])):
        """
        Create layered model given deterministic parametric definition
        :param ints: 	    Size of intervals
        :param v: 	        Velocity of intervals
        :param rho: 	    Density of intervals
        """

        self.int = ints
        self.v   = v
        if len(rho)==0:
            self.rho = 1000*np.ones(len(self.int))
        else:
            self.rho = rho


    def Stochastic(self, nint, dv, drho=[], dint=[]):
        """
        Create layered model given stochastic parametric definition
        :param nint: 	    Number of intervals
        :param dint: 	    Range of intervals [intmin,intmax] from which int is uniformly drawn
        :param dv: 	        Range of velocities [vmin,vmax] from which v is uniformly drawn
        :param drho: 	    Range of densities  [vmin,vmax] from which v is uniformly drawn
        """

        if len(dint)==0:
            dint=[0,self.nz]

        # draw reflector positions
        nrefl = nint - 1
        refl  = np.floor(np.random.uniform(dint[0],dint[1],nrefl)) + 1
        refl  = np.sort(refl)

        self.int       = np.zeros(nint, dtype=np.int8)
        self.int[0]    = np.int8(refl[0])
        self.int[1:-1] = np.int8(np.diff(refl))
        self.int[-1]   = np.int8(self.nz - refl[-1])
        #print 'sum of ints:',np.sum(self.int)

        # draw velocity and density
        self.v = np.round(np.random.uniform(dv[0],dv[1],nint))
        if len(drho) == 0:
            self.rho = 1000 * np.ones(nint)
        else:
            self.rho = np.round(np.random.uniform(drho[0],drho[1],nint))

        #print 'int',self.int
        #print 'v',self.v
        #print 'rho',self.rho

        return


    def Apply(self):
        """
        Apply layers modelling
        """
        v   = self.v[0]  * np.ones(self.int[0])
        rho = self.rho[0]* np.ones(self.int[0])

        for iint in range(1,len(self.int)):
            v   = np.hstack((v,   self.v[iint]  * np.ones(self.int[iint])))
            rho = np.hstack((rho, self.rho[iint]* np.ones(self.int[iint])))

        self.V   = np.repeat(v[:, np.newaxis],   self.nx, axis=1)
        self.Rho = np.repeat(rho[:, np.newaxis], self.nx, axis=1)




class DippingModel(GeologicalModelling):
    """
    Class for creating dipping layered model

    Returns: a GeologicalModelling object

    """
    def __init__(self, par):
        par['type'] = 'dipping'
        GeologicalModelling.__init__(self, par)
        self.flip = False


    def Deterministic(self, ints, p, vback, dv, rhoback=1000, drho=np.array([])):
        """
        Create dipping model given deterministic parametric definition
        :param nints: 	    Size of intervals (at x=0)
        :param p: 	        Slopes
        :param vback: 	    Background velocity
        :param dv: 	        Changes in velocity
        :param rhoback: 	Background density
        :param drho: 	    Changes in density

        """

        self.int     = ints
        self.vback   = vback
        self.rhoback = rhoback

        self.p  = p
        self.dv = dv
        if len(drho) == 0:
            self.drho = 1000 * np.ones(len(self.int))
        else:
            self.drho = drho

        return


    def Stochastic(self, nint, p, vback, dv, rhoback=[1000,1000], drho=np.array([]), dint=[], flip=True):
        """
        Create dipping model given stochastic parametric definition
        :param nint: 	    Number of intervals
        :param dint: 	    Range of intervals [intmin,intmax] from which int is uniformly drawn
        :param p: 	        Slopes
        :param vback: 	    Range of background velocity [vmin    ,vmax]
        :param dv: 	        Range of velocity changes    [dvmin   ,dvmax]
        :param rhoback: 	Range of background density  [rhomin  ,rhomax]
        :param drho: 	    Range of density changes     [drhomin ,drhomax]
        """

        if len(dint) == 0:
            dint = [0, self.nz]

        # draw reflector positions
        nrefl = nint - 1
        refl  = np.floor(np.random.uniform(dint[0],dint[1],nrefl)) + 1
        refl  = np.sort(refl)

        self.int       = np.zeros(nint, dtype=np.int8)
        self.int[0]    = np.int8(refl[0])
        self.int[1:-1] = np.int8(np.diff(refl))
        self.int[-1]   = np.int8(self.nz - refl[-1])
        #print 'sum of ints:',np.sum(self.int)

        # draw dips positions
        dips = np.random.uniform(p[0], p[1], nint)
        self.p = np.sort(dips)

        # draw velocity and density
        self.vback = np.round(np.random.uniform(vback[0],vback[1]))
        self.vback = np.round(np.random.uniform(rhoback[0],rhoback[1]))

        self.dv    = np.round(np.random.uniform(dv[0],dv[1],nint))

        if len(drho) == 0:
            self.drho = 1000 * np.ones(nint)
        else:
            self.drho = np.round(np.random.uniform(drho[0],drho[1],nint))

        self.flip=flip

        #print 'int',self.int
        #print 'v',self.v
        #print 'rho',self.rho

        return


    def Apply(self):
        """
        Apply dipping layers modelling
        """

        self.V   = self.vback*np.ones((self.nz,self.nx))
        self.Rho = self.vback*np.ones((self.nz,self.nx))

        intercepts = np.cumsum(self.int)

        for iint in range(len(self.int)):

            V   = np.zeros((self.nz,self.nx))
            Rho = np.zeros((self.nz,self.nx))

            for ix in range(self.nx):
                intercept = int(np.round(intercepts[iint] + ix*self.p[iint]))
                V[intercept:,ix]   = self.dv[iint]
                Rho[intercept:,ix] = self.drho[iint]

            self.V   = self.V   + V
            self.Rho = self.Rho + Rho

        if self.flip==True:
            if(np.random.rand()>0.5):
                self.V   = np.fliplr(self.V)
                self.Rho = np.fliplr(self.Rho)

        return




class FaultModel(GeologicalModelling):
    """
    Class for creating fault model

    Returns: a GeologicalModelling object

    """
    def __init__(self, par):
        par['type'] = 'fault'
        GeologicalModelling.__init__(self, par)
        self.flip = False

    def Stochastic(self, nint, dv, drho=[], dint=[], dfaultlim=[], doffset=[]):
        """
        Create fault model given stochastic parametric definition
        :param nint: 	    Number of intervals
        :param dint: 	    Range of intervals [intmin,intmax] from which int is uniformly drawn
        :param dv: 	        Range of velocities [vmin,vmax] from which v is uniformly drawn
        :param drho: 	    Range of densities  [vmin,vmax] from which rho is uniformly drawn
        :param doffset: 	Range of offsets  [offsetmin,offsetmax] from which offset is uniformly drawn
        :param dfaultlim: 	Range of faultlim  [faultlimmin,defaultlimmax] from which faultlim is uniformly drawn
        """

        if len(dint)==0:
            dint=[0,self.nz]

        if len(doffset)==0:
            doffset=[0,self.nz-1]

        if len(dfaultlim)==0:
            dfaultlim=[0,self.nz-1]

        # IMPORTANT
        # Probably, I could just use the LayerdModel class here.

        # draw reflector positions
        nrefl = nint - 1
        refl  = np.floor(np.random.uniform(dint[0],dint[1],nrefl)) + 1
        refl  = np.sort(refl)

        self.int       = np.zeros(nint, dtype=np.int8)
        self.int[0]    = np.int8(refl[0])
        self.int[1:-1] = np.int8(np.diff(refl))
        self.int[-1]   = np.int8(self.nz - refl[-1])
        #print 'sum of ints:',np.sum(self.int)

        # draw velocity and density
        self.v = np.round(np.random.uniform(dv[0],dv[1],nint))
        if len(drho) == 0:
            self.rho = 1000 * np.ones(nint)
        else:
            self.rho = np.round(np.random.uniform(drho[0],drho[1],nint))

        #print 'int',self.int
        #print 'v',self.v
        #print 'rho',self.rho

        # Make a line with "num" points...
        x0, z0 = np.floor(np.random.uniform(dfaultlim[0],dfaultlim[1])), 0 # These are in _pixel_ coordinates!!
#        x1, z1 = np.floor(np.random.uniform(dfaultlim[0],dfaultlim[1])), 99

        #
        x1, z1 = np.floor(np.random.uniform(x0,dfaultlim[1])), 99
        self.x, self.z = np.linspace(x0, x1, self.nx, dtype=np.int), np.linspace(z0, z1, self.nz)

        # Offset
        self.offset = np.int(np.floor(np.random.uniform(doffset[0],doffset[1])))

        return


    def Apply(self):
        """
        Apply dipping layers modelling
        """

        v   = self.v[0]  * np.ones(self.int[0])
        rho = self.rho[0]* np.ones(self.int[0])

        for iint in range(1,len(self.int)):
            v   = np.hstack((v,   self.v[iint]  * np.ones(self.int[iint])))
            rho = np.hstack((rho, self.rho[iint]* np.ones(self.int[iint])))

        self.V   = np.repeat(v[:, np.newaxis],   self.nx, axis=1)
        self.Rho = np.repeat(rho[:, np.newaxis], self.nx, axis=1)


        mask0 = np.ones_like(self.V, dtype=np.int)
        mask1 = np.ones_like(self.V, dtype=np.int)
        for i in range(self.nz):
            mask0[i, self.x[i]:] = 0

        mask1 = mask1 - mask0

        self.V = self.V*mask0 + np.roll(self.V, self.offset, 0)*mask1

        return

class WedgeModel(GeologicalModelling):
    """
    Class for creating wedge model

    Returns: a GeologicalModelling object

    """


class TrapModel(GeologicalModelling):
    """
    Class for creating trap model

    Returns: a GeologicalModelling object

    """


if __name__ == "__main__":

    # Test deterministic method - layered model
    ints = np.array([10, 20, 50, 10])
    v = np.array([1500, 1800, 2000, 2500])
    rho = np.array([1000, 1800, 1400, 1200])

    Layers = LayeredModel({'dims': [np.sum(ints), 100], 'type': 'layer'})
    Layers.Deterministic(ints,v,rho)
    Layers.Apply()

    Layers.Visualize(figsize=(12, 7))

    filepath='/Users/matteoravasi/PycharmProjects/Seismic_Recognition/datasets/synthetics/'
    filename='layer'

    Layers.Save(filepath=filepath, filename=filename)


    # Test stochastic method - layered model
    dv   = [1500,2000]
    drho = [1000,1800]
    nint = 3
    Layers = LayeredModel({'dims': [100, 100], 'type': 'layer'})
    Layers.Stochastic(nint,dv,drho)
    Layers.Apply()

    Layers.Visualize(figsize=(12, 7))

    filepath = '/Users/matteoravasi/PycharmProjects/Seismic_Recognition/datasets/seismic/synthetics/'
    filename = 'layerrdn'

    Layers.Save(filepath=filepath, filename=filename)



    # Test deterministic method - dipping model
    vback   = 1500
    rhoback = 1000
    ints    = np.array([10,  20,   50,   10])
    p       = np.array([0,   0.1,  0.3, -0.1])
    dv      = np.array([150, 100,  200,  50])
    drho    = np.array([100, 180,  10,   120])

    Layers = DippingModel({'dims': [np.sum(ints), 100], 'type': 'dipping'})
    Layers.Deterministic(ints, p, vback, dv, rhoback, drho)
    Layers.Apply()

    Layers.Visualize(figsize=(12, 7))


    # Test stochastic method - dipping model
    vback   = [1500,1800]
    rhoback = [1000,1200]
    nint    = 3
    p       = [0,0.2]
    dv      = [-150,150]
    drho    = [-100,100]

    Layers = DippingModel({'dims': [np.sum(ints), 100], 'type': 'dipping'})
    Layers.Stochastic(nint, p, vback, dv, rhoback, drho, flip=True)
    Layers.Apply()

    Layers.Visualize(figsize=(12, 7))

plt.show()
