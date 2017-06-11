#!/bin/bash

python Create_Seismic_Dictionary.py

python Seismic_HaarPreprocessing.py

python makeInfoLst.py

python Create_bg.py

