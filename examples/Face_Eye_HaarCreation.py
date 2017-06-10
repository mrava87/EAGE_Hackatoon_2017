#!/usr/bin/env python2.7

# Face recognition example from https://www.youtube.com/watch?v=88HdqNDQsEk
# and https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/
#
# Haar cascade creation for recognition
#
# Authors: C. Birnie, M. Ravasi

import urllib
import cv2
import numpy as np
import os

def store_raw_images(url,directory, dims=(100,100)):
    print url
    print directory 
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    pic_num = len(os.listdir(directory)) + 1
    print pic_num
    
    neg_images_link = url
    neg_image_urls  = urllib.urlopen(neg_images_link).read().decode()
   
    for i in neg_image_urls.split('\n'):

        try:
            print(i)
            urllib.urlretrieve(i, directory+str(pic_num)+".jpg")
            img = cv2.imread(directory+str(pic_num)+".jpg",cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, dims)
            cv2.imwrite(directory+str(pic_num)+".jpg",resized_image)
            pic_num += 1
            
        except Exception as e:
            print(str(e))  
            

def find_uglies(directories):
#    match = False
    for file_type in directories:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))


def create_pos_n_neg():
    
    for file_type in ['neg','pos']:
        for img in os.listdir(file_type):
            
            if file_type == 'pos':
                line = file_type+'/'+img+' 1 0 0 50 50\n'
                with open('info.txt','a') as f:
                    f.write(line)
            elif file_type == 'neg':
                line = file_type+'/'+img+'\n'
                with open('bg.txt','a') as f:
                    f.write(line)

    
#store_raw_images('http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513','../datasets/facerecognition/neg/')
#store_raw_images('http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152','../datasets/facerecognition/neg/')
#store_raw_images('http://image-net.org/api/text/imagenet.synset.geturls?wnid=n04254680','../datasets/facerecognition/pos/', dims=(50,50))

#find_uglies(['../datasets/facerecognition/neg/','../datasets/facerecognition/pos/'])
create_pos_n_neg()
