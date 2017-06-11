#!/usr/bin/env python2.7

# Bottle recognition example from https://www.youtube.com/watch?v=88HdqNDQsEk
# and https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/
#
# Face recognition
#
# Authors: C. Birnie, M. Ravasi

import cv2
import numpy as np
import matplotlib.pyplot as plt

my_cascade = cv2.CascadeClassifier('../datasets/facerecognition/cascades/bottle_7stagecascade.xml')


cv2.startWindowThread()
cv2.namedWindow("img")


img=cv2.imread('../datasets/facerecognition/targets/bottles_detection.png')

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#gray = cv2.equalizeHist(gray)

bottles = my_cascade.detectMultiScale(gray, scaleFactor=1.03, minNeighbors=3, minSize=(40, 40), maxSize=(150,150) )
for (x, y, w, h) in bottles:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow('img',img)
k=cv2.waitKey(0)

cv2.destroyAllWindows()
