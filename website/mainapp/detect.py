import cv2
from django.conf import settings
from django.utils.text import slugify

def detectfaces(path):

	fname = path.split('.')
	filename = slugify(u'd'.join(fname[:-1]))

	img = cv2.imread(settings.BASE_DIR+path)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	path_cascade  = settings.BASE_DIR+'/mainapp/static/mainapp/assets/haarcascades/'
	face_cascade = cv2.CascadeClassifier(path_cascade+'haarcascade_frontalface_default.xml')

	faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=3)

	for (x,y,w,h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

	returnpath = settings.BASE_DIR + path + "_detected.jpg" 
	# if path = filename  the file gets lost ???

	cv2.imwrite(returnpath, img)

	return returnpath

def detectfeatures(path,cascades,scale_fact=1.3,neighbrs=3,minsize=50,maxsize=50):

	fname = path.split('.')
	filename = slugify(u'd'.join(fname[:-1]))

	img = cv2.imread(settings.BASE_DIR+path)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	height, width, channels = img.shape
	mi = minsize/100 * min(height,width)
	ma = max(maxsize/100 * min(height, width), minsz)

	path_cascade  = settings.BASE_DIR+'/mainapp/static/mainapp/assets/haarcascades/'
	
	if cascades['face'] == True:
		face_cascade = cv2.CascadeClassifier(path_cascade+'haarcascade_frontalface_default.xml')
		faces = face_cascade.detectMultiScale(gray, scale_fact, neighbrs, maxSize=(ma,ma) , minSize=(mi,mi))
		for (x,y,w,h) in faces:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

	if cascades['bottle'] == True:
		bottle_cascade = cv2.CascadeClassifier(path_cascade+'bottle_7stagecascade.xml')
		bottles = bottle_cascade.detectMultiScale(gray, scale_fact, neighbrs, maxSize=(ma,ma) , minSize=(mi,mi))
		for (x,y,w,h) in bottles:
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

	if cascades['fault'] == True:
		#fault_cascade = cv2.CascadeClassifier(path_cascade+'haarcascade_frontalface_default.xml')
		faults = fault_cascade.detectMultiScale(gray, scale_fact, neighbrs, maxSize=(ma,ma) , minSize=(mi,mi))
		for (x,y,w,h) in faults:
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

	if cascades['trap'] == True:
		trap_cascade = cv2.CascadeClassifier(path_cascade+'trap_3stagecascade.xml')
		traps = trap_cascade.detectMultiScale(gray, scale_fact, neighbrs, maxSize=(ma,ma) , minSize=(mi,mi))
		for (x,y,w,h) in traps:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),2)


	returnpath = settings.BASE_DIR + path + "_detected.jpg" 
	# if path = filename  the file gets lost ???

	cv2.imwrite(returnpath, img)

	return returnpath
