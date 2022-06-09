#! usr/bin/python 
import os,sys

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



if __name__ == '__main__':
    bridge = CvBridge()
    TIME_INTERVAL=30
    # ros_bag_file_name="2022-03-14-18-24-54_graz_bag.bag"
    ros_bag_file_name="/home/arash/Desktop/workdir/RoboRoyal/codes_for_roboroyale_gitlab/bee_tracking/2022-03-15-14-05-31.bag"
    
    topic="/cam1/main_camera/image_raw"
    output_dir="outputs/"+sys.argv[0].split("/")[-1].split(".")[0]
    output_dir=os.path.join(output_dir,topic.replace("/","_"))+"whycon"
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir,exist_ok=True)    

    print("[+] Extract images from {} on topic {} into {}".format(ros_bag_file_name,topic, output_dir))
    bag = rosbag.Bag(ros_bag_file_name, "r")
    print("[+] bag successfully read")
    time_tmp=next(bag.read_messages(topic))[2].to_sec()
    count = 0
    
    for topic, msg, t in bag.read_messages(topic):
        time_tmp=t.to_sec()
        cv_img = bridge.imgmsg_to_cv2(msg)
        cv_img=cv2.cvtColor(cv_img, cv2.COLOR_GRAY2BGR)
        tmp='{:05d}'.format(count)+topic.replace("/","_")+'.png'
        cv2.imwrite(os.path.join(output_dir,tmp),cv_img)
        count += 1
        percentage=count/(24*3600/30)*100
        print("[+] progress {:.2f}".format(percentage),end='\r')

    bag.close()
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

    
 

