import numpy as np
import matplotlib.pyplot as plt


class SeismicModelling:
    """
    Class for creating seismic trace from elastic parameters

    inputs:
    ------

    V:            Velocity trace
    Rho:          Density trace
    t:            Time axis
    trick:        Ricker wavelet time axis
    f0:           Ricker wavelet central frequency

    functions:
    ----------

    AcousticImpedence: computes Acoustic Impedence trace
    Reflectivity:      computes Reflectivity
    Ricker:            generate Ricker wavelet
    SeismicTrace:      compute Seismic Trace using convolutional model


    Returns: a SeismicModelling object

    """

    def __init__(self, par):
        self.V   = par['V']
        self.Rho = par['Rho']

        self.dt  = par['dt']
        self.ot  = par['ot']
        self.nt  = len(par['V'])
        self.t   = np.arange(self.nt)*self.dt + self.ot
        if 'ntrick' in par.keys():
            self.ntrick = par['ntrick']
        else:
            self.ntrick = self.nt

        self.f0 = par['f0']

        return

    def AcousticImpedence(self):
        """
        Compute Acoustic Impedence trace
        :param V: 		Velocity trace
        :param Rho: 		Density trace
        :return: 		Acoustic impedence trace
        """
        self.AI = np.multiply(self.V, self.Rho)
        return

    def Reflectivity(self):
        """
        Compute Reflectivity trace
        :param r: 		Reflectivity trace
        """

        num = self.AI[1:] - self.AI[0:-1]
        den = self.AI[1:] + self.AI[0:-1]

        self.r     = np.zeros(self.nt)
        self.r[1:] = np.multiply(num, den)

        return

    def Ricker(self, ntrick=2**10):
        """
        Generate Ricker wavelet
        :param t: 		Time axis
        :param f0: 		Central frequency
        :return: 		Ricker wavelet
        """

        if ntrick<len(self.t):
            trick = self.t[:ntrick]
        else:
            trick = self.t

        self.w = (1 - 2 * (np.pi * self.f0 * trick) ** 2) * np.exp(-(np.pi * self.f0 * trick) ** 2)

        self.w = np.concatenate((np.flipud(self.w[1:]),self.w), axis=0)
        self.wcenter = np.argmax(np.abs(self.w))

        return


    def SeismicTrace(self):
        """
        Compute seismic trace: s(t) = r(t) * w(t)
        :param r: 		Reflectivity trace
        :param w:    	Wavelet
        :return: 		Seismic trace
        """
        self.trace = np.convolve(self.r, self.w, 'full')
        self.trace = self.trace[self.wcenter:(self.wcenter + len(self.r))]

        return


    def Apply(self):
        """
        Apply seismic modelling
        """
        self.AcousticImpedence()
        self.Reflectivity()
        self.Ricker(self.ntrick)
        self.SeismicTrace()

        return


    def Visualize(self, figsize=(12, 7)):
        """
        Visualize Elastic parameters and seismic trace
        :param figsize: 	Figure size
        """

        fig, ax = plt.subplots(1, 2, figsize=figsize)
        ax[0].plot(self.V, self.t, 'k', label='V')
        ax[0].plot(self.Rho, self.t, 'r', label='Rho')
        ax[0].set_ylabel('time')
        ax[0].set_title('Elastic parameters')
        ax[0].legend()
        ax[0].invert_yaxis()
        ax[1].plot(self.trace, self.t, 'r', label='Trace')
        ax[1].fill_betweenx(self.t, 0, self.trace, where=(self.trace > 0), color='r')
        ax[1].plot(self.r, self.t, 'k', label='Reflectivity')
        ax[1].set_ylabel('time')
        ax[1].set_title('Seismic')
        ax[1].legend()
        ax[1].invert_yaxis()

        return


if __name__ == "__main__":
    INT = np.array([100, 50, 80, 200])

    par = {'V'  : np.hstack((1500 * np.ones(INT[0]), 1800 * np.ones(INT[1]), 2000 * np.ones(INT[2]), 2500 * np.ones(INT[3]))),
           'Rho': np.hstack((1000 * np.ones(INT[0]), 1200 * np.ones(INT[1]), 1400 * np.ones(INT[2]), 1800 * np.ones(INT[3]))),
           'dt' : 0.004,
           'ot' : 0,
           'ntrick':31,
           'f0' : 10}

    Seismod = SeismicModelling(par)

    Seismod.Apply()
    Seismod.Visualize(figsize=(12, 7))

    plt.show()
