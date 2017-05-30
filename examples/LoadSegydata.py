# Import and visualize real data

import segyio
import numpy as np
import scipy.misc as sp

import matplotlib.pyplot as plt


f = segyio.open('../dataset/seismic/real/Kerry3D.segy')
d = np.reshape(f.trace.raw[:],(287,735,1252))

plt.figure()
plt.imshow(d[130,:,:].T, cmap='gray')
plt.axis('tight')

plt.figure()
plt.imshow(d[:,350,:].T, cmap='gray')
plt.axis('tight')


plt.figure()
plt.imshow(d[0:100,350,0:100,].T, cmap='gray', interpolation='None')
plt.axis('tight')

plt.show()
