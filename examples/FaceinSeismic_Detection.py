# Face recognition in seismic image
#
# Authors: C. Birnie, M. Ravasi

import cv2

path_conda   = '/Users/matteoravasi/anaconda/'
path_opencv  = path_conda+'share/OpenCV/haarcascades/'
face_cascade = cv2.CascadeClassifier(path_opencv+'haarcascade_frontalface_default.xml')

imgnames     = ['imagetest_withclaire.png','imagetest_withclaire1.png',\
                'imagetest_withclaire2.png','imagetest_withclaire3.png']

#cv2.startWindowThread()

for imgname in imgnames:

    img=cv2.imread('datasets/seismic/real/'+imgname,1)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    faces   = face_cascade.detectMultiScale(gray, 1.03, 3)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h), (255,0,0),2)


    cv2.imshow(imgname,img)

    k=cv2.waitKey(0)

cv2.destroyAllWindows()