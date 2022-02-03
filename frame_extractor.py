# command to execute this code in Arash thinkpad: /usr/bin/env /bin/python3 frame_extractor.py 100 annotated.avi
# opencv doesn't exist in original path
import sys, os
import cv2
from time import time,ctime
output_dir_name=ctime(time()).replace(':','_')
os.mkdir(output_dir_name)
number_of_frames=int(sys.argv[1])
video_path=sys.argv[2]
vidcap = cv2.VideoCapture(video_path)
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite(output_dir_name+"/%06d.png" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
#   print('Read a new frame: ', success)
  count += 1
  if count >=number_of_frames:
      print("[+] {} frames were extracted! \n goodbye".format(number_of_frames))
      exit(0)
    #   break

print("[-] couldn't read the video")