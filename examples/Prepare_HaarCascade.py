#!/usr/bin/env python2.7
# Run workflow for data creation and  preparation for HaarCascade - to be run in examples
import os,sys,inspect

from Create_Seismic_Dictionary import Create_Seismic_Dictionary
from Seismic_HaarPreprocessing import preprocessing
from Create_bg import create_bg
from makeInfoLst import makeInfoLst

models     = ['flat','dip','wedge','fault','trap']
models_dir = '/datasets/seismic/synthetics_test/'

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


# Choose steps to run
Create_Seismic_flag = True
Preprocessing_flag  = True
Create_bg_flag      = True
Create_list_flag    = True



# Make seismic data
if Create_Seismic_flag: Create_Seismic_Dictionary(directory  = os.path.dirname(currentdir)+models_dir, \
                              					  models     = models, \
                            					  nsubmodels = 5000, \
												  moddims    = [100, 100], \
                                                  norm_seismic = 6e12)

# Preprocess data for image recognition
if Preprocessing_flag: preprocessing(models=models, basedir=os.path.dirname(currentdir)+models_dir, size=(35,35))


# Create background files
if Create_bg_flag: 
	create_bg('dip',   basedir=os.path.dirname(currentdir)+models_dir, n=600)
	create_bg('flat',  basedir=os.path.dirname(currentdir)+models_dir, n=600)
	create_bg('fault', basedir=os.path.dirname(currentdir)+models_dir, n=600)
	create_bg('trap',  basedir=os.path.dirname(currentdir)+models_dir, n=600)
	create_bg('wedge', basedir=os.path.dirname(currentdir)+models_dir, n=600)


# Create positive
if Create_list_flag: 
	makeInfoLst(pos_model='dip',   basedir=os.path.dirname(currentdir)+models_dir, figsize=[35, 35])
	makeInfoLst(pos_model='flat',  basedir=os.path.dirname(currentdir)+models_dir, figsize=[35, 35])
	makeInfoLst(pos_model='fault', basedir=os.path.dirname(currentdir)+models_dir, figsize=[35, 35])
	makeInfoLst(pos_model='trap',  basedir=os.path.dirname(currentdir)+models_dir, figsize=[35, 35])
	makeInfoLst(pos_model='wedge', basedir=os.path.dirname(currentdir)+models_dir, figsize=[35, 35])
