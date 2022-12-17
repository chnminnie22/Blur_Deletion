import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import argparse
from sklearn.model_selection import train_test_split
from math import *

#----------------- functions on a single image ----------------------------

def fix_size(image:np.array, expected_pixels: float = 2E6):
    '''
    Fixes all image size. Essentially scales down.
    '''
    ratio = np.sqrt(expected_pixels/(image.shape[0]*image.shape[1]))
    return cv.resize(image,(0,0), fx=ratio,fy=ratio)

def estimate_blur(img, threshold,kernel=None):
    '''
    Computes blur score by applying Laplacian filter OR provided kernel.
    '''
    if img.ndim == 3:
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        
    if kernel is None:
        blur_map = cv.Laplacian(img,cv.CV_64F)
    else:
        blur_map = cv.filter2D(img,-1,kernel,cv.CV_64F)
    
    score = np.var(blur_map)
    return blur_map, score, bool(score<threshold)

def pretty_blur_map(blur_map, sigma=5, min_abs=0.5):
    '''
    Creates monochrome blur map.
    '''
    abs_img = np.abs(blur_map).astype(np.float32)
    abs_img[abs_img < min_abs] = min_abs
    
    abs_image = np.log(abs_img)
    return cv.medianBlur(abs_image,sigma) 

def blurDetection(img,kernel=None):
    '''
    Calls the essential functions in tandem to perform overall blur detection on a single image.
    '''
    if img is None:
        print('error: no pic')
    img = fix_size(img)
    blur_map, score, blurry = estimate_blur(img, 100, kernel)
    prettyResult = pretty_blur_map(blur_map)
    return prettyResult, score, blurry
##--------------------- functions on a library of images-------------------------------------
def libraryDetection(path):
    '''
    Extracts all the images stored in given directory path.
    Perform blur detection the images and returns all relavent metrics.
    Input: path
    Output: labels 
    '''
    names = []
    img = []
    if os.path.isdir(path):
        for file in os.listdir(path):
            f = path+file
            pic = cv.imread(f)
            if pic is not None:
                names.append(f)
                img.append(pic[:,:,::-1])
    else:
        img.append(cv.imread(path)[:,:,::-1])
    
    # kernel = np.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]])
    kernel = None
    # kernel = np.array([[0,1,0],[1,-4,1],[0,1,0]])

    blur_maps, scores, labels = [],[],[]
    for p in img:
        b, s, l = blurDetection(p,kernel)
        blur_maps.append(b)
        scores.append(s)
        labels.append(l)
    return names, blur_maps, scores, labels

def deletion(library):
    '''
    Performs deletion on the detected blurry iamges.
    '''

    names, blur_maps, scores, labels = libraryDetection(library)
    print("Done with blur detection!")
    # sort the indices by score.
    idxs = {i:scores[i] for i in range(len(labels)) if labels[i]}
    sorted_idxs = sorted(idxs.keys(), key = lambda x : idxs[x])
    
    if len(idxs) == 0:
        print("Your library is clean of blurry photos. Nice! :)")
        return
    else:

        print(str(len(labels))+" images exists in the library provided.")
        print(str(len(sorted_idxs))+" images were detected to be blurry.")
        delete = displayBlur(sorted_idxs,names)
        
        if len(delete)==0:
            print("Ok, keep your blurry pics, I guess. :/")
            return
        
        y_n = userDelete(delete,names,library)

        if y_n == "y":
            print("Deletion in progress...")
            for d in delete:
                d = int(d)
                if d in sorted_idxs:
                    path = names[d]
                    print("Deleting "+names[d]+"...")
                    os.remove(path)
                else:
                    print("Error: Image "+d+" is an invalid input.")
            
            print("Deletion complete!")
        elif y_n == "n":
            print("Ok, keep your blurry pics, I guess. :/")
        else:
            print("Error: Invalid Input")

def displayBlur(sorted_idxs,names):
    rows = ceil(len(sorted_idxs)/3)
    count = 1
    delete = []
    for i in sorted_idxs:
        cv.imshow(names[i],cv.imread(names[i]))
        k = cv.waitKey(0)
        if k==ord("d"):
            delete+=[i]
        elif k==ord("a"):
            confirmAll = input("Whoa there, you sure you want to delete everything? y/n ")
            if confirmAll == "y":
                print("Love the confidence! Thank you for trusting us :) All blurry photos will be deleted.")
                delete = sorted_idxs
                cv.destroyAllWindows()
                break
            else:
                print("Ok, let's resume selection.")
        elif k==ord("s"):
            print("Phew, that sure is a lot of blurry photos. Deleting only photos that have been selected so far.")
            cv.destroyAllWindows()
            break
        cv.destroyAllWindows()
        count += 1
    plt.show()
    return delete

def userDelete(delete,names,library):
    print(str(len(delete))+" images were selected for deletion.")
    msg = "The following images were selected for deletion:\n"
    for d in delete:
        msg += names[d].replace(library,"")+"\n"
    
    y_n = input(msg+"CONFIRM DELETE? y/n ")
    return y_n

#----------- sys functions ----------------
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--images',type=str,required=True,help='directory of images')
    parser.add_argument('-s','--save-path',type=str,help='path to save output')
    parser.add_argument('-t','--threshold',type=float,default=100,nargs="?",help='blurry threshold')
    parser.add_argument('-d','--display',action='store_true',help='display images')
    return parser.parse_args()

if __name__ == '__main__':
    args = vars(parse_args())
    print("Loading..........")
    
    deletion(args['images'])
