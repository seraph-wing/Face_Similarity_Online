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


def get_face_list(path):
    """
    returns a list of the path of all images available for processing
    """
    face_list = []
    for filename in os.listdir(path):
        if filename.endswith('jpg'):
          face_list.append(path+'/'+filename)
    return face_list

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

def create_dataset(face_list):
    """
    creates the dataset(list of dicts) from face encodings of the images provided
    by the user in which are path locations for images to be processed
    """
    data=[]
    d=[]
    #getting encodings for first set of images
    for (i,imagePath) in enumerate(face_list):
      print('Processing image {}/{}:'.format(i,len(face_list)))
      print(imagePath)
      #img = face_recognition.load_image_file(imagePath)
      img = cv2.imread(imagePath)
      #print(img.shape)
      #print("Image:",type(img))
      rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
      img = get_normalized(rgb)
      #print("Image:",type(img))
      boxes = face_recognition.face_locations(img)
      #print("Boxes: ",boxes)
      encodings = face_recognition.face_encodings(img, boxes)
      #print("Encodings: ",encodings)
      for (box, enc) in zip(boxes, encodings):
          d.append({"imagePath": imagePath, "loc": box, "encoding": enc})
      #print(d)
      data.extend(d)
    #print(len(data))
    #print('Total faces detected from both sets of images:',len(data[0]['encoding']))
    return data


def get_clustered_faces(data):
    """
    clustering all available faces from dataset created by create_dataset and building the montages for the clusters
    """
    clustered_faces = []
    encodings = [d["encoding"] for d in data]
    print("[INFO] Clustering...")
    clt = DBSCAN(eps = 0.5, metric ='euclidean')
    clt.fit(encodings)
    #finding number of unique faces found
    labelIDs = np.unique(clt.labels_)
    numUniqueFaces = len(np.where(labelIDs > -1)[0])
    print("[INFO] Number of unique faces: {}".format(numUniqueFaces))
    #================GETTING THE CLUSTERED FACES===============================
    for labelID in labelIDs:
      #print("[INFO] Faces for face ID :{}".format(labelID))
      indexes = np.where(clt.labels_ == labelID)[0]
      faces = []
      for i in indexes:
        image = cv2.imread(data[i]['imagePath'])
        (top,right, bottom,left) = data[i]['loc']
        face = image[top:bottom,left:right]
        #print(type(face))
        encoding = data[i]['encoding']
        d = {'face':face,'encoding':encoding}
        faces.append(d)#contains face+encoding of same cluster
      clustered_faces.append(faces)
    #==========CREATING THE MONTAGE========================
    montage_path = 'D:/Public projects/ML web apps/Face similarity/Face_Similarity_Online/face_similarity/media/montage'
    os.mkdir(montage_path)
    for labelID in labelIDs:
      #print(f'[INFO] faces for face ID {labelID}')
      idxs = np.where(clt.labels_ == labelID)[0]
      idxs = np.random.choice(idxs,size=min(25,len(idxs)),replace=False)
      faces = []
      for i in idxs:
        image = cv2.imread(data[i]['imagePath'])
        (top,right,bottom,left) = data[i]['loc']
        face = image[top:bottom, left:right]
        face = cv2.resize(face, (96,96))
        faces.append(face)
      montage = build_montages(faces,(96,96),(5,5))[0]
      #saving the montages in folders with their labelID so we can easily get the input and provide the score for the user
      image_name = 'montage_'+str(labelID)+'.jpg'
      cv2.imwrite(os.path.join(montage_path,image_name),montage)
      f = open('cluster_Data.pickle','wb+')
      f.write(pickle.dumps(clustered_faces))
      f.close()
    return clustered_faces


def get_similarity_score(clus_num1,clus_num2):
    """
    gets the final score by comparing the two clusters as provided by the user.
    """
    data_path = 'cluster_Data.pickle'
    data = pickle.loads(open(data_path, "rb").read())
    clustered_faces = np.array(data,dtype=object)

    face_list1 = clustered_faces[clus_num1]
    face_list2 = clustered_faces[clus_num2]
    distance_matrix = np.zeros((len(face_list1),len(face_list2)))
    for (i,img1) in enumerate(face_list1[:]):
      for (j,img2) in enumerate(face_list2[:]):
        distance_matrix[i][j] = distance.sqeuclidean(img1['encoding'],img2['encoding'])
    mean = np.mean(distance_matrix)
    #standardized_mean = (mean - distance_matrix.min())/(distance_matrix.max()-distance_matrix.min())
    return (1-mean)
