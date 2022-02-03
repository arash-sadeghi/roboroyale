# first argument is the path to image folder
# second argument is the format of the images that should ne renamed
# for converting import PIL (code is not compelete for this)
import os
import sys
def rename_images(im_frames_path,formats='.jpg'):
    print("[+] rename images in path {}".format(im_frames_path))
    imgs=sorted(os.listdir(im_frames_path))
    for c,img in enumerate(imgs):
        if formats in img:
            old=im_frames_path+"/"+img
            new=im_frames_path+r'/%06d'% c+formats
            os.rename(old,new)

if len(sys.argv)>2:
    rename_images(sys.argv[1],sys.argv[2])
else:
    rename_images(sys.argv[1])
