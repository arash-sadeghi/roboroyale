import os
import numpy as np
import sys
import cv2
import matplotlib.pyplot as plt
import random
from torch.nn import functional as F
import torch 
from scipy import ndimage
import math
from scipy.ndimage.interpolation import rotate
def manual_conv2d(inp,ker):
    inp=torch.tensor(im_cropped)
    inp=inp.reshape((1,1,inp.shape[0],inp.shape[1]))
    ker=torch.tensor(queen-np.mean(queen[:]))
    ker=ker.reshape((1,1,ker.shape[0],ker.shape[1]))
    out=F.conv2d(inp,ker)
    return out[0,0,:,:].numpy()


def put_in_canvas(queen,big_dim):
    fixed_queen_dim=queen.shape
    canvas=np.zeros((big_dim[0],big_dim[1]))
    queen_center=[0,0]
    queen_center[0]=(big_dim[0]-fixed_queen_dim[0])//2
    queen_center[1]=(big_dim[1]-fixed_queen_dim[1])//2
    canvas[ queen_center[0]:queen_center[0]+fixed_queen_dim[0] , queen_center[1]:queen_center[1]+fixed_queen_dim[1] ] = queen
    queen = np.copy(canvas)
    return queen

def ROT(inp,a):
    # return ndimage.rotate(inp, a)
    # a=np.radians(a)
    # m11 = math.cos(a)
    # m12 = math.sin(a)
    # m21 = -math.sin(a)
    # m22 = math.cos(a)
    # matrix = np.array([[m11, m12],
    #                       [m21, m22]], dtype=np.float64)
    # np.cross
    return rotate(inp,a,mode='nearest')

def generate_rotations(queen,rotations,big_dim,fixed_queen_dim,mask):
    out=np.zeros((len(rotations),big_dim[0],big_dim[1]))
    masks=np.zeros((len(rotations),big_dim[0],big_dim[1]))
    for c,v in enumerate(rotations):
        rotated = ROT(queen, v)
        rotated = rotated [ (rotated.shape[0]-big_dim[0])//2 : (rotated.shape[0]-big_dim[0])//2+big_dim[0] ,
         (rotated.shape[1]-big_dim[1])//2 : (rotated.shape[1]-big_dim[1])//2+big_dim[1]]

        rotated_mask = ROT(mask, v)

        rotated_mask = rotated_mask [ (rotated_mask.shape[0]-big_dim[0])//2 : (rotated_mask.shape[0]-big_dim[0])//2+big_dim[0] ,
         (rotated_mask.shape[1]-big_dim[1])//2 : (rotated_mask.shape[1]-big_dim[1])//2+big_dim[1]]

        out[c , 0:rotated.shape[0] , 0:rotated.shape[1] ] = rotated
        masks[c , 0:rotated.shape[0] , 0:rotated.shape[1] ] = rotated_mask

    return out , masks

def normalize(inp):
    return (inp-np.min(inp[:])) / (np.max(inp[:])-np.min(inp[:]))*255

if __name__=='__main__':
    # base_folder_path='Aug05-07_side1_rpi1_full_cut'
    # first_file_name='raw_hive1_rpi1_190805-001018-utc.jpg'

    # base_folder_path='/home/arash/Desktop/workdir/RoboRoyal/codes_for_roboroyale_gitlab/outputs/rosbag2videao_no_annotation/_cam1_main_camera_image_raw'
    base_folder_path="/home/arash/Desktop/workdir/RoboRoyal/codes_for_roboroyale_gitlab/outputs/rosbag2videao_no_annotation/_cam1_main_camera_image_rawwhycon"
    first_file_name='00000_cam1_main_camera_image_raw.png'

    output_dir="outputs/"+sys.argv[0].split("/")[-1].split(".")[0]
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir,exist_ok=True)    

    heatmaps="heatmaps"
    if not os.path.isdir(os.path.join(output_dir,heatmaps)):
        os.makedirs(os.path.join(output_dir,heatmaps),exist_ok=True)    

    queen_folder="queen_folder"
    if not os.path.isdir(os.path.join(output_dir,queen_folder)):
        os.makedirs(os.path.join(output_dir,queen_folder),exist_ok=True)    

    crop_folder="crop_folder"
    if not os.path.isdir(os.path.join(output_dir,crop_folder)):
        os.makedirs(os.path.join(output_dir,crop_folder),exist_ok=True)    

    rectangle_folder='rectangle_folder'
    if not os.path.isdir(os.path.join(output_dir,rectangle_folder)):
        os.makedirs(os.path.join(output_dir,rectangle_folder),exist_ok=True)    

    max_move=[0,0]
    LOOP_LIMIT=1
    crop_width=500//2
    # crop_width=150

    # rotations=[-10,-5,0,5,10]
    # rotations=[0]
    # rotations=np.arange(-45,45+5,5)
    rotations=np.arange(-15,15+3,3)


    im=cv2.imread(os.path.join(base_folder_path,first_file_name))
    im=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    # queen=im[618:1038 , 55:500]
    # queen=im[278:885 , 212:802]
    # queen_pos=np.array([ [1094,888+queen_window_width] , [954,1000+queen_window_width] ])
    # queen_pos=np.array([ [1094,1243] , [954,1061] ])
    # queen_pos=np.array([ [954,1061] , [1094,1243]])
    # queen_pos=np.array([ [954,954+100] , [1094,1094+100]])

    # queen_pos=np.array([ [954+40,1061-30] , [1094,1243-50]])
    # queen_pos=np.array([ [816,908] , [2051,2193]])
    queen_pos=np.array([ [832,1014] , [2065,2161]])


    queen=im[queen_pos[0,0]:queen_pos[0,1] , queen_pos[1,0]:queen_pos[1,1]]
    fixed_queen_dim=queen.shape
    big_dim=[0,0]
    big_dim[0]=int(np.sqrt(queen.shape[0]**2+queen.shape[1]**2))+1
    big_dim[1]=int(np.sqrt(queen.shape[0]**2+queen.shape[1]**2))+1
 
    # big_dim[0]=queen.shape[0]
    # big_dim[1]=queen.shape[1]
    white=np.ones(queen.shape)
    queen=put_in_canvas(queen,big_dim)
    queen_filt=put_in_canvas(white,big_dim)
    queen_pos[0,0]=queen_pos[0,0]-(big_dim[0]-fixed_queen_dim[0])//2
    queen_pos[0,1]=queen_pos[0,1]+(big_dim[0]-fixed_queen_dim[0])//2

    queen_pos[1,0]=queen_pos[1,0]-(big_dim[1]-fixed_queen_dim[1])//2
    queen_pos[1,1]=queen_pos[1,1]+(big_dim[1]-fixed_queen_dim[1])//2 
    # queen=cv2.equalizeHist(queen)
    cv2.imwrite(os.path.join(output_dir,"raw_queen.png"),queen)
    im=im.astype(np.float32)
    queen=queen.astype(np.float32)

    image_names=sorted(os.listdir(base_folder_path))
    for c,file_name in enumerate(image_names):
        if c==8:
            print("trP")
        im=cv2.imread(os.path.join(base_folder_path,file_name))
        im=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        # matched=convolve2D(im,queen)
        im=im.astype(np.float32)

        # stabilizing 
        crop_points=np.zeros((2,2))
        crop_points[0,0]=max( (queen_pos[0,0]+queen_pos[0,1])//2 - crop_width//2,0)
        crop_points[0,1]=min( crop_points[0,0]+crop_width,im.shape[0])
        crop_points[1,0]=max( (queen_pos[1,0]+queen_pos[1,1])//2 - crop_width//2,0)
        crop_points[1,1]=min( crop_points[1,0]+crop_width,im.shape[1])
        crop_points=crop_points.astype(np.uint32)
        im_cropped=im[crop_points[0,0]:crop_points[0,1],crop_points[1,0]:crop_points[1,1]]
        cv2.imwrite(os.path.join(output_dir,crop_folder,file_name),im_cropped)

        rectangled=cv2.cvtColor(im,cv2.COLOR_GRAY2RGB)
        # first index in np is row which is y in opencv. so place of indexes should be swapped
        p1=(crop_points[1,0],crop_points[0,0])
        p2=(crop_points[1,1],crop_points[0,1])
        rectangled=cv2.rectangle(rectangled,p1,p2,(0,0,255),2)
        

        # matched=cv2.matchTemplate(im_cropped,queen-np.mean(queen[:]),cv2.TM_CCOEFF)
        # matched=cv2.matchTemplate(im_cropped,queen-np.mean(queen[:]),cv2.TM_SQDIFF_NORMED)
        # matched=cv2.matchTemplate(im_cropped,queen-np.mean(queen[:]),cv2.TM_CCOEFF_NORMED) #! 2 best
        # matched=cv2.matchTemplate(im_cropped,queen-np.mean(queen[:]),cv2.TM_CCORR)
        # matched=cv2.matchTemplate(im_cropped,queen-np.mean(queen[:]),cv2.TM_CCORR_NORMED) #! 1 best
        # matched=cv2.matchTemplate(im_cropped,queen-np.mean(queen[:]),cv2.TM_SQDIFF)
        # matched=cv2.matchTemplate(im_cropped,queen-np.mean(queen[:]),cv2.TM_SQDIFF_NORMED)

        
        queen_stack , masks=generate_rotations(queen,rotations,big_dim,fixed_queen_dim,queen_filt)
        match_stack=[]
        maxes=[]
        for i in range(queen_stack.shape[0]):
            filt=np.round(masks[i])
            kernel=queen_stack[i]
            kernel[filt==1]=kernel[filt==1]-np.mean(kernel[filt==1])

            kernel=kernel.astype(np.float32)
            HM = cv2.matchTemplate(im_cropped,kernel,cv2.TM_CCORR_NORMED) #! 1 best
            # HM = manual_conv2d(im_cropped,kernel)
            match_stack.append(HM)
            maxes.append(match_stack[i].max())
        maxes=np.array(maxes)
        chosen_rot=maxes.argmax()
        matched = match_stack[ chosen_rot ]
        queen_filt=np.round(masks[chosen_rot]).astype(np.uint8)

        
        
        matched=normalize(matched)
        cv2.imwrite(os.path.join(output_dir,heatmaps,file_name),matched)

        indx=np.unravel_index(matched.argmax(),matched.shape)
        
        queen_pos[0,0]= min( crop_points[0,0] + indx[0] , im.shape[0])
        queen_pos[0,1]= min( queen_pos[0,0] + queen_stack.shape[1] , im.shape[0])
        queen_pos[1,0]= min(crop_points[1,0] + indx[1] , im.shape[1])
        queen_pos[1,1]= min(queen_pos[1,0] + queen_stack.shape[2] , im.shape[1])

        # queen=im[queen_pos[0,0]:queen_pos[0,1] , queen_pos[1,0]:queen_pos[1,1]] #!
        queen=im_cropped[indx[0]:indx[0]+queen_stack.shape[1] , indx[1]:indx[1]+queen_stack.shape[2]]
        queen[queen_filt==0]=0
        queen=queen.astype(np.uint8)
        # queen=cv2.equalizeHist(queen)
        cv2.imwrite(os.path.join(output_dir,queen_folder,file_name),queen)
        queen=queen.astype(np.float32)
        

        p1=(queen_pos[1,0],queen_pos[0,0])
        p2=(queen_pos[1,1],queen_pos[0,1])
        rectangled=cv2.rectangle(rectangled,p1,p2,(0,255,0),2)
        rectangled=cv2.putText(rectangled,"angle {}".format(rotations[chosen_rot]) , (100,100) , cv2.FONT_HERSHEY_SIMPLEX , 1 , (255 , 0 , 255) ,2)

        cv2.imwrite(os.path.join(output_dir,rectangle_folder,file_name),rectangled)

        # print("[+] process {:.2f} ".format(c/len(os.listdir(base_folder_path))*100),end='\r')
        # print(queen_pos)

    print('[+] bye !')