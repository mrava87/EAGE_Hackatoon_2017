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

	fname = path.split('.')
	filename = ('.').join(fname[:-1])
	returnpath = settings.BASE_DIR + filename + "_detected.jpg" 

	cv2.imwrite(returnpath, img)

	return returnpath

def detectfeatures(path,cascades,scale_fact=1.2,nbrs=3,minsize=00,maxsize=100):

	img = cv2.imread(settings.BASE_DIR+path)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	height, width, channels = img.shape
	mi = minsize * min(height,width) / 100
	ma = max(maxsize * min(height, width) / 100, mi)

	path_cascade  = settings.BASE_DIR+'/mainapp/static/mainapp/assets/haarcascades/'
	font = cv2.FONT_HERSHEY_DUPLEX
	
	if cascades['face'] == True:
		face_cascade = cv2.CascadeClassifier(path_cascade+'haarcascade_frontalface_default.xml')
		faces = face_cascade.detectMultiScale(gray,scaleFactor=scale_fact,minNeighbors=nbrs,maxSize=(ma,ma),minSize=(mi,mi))
		for (x,y,w,h) in faces:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			cv2.putText(img,'face',(x,y),font,.7,(255,0,0),1)

	if cascades['bottle'] == True:
		bottle_cascade = cv2.CascadeClassifier(path_cascade+'bottle_7stagecascade.xml')
		bottles = bottle_cascade.detectMultiScale(gray,scaleFactor=scale_fact,minNeighbors=nbrs,maxSize=(ma,ma),minSize=(mi,mi))
		for (x,y,w,h) in bottles:
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
			cv2.putText(img,'bottle',(x,y),font,.7,(0,255,0),1)

	if cascades['fault'] == True:
		#fault_cascade = cv2.CascadeClassifier(path_cascade+'haarcascade_frontalface_default.xml')
		faults = fault_cascade.detectMultiScale(gray,scaleFactor=scale_fact,minNeighbors=nbrs,maxSize=(ma,ma),minSize=(mi,mi))
		for (x,y,w,h) in faults:
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
			cv2.putText(img,'fault',(x,y),font,.7,(0,0,255),1)

	if cascades['trap'] == True:
		trap_cascade = cv2.CascadeClassifier(path_cascade+'trap_3stagecascade.xml')
		traps = trap_cascade.detectMultiScale(gray,scaleFactor=scale_fact,minNeighbors=nbrs,maxSize=(ma,ma),minSize=(mi,mi))
		for (x,y,w,h) in traps:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)
			cv2.putText(img,'trap',(x,y),font,.7,(255,255,255),1)

	fname = path.split('.')
	filename = ('.').join(fname[:-1])
	returnpath = settings.BASE_DIR + filename + "_detected.jpg" 

	cv2.imwrite(returnpath, img)

	return returnpath
