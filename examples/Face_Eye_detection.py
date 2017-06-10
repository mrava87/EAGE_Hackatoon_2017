#!/usr/bin/env python2.7

# Face recognition example from https://www.youtube.com/watch?v=88HdqNDQsEk
# and https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/
#
# Face recognition
#
# Authors: C. Birnie, M. Ravasi

import cv2
import numpy as np
import matplotlib.pyplot as plt

path_opencv  = '/Users/matteoravasi/anaconda/share/OpenCV/haarcascades/'
face_cascade = cv2.CascadeClassifier(path_opencv+'haarcascade_frontalface_default.xml')
eye_cascade  = cv2.CascadeClassifier(path_opencv+'haarcascade_eye.xml')
my_cascade = cv2.CascadeClassifier('../datasets/facerecognition/cascades/bottle_7stagecascade.xml')

cap = cv2.VideoCapture(0)

cv2.startWindowThread()
cv2.namedWindow("img")


ret,img=cap.read()
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#gray = cv2.equalizeHist(gray)

bottles = my_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=2)#maxSize=(30,30) , minSize=(30, 30), scaleFactor=1.3, minNeighbors=5
#if (len(bottles)>0):
#    print 'n bottles: %d' % (len(watches))
for (x, y, w, h) in bottles:
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

faces   = face_cascade.detectMultiScale(gray, 1.3, 5)
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h), (255,0,0),2)

    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

cv2.imshow('img',img)
k=cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()


"""
while True:
    ret,img=cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #gray = cv2.equalizeHist(gray)

    bottles = my_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=2)#maxSize=(30,30) , minSize=(30, 30), scaleFactor=1.3, minNeighbors=5
    #if (len(bottles)>0):
    #    print 'n bottles: %d' % (len(bottles))
    for (x, y, w, h) in bottles:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    faces   = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h), (255,0,0),2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    cv2.imshow('img',img)
    k=cv2.waitKey(30) & 0xff
    if k== ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
"""
