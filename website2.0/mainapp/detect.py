import cv2
from django.conf import settings
from django.core.files import File
from .utils import desectpath, url_to_img
import urllib

def detectfeatures2(model):

    img = url_to_img(model.picture.url)
    height, width, channels = img.shape

    if width > 800:
        newheight = int(800*height/width)
        img = cv2.resize(img,(800, newheight), interpolation = cv2.INTER_AREA)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    mi = model.minsize * min(height,width) / 100
    ma = max(model.maxsize * min(height, width) / 100, mi)

    path_cascade  = settings.BASE_DIR+'/mainapp/static/mainapp/assets/haarcascades/'
    font = cv2.FONT_HERSHEY_DUPLEX

    if model.face == True:
        face_cascade = cv2.CascadeClassifier(path_cascade+'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray,scaleFactor=model.scale,minNeighbors=model.neighbors,
            maxSize=(ma,ma),minSize=(mi,mi))
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),6)
            cv2.rectangle(img, (x+ w/2, y + h/2), (x + w/2+1, y + h/2 + 1), (255, 0, 0), 6)
            cv2.putText(img,'face',(x,y),font,2,(255,0,0),2)

    if model.bottle == True:
        bottle_cascade = cv2.CascadeClassifier(path_cascade+'bottle_7stagecascade.xml')
        bottles = bottle_cascade.detectMultiScale(gray,scaleFactor=model.scale,minNeighbors=model.neighbors,
            maxSize=(ma,ma),minSize=(mi,mi))
        for (x,y,w,h) in bottles:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),6)
            cv2.rectangle(img, (x+ w/2, y + h/2), (x + w/2+1, y + h/2 + 1), (0, 255, 0), 6)
            cv2.putText(img,'bottle',(x,y),font,2,(0,255,0),2)

    if model.fault == True:
        fault_cascade = cv2.CascadeClassifier(path_cascade+'fault_cascades.xml')
        faults = fault_cascade.detectMultiScale(gray,scaleFactor=model.scale,minNeighbors=model.neighbors,
            maxSize=(ma,ma),minSize=(mi,mi))
        for (x,y,w,h) in faults:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),6)
            cv2.rectangle(img, (x+ w/2, y + h/2), (x + w/2+1, y + h/2 + 1), (0, 0, 255), 6)
            cv2.putText(img,'fault',(x,y),font,2,(0,0,255),2)

    if model.trap == True:
        trap_cascade = cv2.CascadeClassifier(path_cascade+'trap_3stagecascade.xml')
        traps = trap_cascade.detectMultiScale(gray,scaleFactor=model.scale,minNeighbors=model.neighbors,
            maxSize=(ma,ma),minSize=(mi,mi))
        for (x,y,w,h) in traps:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),6)
            cv2.rectangle(img, (x+ w/2, y + h/2), (x + w/2+1, y + h/2 + 1), (255, 255, 255), 6)
            cv2.putText(img,'trap',(x,y),font,2,(255,255,255),2)

    _,filename,_ = desectpath(model.picture.url)
    tempfile = settings.BASE_DIR + '/media/mainapp/temp.jpg'
    cv2.imwrite(tempfile, img)

    content = urllib.urlretrieve(tempfile)
    model.resultfile.save(filename+'.jpg', File(open(content[0])), save=True)

    return

def detectfeatures(path,cascades,scale_fact=1.2,nbrs=3,minsize=00,maxsize=100):

	print "starting detection with reading image..."
	
	img = cv2.imread(settings.BASE_DIR+path)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	height, width, channels = img.shape
	
	if width > 800:
		newheight = int(800*height/width)
		img = cv2.resize(img,(800, newheight), interpolation = cv2.INTER_AREA)

	mi = minsize * min(height,width) / 100
	ma = max(maxsize * min(height, width) / 100, mi)

	path_cascade  = settings.BASE_DIR+'/mainapp/static/mainapp/assets/haarcascades/'
	font = cv2.FONT_HERSHEY_DUPLEX
	
	if cascades['face'] == True:
		face_cascade = cv2.CascadeClassifier(path_cascade+'haarcascade_frontalface_default.xml')
		faces = face_cascade.detectMultiScale(gray,scaleFactor=scale_fact,minNeighbors=nbrs,maxSize=(ma,ma),minSize=(mi,mi))
		for (x,y,w,h) in faces:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),6)
			cv2.rectangle(img, (x+ w/2, y + h/2), (x + w/2+1, y + h/2 + 1), (255, 0, 0), 6)
			cv2.putText(img,'face',(x,y),font,2,(255,0,0),2)

	if cascades['bottle'] == True:
		bottle_cascade = cv2.CascadeClassifier(path_cascade+'bottle_7stagecascade.xml')
		bottles = bottle_cascade.detectMultiScale(gray,scaleFactor=scale_fact,minNeighbors=nbrs,maxSize=(ma,ma),minSize=(mi,mi))
		for (x,y,w,h) in bottles:
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),6)
			cv2.rectangle(img, (x+ w/2, y + h/2), (x + w/2+1, y + h/2 + 1), (0, 255, 0), 6)
			cv2.putText(img,'bottle',(x,y),font,2,(0,255,0),2)

	if cascades['fault'] == True:
		fault_cascade = cv2.CascadeClassifier(path_cascade+'fault_cascades.xml')
		faults = fault_cascade.detectMultiScale(gray,scaleFactor=scale_fact,minNeighbors=nbrs,maxSize=(ma,ma),minSize=(mi,mi))
		for (x,y,w,h) in faults:
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),6)
			cv2.rectangle(img, (x+ w/2, y + h/2), (x + w/2+1, y + h/2 + 1), (0, 0, 255), 6)
			cv2.putText(img,'fault',(x,y),font,2,(0,0,255),2)

	if cascades['trap'] == True:
		trap_cascade = cv2.CascadeClassifier(path_cascade+'trap_3stagecascade.xml')
		traps = trap_cascade.detectMultiScale(gray,scaleFactor=scale_fact,minNeighbors=nbrs,maxSize=(ma,ma),minSize=(mi,mi))
		for (x,y,w,h) in traps:
			cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,255),6)
			cv2.rectangle(img, (x+ w/2, y + h/2), (x + w/2+1, y + h/2 + 1), (255, 255, 255), 6)
			cv2.putText(img,'trap',(x,y),font,2,(255,255,255),2)
	
	
	fname = path.split('.')
	ext = fname[-1]
	filename = ('.').join(fname[:-1])
	returnpath = settings.BASE_DIR + filename + "_detected.jpg" 
	print returnpath
	cv2.imwrite(returnpath, img)

	return returnpath

