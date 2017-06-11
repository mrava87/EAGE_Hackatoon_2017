#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 10 10:54:42 2017

@author: Filippo Broggini
"""

# %%

#%load_ext autoreload
#%autoreload 2

# %%

import sys

#sys.dont_write_bytecode = True

import numpy as np
import scipy.misc as sp

import matplotlib.pyplot as plt

import seispy.GeologicalModelling as GM
import seispy.SeismicModelling2D  as SM

# %% Layered model - Deterministic

ints = np.array([20, 30, 40, 20, 10, 20, 18, 35])
v = np.array([1500, 2000, 1500, 1800, 2000, 2200, 2500, 2100])
rho = v*0.6
Layers0 = GM.LayeredModel({'dims': [np.sum(ints), 1000], 'type': 'layer'})
Layers0.Deterministic(ints,v,rho)
Layers0.Apply()

plt.imshow(Layers0.V)
plt.colorbar()

# %% Fault model - Deterministic

ints = np.array([20, 30, 60, 20, 20, 18, 35])
v = np.array([1500, 2000, 1500, 1800, 2000, 2500, 2100])
rho = v*0.6
faultlim = [400,600]
offset = 50
Fault0 = GM.FaultModel({'dims': [np.sum(ints), 1000], 'type': 'layer'})
Fault0.Deterministic(ints,v,rho,faultlim=faultlim,offset=offset)
Fault0.Apply()

plt.imshow(Fault0.V)
plt.colorbar()

# %% Trap model - Deterministic
perc = 0
center_x = 50
center_z = np.array([80, 90])
v = np.array([0, 600, 0])
rho = v*0.6
Trap0 = GM.TrapModel({'dims': [100, 100], 'type': 'trap'})
Trap0.Deterministic(center_x, center_z, v, rho, perc)
Trap0.Apply()

plt.imshow(Trap0.V)
plt.colorbar()

# %% Combine models

Fake = np.concatenate((Layers0.V, Fault0.V, Layers0.V), axis=0)
Fake[270:370, 600:700] = Fake[270:370, 600:700] + Trap0.V
Fake[400:500, 650:750] = Fake[400:500, 650:750] + Trap0.V
#Fake[300:400, 600:700] = Trap0.V

plt.figure(figsize=(12, 7))
plt.imshow(Fake)
plt.colorbar()
plt.show()

# %%

Seismod = SM.SeismicModelling2D({'V'      : Fake,
                                 'Rho'    : Fake*0.6,
                                 'dt'     : 0.004,
                                 'ot'     : 0,
                                 'ntrick' : 31,
                                 'f0'     : 10})

Seismod.Apply()
Seismod.Visualize(cbarlims=[-4e12,4e12])

sp.imsave('../datasets/seismic/synthetics/targets/synthetic_model.png',Seismod.stack)

# %%
#filepath='/home/bfilippo/Work/EAGE_Hackatoon_2017/datasets/faults/'
#filename='fault'
#
#Layers.Save(filepath=filepath, filename=filename)
#
#plt.show()