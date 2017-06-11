#!/usr/bin/env python2.7

# Fault recognition in seismic image - to be run inside examples folder
#
# Authors: C. Birnie, M. Ravasi

import cv2

path_cascade  = '../datasets/seismic/synthetics/cascades/'
#trap_cascade = cv2.CascadeClassifier(path_cascade+'trap_3stagecascade.xml')
trap_cascade = cv2.CascadeClassifier(path_cascade+'trap_2stagecascadeEC2.xml')


# Trap on real data
imgname     = 'imagetest_withtrap.png'

img=cv2.imread('../datasets/seismic/synthetics/targets/'+imgname,1)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)

print 'apply trap_cascade'
traps     = trap_cascade.detectMultiScale(gray, scaleFactor=2, minNeighbors=10, maxSize=(40,40) , minSize=(35, 35))
#traps_big = trap_cascade.detectMultiScale(gray, scaleFactor=2, minNeighbors=10, maxSize=(400, 400), minSize=(205, 205))

for (x,y,w,h) in traps:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.rectangle(img, (x+ w/2, y + h/2), (x + w/2+1, y + h/2 + 1), (255, 0, 0), 2)

#for (x, y, w, h) in traps_big:
#    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#    cv2.rectangle(img, (x + w / 2, y + h / 2), (x + w / 2 + 1, y + h / 2 + 1), (0, 255, 0), 2)

cv2.imshow(imgname,img)

k=cv2.waitKey(0)





# Trap on synthetic data
imgnames     = ['synthetic_model1.png']

for imgname in imgnames:
    img=cv2.imread('../datasets/seismic/synthetics/targets/'+imgname,1)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    print 'apply trap_cascade'
    traps     = trap_cascade.detectMultiScale(gray, scaleFactor=1.4, minNeighbors=4, maxSize=(150,150) , minSize=(90, 90))

    for (x,y,w,h) in traps:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.rectangle(img, (x+ w/2, y + h/2), (x + w/2+1, y + h/2 + 1), (255, 0, 0), 2)

    cv2.imshow(imgname,img)

    k=cv2.waitKey(0)






cv2.destroyAllWindows()
