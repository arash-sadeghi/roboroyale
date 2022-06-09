from cgi import test
import os
import numpy as np
import sys
import cv2
import matplotlib.pyplot as plt
import random
# from torch.nn import functional as F
# import torch 
from scipy import signal
def convolve2D(image, kernel, padding=0, strides=1):
    # Cross Correlation
    kernel = np.flipud(np.fliplr(kernel))

    # Gather Shapes of Kernel + Image + Padding
    xKernShape = kernel.shape[0]
    yKernShape = kernel.shape[1]
    xImgShape = image.shape[0]
    yImgShape = image.shape[1]

    # Shape of Output Convolution
    xOutput = int(((xImgShape - xKernShape + 2 * padding) / strides) + 1)
    yOutput = int(((yImgShape - yKernShape + 2 * padding) / strides) + 1)
    output = np.zeros((xOutput, yOutput))

    # Apply Equal Padding to All Sides
    if padding != 0:
        imagePadded = np.zeros((image.shape[0] + padding*2, image.shape[1] + padding*2))
        imagePadded[int(padding):int(-1 * padding), int(padding):int(-1 * padding)] = image
        print(imagePadded)
    else:
        imagePadded = image

    # Iterate through image
    for y in range(image.shape[1]- yKernShape):
        print("[+] progress {:.2f}".format(y/image.shape[1]*100),end='\r')
        if y % strides == 0:
            for x in range(image.shape[0]- xKernShape):
                try:
                    if x % strides == 0:
                        output[x, y] = (kernel * imagePadded[x: x + xKernShape, y: y + yKernShape]).sum()/(xKernShape*yKernShape)
                except:
                    print("[+] broke because of try except")
                    break

    return output

if __name__=='__main__':
    base_folder_path='Aug05-07_side1_rpi1_full_cut'
    file_name='test.jpg'
    output_dir="outputs/"+sys.argv[0].split("/")[-1].split(".")[0]
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir,exist_ok=True)    
    lots_of_data="lots_of_data"
    if not os.path.isdir(os.path.join(output_dir,lots_of_data)):
        os.makedirs(os.path.join(output_dir,lots_of_data),exist_ok=True)    

    LOOP_LIMIT=1
    im=cv2.imread(os.path.join(base_folder_path,file_name))
    im=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    im_eq=cv2.equalizeHist(im)
    queen=im_eq[200:450 , 235:520]
    cv2.imwrite(os.path.join(output_dir,"raw_queen.png"),queen)
    matched=cv2.matchTemplate(im_eq,queen,cv2.TM_CCOEFF)
    matched=(matched-np.min(matched[:])) / (np.max(matched[:])-np.min(matched[:]))*255
    cv2.imwrite(os.path.join(output_dir,lots_of_data,file_name),matched)
    for c,file_name in enumerate(sorted(os.listdir(base_folder_path))):
        
        im=cv2.imread(os.path.join(base_folder_path,file_name))
        im=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        im_eq=cv2.equalizeHist(im)
        matched=cv2.matchTemplate(im_eq,queen,cv2.TM_CCOEFF)
        matched=(matched-np.min(matched[:])) / (np.max(matched[:])-np.min(matched[:]))*255
        cv2.imwrite(os.path.join(output_dir,lots_of_data,file_name),matched)

        print("[+] process {:.2f} ".format(c/len(os.listdir(base_folder_path))*100),end='\r')


    print('[+] bye !')