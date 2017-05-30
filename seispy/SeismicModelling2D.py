import numpy as np
import matplotlib.pyplot as plt
import scipy.misc as sp

import SeismicModelling as SM
import GeologicalModelling as GM

class SeismicModelling2D:
    """
	Class for creating 2D seismic gather from elastic parameters

	inputs:
	------

	V:            Velocity model [nt x nx]
	Rho:          Density  model  [nt x nx]
	t:            Time axis
	trick:        Ricker wavelet time axis
	f0:           Ricker wavelet central frequency


    functions:
    ----------

    Apply:             computes Seismic stack using convolutional model


    Returns: a SeismicModelling2D object

    """

    def __init__(self, par):
        self.V = par['V']
        self.Rho = par['Rho']

        self.nx = self.V.shape[1]
        self.dt = par['dt']
        self.ot = par['ot']
        self.nt = par['V'].shape[0]
        self.t = np.arange(self.nt) * self.dt + self.ot
        if 'ntrick' in par.keys():
            self.ntrick = par['ntrick']
        else:
            self.ntrick = self.nt
        self.f0 = par['f0']

        self.stack = np.zeros((self.nt,self.nx))

        return


    def Apply(self):
        """
        Apply seismic modelling
        """

        for ix in range(self.nx):
            par = {'V'     : self.V[:,ix],
                   'Rho'   : self.Rho[:,ix],
                   'dt'    : self.dt,
                   'ot'    : self.ot,
                   'ntrick': self.ntrick,
                   'f0'    : self.f0}

            Seismod = SM.SeismicModelling(par)
            Seismod.Apply()

            self.stack[:,ix] = Seismod.trace


    def Visualize(self, figsize=(12, 7), cbarlims=[0,0]):
        """
        Visualize Elastic parameters and seismic trace
        :param figsize: 	Figure size
        :param cbarlims: 	Colorbar extrems
        """

        if(cbarlims[1]-cbarlims[0]==0):
            cbarlims=[-np.max(np.abs(self.stack.flatten())),np.max(np.abs(self.stack.flatten()))]

        fig, ax = plt.subplots(1, 2, figsize=figsize)
        ax[0].imshow(self.V, interpolation='nearest')
        ax[0].set_title('Elastic parameters')
        ax[0].axis('tight')
        im = ax[1].imshow(self.stack, cmap='gray', vmin=cbarlims[0], vmax=cbarlims[1])
        ax[1].axis('tight')
        plt.colorbar(im)

        return


    def Save(self, filepath='./', filename='test', norm=1):
        """
        Save models in png files
        :param filepath: 	Path to save .png files
        :param filename: 	Prefix to give to .png files
        :param norm:        normalizing factor

        """

        stack_norm = (self.stack/norm + 1.) * (255./2)
        sp.toimage(stack_norm, cmin=0, cmax=255).save(filepath + filename + '_stack.png')

        # print 'max stack', np.max(self.stack.flatten())
        # print 'min stack', np.min(self.stack.flatten())

        # print 'max stack_norm', np.max(stack_norm.flatten())
        # print 'min stack_norm', np.min(stack_norm.flatten())

        return



if __name__ == "__main__":


    # Make layered model
    filepath = '/Users/matteoravasi/PycharmProjects/Seismic_Recognition/datasets/seismic/synthetics/'
    filename = 'layer'

    ints = np.array([100, 50, 80, 200])
    v    = np.array([1500, 1800, 2000, 2500])
    rho  = np.array([1000, 1800, 1400, 1200])

    Layers = GM.LayeredModel({'dims': [np.sum(ints), 100], 'type': 'layer'})
    Layers.Deterministic(ints,v,rho)
    Layers.Apply()
    Layers.Visualize(figsize=(12, 7))
    Layers.Save(filepath=filepath, filename=filename)

    # Create seismic stack
    Seismod = SeismicModelling2D({'V'  :     Layers.V,
                                  'Rho':     Layers.Rho,
                                  'dt' : 0.004, 'ot': 0,
                                  'ntrick':31, 'f0': 30})

    Seismod.Apply()
    Seismod.Visualize(figsize=(12, 7), cbarlims=[-6e12,6e12])
    Seismod.Save(filepath=filepath, filename=filename, norm=6e12)



    # Make stochastic layered models
    dv   = [1500, 2000]
    drho = [1000, 1800]
    nint = 3

    filepath = '/Users/matteoravasi/PycharmProjects/Seismic_Recognition/datasets/synthetics/'
    filename = 'layerrdn'

    for imod in range(5):
        Layers = GM.LayeredModel({'dims': [100, 100], 'type': 'layer'})
        Layers.Stochastic(nint, dv, drho)
        Layers.Apply()
        #Layers.Save(filepath=filepath, filename=filename+str(imod))

        # Create seismic stack
        Seismod = SeismicModelling2D({'V':     Layers.V,
                                      'Rho':   Layers.Rho,
                                      'dt' : 0.004, 'ot': 0,
                                      'ntrick':31,  'f0': 30})

        Seismod.Apply()
        Seismod.Visualize(figsize=(12, 7), cbarlims=[-6e12,6e12])
        Seismod.Save(filepath=filepath, filename=filename+str(imod), norm=6e12)

        imgpng = sp.imread(filepath+filename+str(imod)+'_stack.png', flatten=True)
        plt.figure()
        plt.imshow(imgpng, cmap='gray',vmin=0, vmax=255)


    # Make dipping model
    filepath = '/Users/matteoravasi/PycharmProjects/Seismic_Recognition/datasets/synthetics/'
    filename = 'dipping'

    vback   = 1500
    rhoback = 1000
    ints    = np.array([10, 20, 50, 10])
    p       = np.array([0, 0.1, 0.3, -0.1])
    dv      = np.array([150, 100, 200, 50])
    drho    = np.array([100, 180, 10, 120])

    Layers = GM.DippingModel({'dims': [np.sum(ints), 100], 'type': 'dipping'})
    Layers.Deterministic(ints, p, vback, dv, rhoback, drho)
    Layers.Apply()
    Layers.Save(filepath=filepath, filename=filename)

    # Create seismic stack
    Seismod = SeismicModelling2D({'V': Layers.V,
                                  'Rho': Layers.Rho,
                                  'dt': 0.004,  'ot': 0,
                                  'ntrick': 31, 'f0': 30})

    Seismod.Apply()
    Seismod.Visualize(figsize=(12, 7), cbarlims=[-6e12,6e12])
    Seismod.Save(filepath=filepath, filename=filename, norm=6e12)


plt.show()



