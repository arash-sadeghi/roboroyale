import os
import argparse

import cv2

import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from time import ctime, time

import csv,datetime

def format_number(n):
    if n<10:
        return '0'+str(n)
    else:
        return str(n)
def get_temp(csv_content,second):
    date=datetime.datetime.strptime(ctime(second),"%a %b %d %H:%M:%S %Y")
    date_format=format_number(date.year)+'-'+format_number(date.month)+'-'+format_number(date.day)
    for row in csv_content:
        if row[0]==date_format:
            return "tmin: "+row[2]+" tavg: "+row[1]+" tmax: "+row[3]
    return "temp_not_found"
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
    TIME_INTERVAL=30
    bag_list=os.listdir(args.input_dir)
    bag_list.sort()    
    tmp=bag_list.copy()

    for i in tmp:
        if not ('.bag' in i):
            bag_list.remove(i)
    written_bags=[]
    video_file_name=args.input_dir+ctime(time()).replace(":","_").replace(" ","_")+".avi"
    bag_log=open(video_file_name[0:-4]+'.txt','w') 
    size = (1280,720)
    FPS=48
    video=cv2.VideoWriter(video_file_name,cv2.VideoWriter_fourcc(*'XVID'), FPS, size)
    weather_file_name="graz_weather_dec.csv"
    csv_file=open(weather_file_name)
    csv_reader = csv.reader(csv_file, delimiter=',')
    csv_content=[]
    for i in csv_reader:
        csv_content.append(i)
    csv_file.close()
    #try:
    if True:
        for file in bag_list:
            print("[+] Extract images from {} on topic {} into {}".format(file,args.image_topic, video_file_name))
            bag_log.write(args.input_dir+file+'\n')
            bag = rosbag.Bag(args.input_dir+file, "r")
            print("[+] bag successfully read")
            time_tmp=next(bag.read_messages(args.image_topic))[2].to_sec()
            count = 0
            
            for topic, msg, t in bag.read_messages(args.image_topic):
                if int(t.to_sec()-time_tmp)==TIME_INTERVAL:
                    time_tmp=t.to_sec()
                    cv_img = bridge.compressed_imgmsg_to_cv2(msg)
                    cv_img=cv2.cvtColor(cv_img, cv2.COLOR_GRAY2BGR)
                    cv2.putText(cv_img,ctime(t.to_sec()) , (0,size[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    temp_str=get_temp(csv_content,t.to_sec())
                    cv2.putText(cv_img,temp_str , (size[0]//2,size[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0, 0), 2, cv2.LINE_AA)
                    # cv2.imwrite("im.png",cv_img)
                    video.write(cv_img)
                    count += 1
                    percentage=count/(24*3600/30)*100
                    print("[+] progress {:.2f}".format(percentage),end='\r')

            print("\n[+] bag {} added".format(file))
            bag.close()
        bag_log.close()
        video.release()
        print("\n[+] DONE!")
    
   #  except Exception as E:
   #     print('[-] Error occured: ',E)
   #     bag_log.close()
   #     video.release()
   #     csv_file.close()
''' ctime(t.to_sec()) '''
'''
30 mins one day
3600*24=86400 in total
30 mins= 1800 sec
each sec FPS pictures
1800*FPS=86400-->FPS=48
'''

    
 

