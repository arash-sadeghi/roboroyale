import os
import numpy as np
import sys
import cv2
import matplotlib.pyplot as plt
import random
def hist_dem(im,queen):
    plt.hist(im.flatten(),256,[0,256], color = 'r')
    plt.xlim([0,256])
    plt.legend(('cdf','histogram'), loc = 'upper left')
    plt.savefig(os.path.join(output_dir,'im_hist.png'))
    plt.clf()

    x_beg=random.randrange(0,im.shape[0]-queen.shape[0])
    y_beg=random.randrange(0,im.shape[1]-queen.shape[1])
    rand_select=im[ x_beg:x_beg+queen.shape[0] , y_beg:y_beg+queen.shape[1]]
    cv2.imwrite(os.path.join(output_dir,"random select.png"),rand_select)

    plt.hist(rand_select.flatten(),256,[0,256], color = 'r')
    plt.xlim([0,256])
    plt.legend(('cdf','histogram'), loc = 'upper left')
    plt.savefig(os.path.join(output_dir,'random_hist.png'))
    plt.clf()

    plt.hist(queen.flatten(),256,[0,256], color = 'r')
    plt.xlim([0,256])
    plt.legend(('cdf','histogram'), loc = 'upper left')
    plt.savefig(os.path.join(output_dir,'queen_hist.png'))
    plt.clf()


def equlizer(im):

    equ = cv2.equalizeHist(im)
    res = np.hstack((im,equ)) #stacking images side-by-side
    cv2.imwrite(os.path.join(output_dir,'whole_image_equlized.png'),res)
    res = np.hstack((im[200:450 , 235:520],equ[200:450 , 235:520])) #stacking images side-by-side
    cv2.imwrite(os.path.join(output_dir,'queen_equlized.png'),res)

    # plt.plot(cdf_normalized, color = 'b')
    # plt.hist(im.flatten(),256,[0,256], color = 'r')
    # plt.xlim([0,256])
    # plt.legend(('cdf','histogram'), loc = 'upper left')
    # plt.show()
    return equ

if __name__=='__main__':
    base_folder_path='Aug05-07_side1_rpi1_full_cut'
    file_name='raw_hive1_rpi1_190805-121858-utc.jpg'
    
    output_dir="outputs/"+sys.argv[0].split("/")[-1].split(".")[0]
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir,exist_ok=True)    
    
    images=os.listdir(base_folder_path)
    LOOP_LIMIT=1
    im=cv2.imread(os.path.join(base_folder_path,file_name))
    im=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    queen=im[200:450 , 235:520]
    cv2.imwrite(os.path.join(output_dir,"raw_queen.png"),queen)
    im_eq=equlizer(im)
    queen_eq=im_eq[200:450 , 235:520]
    hist_dem(im_eq,queen_eq)

    



    # plt.imshow()
    plt.show()
    print('[+] bye !')