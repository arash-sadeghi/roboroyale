import os
import cv2
import numpy as np
def blueize(im_frames_path):
    print("[+] bluing image")
    imgs=os.listdir(im_frames_path)
    for img in imgs:
        im_data=cv2.imread(im_frames_path+"/"+img,0)
        im_data=cv2.equalizeHist(im_data)
        im_data_rgb=np.zeros((np.shape(im_data)[0],np.shape(im_data)[1],3))
        im_data_rgb[:,:,0]=im_data
        cv2.imwrite(im_frames_path+"/b"+img,im_data_rgb)
# blueize("data/frames")
