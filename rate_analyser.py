import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from time import time,ctime
import sys

def norm(arr):
    return (arr-np.min(arr))/(np.max(arr)-np.min(arr))*255

def video_compat(arr):
    return    cv2.cvtColor(arr.astype(np.uint8), cv2.COLOR_GRAY2RGB)


file_path="data.avi"
output_dir="outputs/"+sys.argv[0].split("/")[-1].split(".")[0]
if not os.path.isdir(output_dir):
    os.makedirs(output_dir,exist_ok=True)
cap = cv2.VideoCapture(file_path)
video_diff_file_name=os.path.join(output_dir,"diff_"+ctime(time()).replace(":","_").replace(" ","_")+".avi")
video_z_file_name=os.path.join(output_dir,"Z_"+ctime(time()).replace(":","_").replace(" ","_")+".avi")
video_Z_mean_name=os.path.join(output_dir,"Z_mean_"+ctime(time()).replace(":","_").replace(" ","_")+".avi")
if (cap.isOpened()== False):
    raise NameError("[-] Error opening video stream or file")
    
video=[]
while(cap.isOpened()):
  ret, frame = cap.read()
  if ret == True:
    frame=cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    video.append(frame)

  else: 
    break

cap.release()
cv2.destroyAllWindows()
video=np.array(video,dtype=np.float32) #! if you keep this at uint8, when substracting, negative numbers will saturate. like -1 will become 255
video_len=video.shape[0]
diffrences=np.empty_like(video,dtype=np.float32) #!
size = (diffrences.shape[2],diffrences.shape[1])
FPS=5*2
video_diff=cv2.VideoWriter(video_diff_file_name,cv2.VideoWriter_fourcc(*'XVID'), FPS, size)
video_Z=cv2.VideoWriter(video_z_file_name,cv2.VideoWriter_fourcc(*'XVID'), FPS, size)
video_Z_mean=cv2.VideoWriter(video_Z_mean_name,cv2.VideoWriter_fourcc(*'XVID'), FPS, size)

for i in range(1,video_len):
    # diffrences[i,:,:]=np.abs(video[i,:,:].astype(np.float64)-video[i-1,:,:].astype(np.float64)).astype(np.uint8)
    diffrences[i,:,:]=np.abs(video[i,:,:]-video[i-1,:,:])
    vid_tmp=diffrences[i,:,:].astype(np.uint8)
    vid_tmp=cv2.cvtColor(vid_tmp, cv2.COLOR_GRAY2RGB)
    video_diff.write(vid_tmp) #! video writer needs a 3D channel not a grayscale

video_diff.release()

mean=np.mean(diffrences,axis=0)
std=np.std(diffrences,axis=0)
cv2.imwrite(os.path.join(output_dir,'std.png'),std)
cv2.imwrite(os.path.join(output_dir,'mean.png'),mean)
Z=np.empty_like(diffrences,dtype=np.float32) 

for i in range(0,video_len):
    Z[i,:,:]=(diffrences[i,:,:]-mean)/std #! calculating Z score
    Z[i,:,:]=np.abs(Z[i,:,:]) #! avoiding negative Z score
# Z=Z/np.max(Z[:])*255 #! for visulization
Z=norm(Z)
for i in range(0,video_len):
    video_Z.write(video_compat(Z[i,:,:]))
    acc= np.mean(Z[i-min(i,5):i,:,:],axis=0)    
    video_Z_mean.write(video_compat(acc))
video_Z.release()
video_Z_mean.release()
Z_mean=np.mean(Z,axis=0)
Z_std=np.std(Z,axis=0)
cv2.imwrite(os.path.join(output_dir,'Z_std.png'),Z_std)
cv2.imwrite(os.path.join(output_dir,'Z_mean.png'),Z_mean)


print("[+] bye!")

