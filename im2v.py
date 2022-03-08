import os
import cv2 as cv
import numpy as np
from time import time,ctime
import signal


def signal_handler(sig, frame):
        print("[+] signal catched, saving acc")
        cv.imwrite(str(global_counter)+video_file_name[0:-4]+".jpg",acc)
        global_counter+=1
        i=input("do you wanna quit? [y/n]")
        if i=='y': 
            video.release()
            exit(0)

signal.signal(signal.SIGINT, signal_handler)
global_counter=0

im_path="/home/arash/Desktop/workdir/RoboRoyal/new_data/side1" # beggining should start with /
ims=os.listdir(im_path)
im0=cv.imread(im_path+'/'+ims[0])
size = (np.shape(im0)[1],np.shape(im0)[0])
FPS=5
video_file_name=ctime(time()).replace(":","_").replace(" ","_")+".avi"
video=cv.VideoWriter(video_file_name,cv.VideoWriter_fourcc(*'XVID'), FPS, size)
acc=np.zeros(np.shape(im0))
acc_ratio=1/len(ims)
for c,imn in enumerate(ims):
    im=cv.imread(im_path+'/'+imn)
    video.write(im)
    acc=(1-acc_ratio)*acc+acc_ratio*im
    print("[+] progress {:.2f}".format(c/len(ims)),end='\r')
video.release()
cv.imwrite(video_file_name[0:-4]+".jpg",acc)

