import os
import cv2

def crop_images(im_frames_path):
    print("[+] cropping image")
    imgs=os.listdir(im_frames_path)
    for img in imgs:
        im_data=cv2.imread(im_frames_path+"/"+img)
        # im_data=im_data[0:1080,0:1080,:]
        im_data=im_data[0:512,0:512,:]
        cv2.imwrite(im_frames_path+"/"+img,im_data)
        
crop_images("data/frames")
path="/home/arash/Desktop/workdir/RoboRoyal/markerless_tracking_paper/markless_tracking_my_version/static/png"
crop_images(path)
