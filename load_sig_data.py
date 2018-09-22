import sys
import numpy as np
from scipy.misc import imread
import pickle
import os
import matplotlib.pyplot as plt
import argparse
import cv2 as cv
"""Script to preprocess the omniglot dataset and pickle it into an array that's easy
    to index my character type"""

parser = argparse.ArgumentParser()
parser.add_argument("--data",help="Path where signature images folder resides")
parser.add_argument("--save", help = "Path to pickle data to.", default=os.getcwd())
args = parser.parse_args()
data_path = args.data
save_path = args.save
resized_path = 'resized'
image_size = 105

def resize_images(path):
    for filename in os.listdir(path):
        if filename == '.DS_Store':
            continue
        image = cv.imread(os.path.join(path,filename))
        new_image = cv.resize(image,(image_size,image_size))
        print("resizing image: " + filename)
        cv.imwrite(os.path.join(save_path,resized_path,filename),new_image)


def loadimgs(path):
    #if data not already unzipped, unzip it.
    if not os.path.exists(path):
        print("unzipping")
        os.chdir(data_path)
        os.system("unzip {}".format(path+".zip" ))
    X=[]
    author_ids = []
    #we load every alphabet seperately so we can isolate them later
    for filename in os.listdir(path):
        if filename == '.DS_Store':
            continue
        #file_name format: authorid_orginialfilename_index.tif
        author_id = filename[:filename.find('_')]
        if author_id == 'Anonymous':
            continue
        image = imread(os.path.join(path,filename))
        X.append(image)
        author_ids.append(author_id)
    # X = np.stack(X)
    # author_ids = np.stack(author_ids)
    return X,author_ids

resize_images(data_path)
X,author_ids=loadimgs(os.path.join(save_path,resized_path))
with open(os.path.join(save_path,"sig_data.pickle"), "wb") as f:
	pickle.dump((X,author_ids),f)

# verify the pickled data
with open(os.path.join(save_path, "sig_data.pickle"), "rb") as f:
    (X,author_ids) = pickle.load(f)
    print("len of X {}".format(len(X)))
    print("shape of image 10: {}".format(X[9].shape))
    print("len of author_ids {}".format(len(author_ids)))
