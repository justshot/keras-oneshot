import sys
import numpy as np
from scipy.misc import imread
import pickle
import os
import glob
import matplotlib.pyplot as plt
import argparse
import cv2 as cv
"""Script to preprocess the omniglot dataset and pickle it into an array that's easy
    to index my character type"""

parser = argparse.ArgumentParser()
parser.add_argument("--data",help="Path where signature images folder resides")
parser.add_argument("--save_file", help = "pickle file name")
args = parser.parse_args()
data_path = args.data
save_file_name = args.save_file

save_path = os.getcwd()
resized_path = 'resized'
image_size = 105

def clear_resize_folder():
    files = glob.glob(os.path.join(save_path,resized_path))
    for f in files:
        os.remove(f)

def resize_images(input_path):
    for filename in os.listdir(input_path):
        if filename == '.DS_Store':
            continue
        image = cv.imread(os.path.join(input_path,filename))
        new_image = cv.resize(image,(image_size,image_size))
        cv.imwrite(os.path.join(save_path,resized_path,filename),new_image)


def loadimgs(path):
    #if data not already unzipped, unzip it.
    if not os.path.exists(path):
        print("unzipping")
        os.chdir(data_path)
        os.system("unzip {}".format(path+".zip" ))
    X=[]
    author_dict = {}
    #we load every alphabet seperately so we can isolate them later
    for filename in os.listdir(path):
        if filename == '.DS_Store':
            continue
        #file_name format: authorid_orginialfilename_index.tif
        author_id = filename[:filename.find('_')]
        if author_id == 'Anonymous':
            continue
        image = cv.imread(os.path.join(path,filename),0)
        X.append(image)
        update_author_dict(author_dict, author_id, len(X) - 1)
    # X = np.stack(X)
    # author_ids = np.stack(author_ids)
    return X,author_dict

def update_author_dict(author_dict, author_id, index):
    if(author_dict.get(author_id) == None):
        author_dict[author_id] = []
    author_dict[author_id].append(index)

if __name__ == '__main__':

    resize_images(data_path)
    X,author_ids=loadimgs(os.path.join(save_path,resized_path))
    with open(os.path.join(save_path,save_file_name), "wb") as f:
        pickle.dump((X,author_ids),f)

    # verify the pickled data
    with open(os.path.join(save_path, save_file_name), "rb") as f:
        (X_loaded,author_dict_loaded) = pickle.load(f)
        print("len of X_loaded {}".format(len(X_loaded)))
        print("shape of image 10: {}".format(X_loaded[9].shape))
        print("len of author_dict_loaded {}".format(len(author_dict_loaded)))
        for author_id, sigs in author_dict_loaded.items():
            print("{}: {}".format(author_id, len(sigs)))