#importing necessary libraries
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.spatial import distance
import os
import face_recognition
import pickle
from sklearn.cluster import DBSCAN
from imutils import build_montages
from keras.applications import xception



def get_normalized(img):
    """
    return the histogram normalized image of parameter
    """
    yuv_img = cv2.cvtColor(img,cv2.COLOR_RGB2YUV)
    yuv_img[:,:,0] = cv2.equalizeHist(yuv_img[:,:,0])
    final_img = cv2.cvtColor(yuv_img,cv2.COLOR_YUV2RGB)
    norm_image = np.zeros(img.shape)
    norm_img = cv2.normalize(final_img,  norm_image, 0, 255, cv2.NORM_MINMAX)
    return norm_img

def create_dataset(face_1,face_2):
    """
    creates the dataset from face encodings of the images provided by the user in face_1 and face_2
    """
    data=[]
    model = Xception(weights="imagenet",include_top=False)
    #getting encodings for first set of images
    for (i,imagePath) in enumerate(face_1):
      print('Processing image {}/{}:'.format(i,len(face_1)))
      print(imagePath)
      #img = cv2.imread(imagePath)
      rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
      rgb = get_normalized(rgb)
      boxes = face_recognition.face_locations(rgb)
      encodings = face_recognition.face_encodings(rgb, boxes)
      d = [{"imagePath": imagePath, "loc": box, "encoding": enc}
           for (box, enc) in zip(boxes, encodings)]
           #as there can be multiple faces in an image,
           #unzipping them all and adding the encodings
      data.extend(d)
    #getting encodings for second set of images
    for (i,imagePath) in enumerate(face_2):
      print('Processing image {}/{}:'.format((i+1),len(face_2)))
      print(imagePath)
      #img = cv2.imread(imagePath)
      rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
      rgb = get_normalized(rgb)
      boxes = face_recognition.face_locations(rgb)
      encodings = face_recognition.face_encodings(rgb, boxes)
      d = [{"imagePath": imagePath, "loc": box, "encoding": enc}
           for (box, enc) in zip(boxes, encodings)]
           #as there can be multiple faces in an image,
           #unzipping them all and adding the encodings
      data.extend(d)
    print('Total faces detected from both sets of images:',len(data[0]['encoding']))
    return data
