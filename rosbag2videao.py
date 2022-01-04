import os
import argparse

import cv2

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from time import ctime, time

class Args:
    def __init__(self):
        self.bag_file=""
        #self.image_topic="/d435/1/infra1/image_rect_raw/compressed"
        self.image_topic="/cam/infra1/image_rect_raw/compressed_slowed"
        self.input_dir="/home/users/aamjadi/hdd/rosbags/"
        self.output_dir="/home/users/aamjadi/hdd/rosbags/"



if __name__ == '__main__':
    """Extract a folder of images from a rosbag."""
    # parser = argparse.ArgumentParser(description="Extract images from a ROS bag.")
    # parser.add_argument("bag_file", help="Input ROS bag.")
    # parser.add_argument("output_dir", help="Output directory.")
    # parser.add_argument("image_topic", help="Image topic.")
    # args = parser.parse_args()

    args=Args()
    bridge = CvBridge()
    video_file_name=args.input_dir+ctime(time()).replace(":","_")+".avi"
    FPS=48
    TIME_INTERVAL=30
    size = (1280,720)
    video = cv2.VideoWriter(video_file_name,cv2.VideoWriter_fourcc(*'XVID'), FPS, size)
    bag_list=os.listdir(args.input_dir)
    bag_list.sort()    
    for file in bag_list:
        print("[+] Extract images from {} on topic {} into {}".format(file,args.image_topic, video_file_name))
        bag = rosbag.Bag(args.input_dir+file, "r")
        print("[+] bag successfully read")
        time_tmp=next(bag.read_messages(args.image_topic))[2].to_sec()
        count = 0
        
        for topic, msg, t in bag.read_messages(args.image_topic):
            if int(t.to_sec()-time_tmp)==TIME_INTERVAL:
                time_tmp=t.to_sec()
                cv_img = bridge.compressed_imgmsg_to_cv2(msg)
                video.write(cv2.cvtColor(cv_img, cv2.COLOR_GRAY2BGR))
                count += 1
                percentage=count/(24*3600/30)*100
                print("[+] progress {:.2f}".format(percentage),end='\r')

        print("\n[+] bag {} added".format(file))
        bag.close()
    video.release()
    print("\n[+] DONE!")
''' ctime(t.to_sec()) '''
'''
30 mins one day
3600*24=86400 in total
30 mins= 1800 sec
each sec FPS pictures
1800*FPS=86400-->FPS=48
'''

    
 

