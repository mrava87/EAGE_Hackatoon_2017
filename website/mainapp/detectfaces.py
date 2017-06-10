import cv2
from django.conf import settings

def detectfaces(path):

	img = cv2.imread(settings.BASE_DIR+path)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	path_cascade  = settings.BASE_DIR+'/mainapp/static/mainapp/assets/haarcascades/'
	face_cascade = cv2.CascadeClassifier(path_cascade+'haarcascade_frontalface_default.xml')

	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3)

	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

	returnpath = settings.BASE_DIR+path+"detected.jpg"

	cv2.imwrite(returnpath, img)

	return returnpath

