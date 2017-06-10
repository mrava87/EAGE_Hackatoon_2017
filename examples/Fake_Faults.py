#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 10:54:42 2017

@author: Filippo Broggini
"""

# %%

import sys

sys.dont_write_bytecode = True

import numpy as np
import scipy.misc as sp

import matplotlib.pyplot as plt

import seispy.GeologicalModelling as GM
import seispy.SeismicModelling2D  as SM



# %%

xdim = 100
zdim = 100

offset = 10

# Test deterministic method - layered model
ints0 = np.array([10, 20, 50, 20])
ints1 = ints0 + np.array([-offset, 0, 0, +offset])
v0 = v1 = np.array([1500, 1800, 2000, 2500])
rho0 = rho1 = np.array([1000, 1800, 1400, 1200])

Layers0 = GM.LayeredModel({'dims': [np.sum(ints0), xdim], 'type': 'layer'})
Layers0.Deterministic(ints0,v0,rho0)
Layers0.Apply()

Layers0.Visualize(figsize=(12, 7))

Layers1 = GM.LayeredModel({'dims': [np.sum(ints1), xdim], 'type': 'layer'})
Layers1.Deterministic(ints1,v1,rho1)
Layers1.Apply()

Layers1.Visualize(figsize=(12, 7))

plt.show()

# %% Define fault
# Make a line with "num" points...
x0, z0 = 40, 0 # These are in _pixel_ coordinates!!
x1, z1 = 60, 99
num = 100
x, z = np.linspace(x0, x1, num, dtype=np.int), np.linspace(z0, z1, num)

mask0 = np.ones_like(Layers0.V, dtype=np.int)
mask1 = np.ones_like(Layers0.V, dtype=np.int)
for i in range(zdim):
    mask0[i, x[i]:] = 0

mask1 = mask1 - mask0

plt.imshow(mask0)
plt.colorbar()
plt.show()
plt.imshow(mask1)
plt.show()
# Extract the values along the line
#zi = z[x.astype(np.int), y.astype(np.int)]

# %% Combine models

dv   = [1500,2000]
drho = [1000,1800]
nint = 4
Layers3 = GM.FaultModel({'dims': [100, 100], 'type': 'layer'})
Layers3.Stochastic(nint,dv,drho)
Layers3.Apply()

plt.imshow(Layers3.V)
#plt.plot(x,z, color='k')

# %%

Layers0 = GM.LayeredModel({'dims': [np.sum(ints0), xdim], 'type': 'layer'})
Layers0.Deterministic(ints0,v0,rho0)
Layers0.Apply()

Layers0.Visualize(figsize=(12, 7))

# %%
filepath='/home/bfilippo/Work/EAGE_Hackatoon_2017/datasets/faults/'
filename='fault'

#Layers.Save(filepath=filepath, filename=filename)

plt.show()