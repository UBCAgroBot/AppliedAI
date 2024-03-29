import cv2
import matplotlib.pyplot as plt
import numpy as np
from decord import VideoReader, cpu
import os
import time

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

TYPE1 = "Webcam"
TYPE2 = "Video"
TYPE3 = "Image"
TYPE4 = "ZED Camera"
DELAY = 0.1

os.chdir("23-I-12_SysArch/Experiments/extermination_workspace") # change to be dynamic

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node')
        self.initialize()
        self.image = None
        self.bridge = CvBridge()
        self.type = TYPE1
        self.on = True
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.frame_publisher = self.create_publisher(Image, 'source', 10)

    def initialize(self):
        if self.type == TYPE1:
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                else:
                    self.image = frame
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.on = not self.on
                    
        elif self.type == TYPE2:
            is_working = True
            vr = VideoReader('examples/flipping_a_pancake.mkv', ctx=cpu(0))
            if is_working:
                for i in range(len(vr)):
                    self.image = vr[i]
                    time.sleep(DELAY)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        self.on = not self.on
        elif self.type == TYPE3:
            is_working = True
            self.image = cv2.imread("test.jpg")
            time.sleep(DELAY)
        else:
            import pyzed.sl as sl
            init = sl.InitParameters()
            cam = sl.Camera()
            init.camera_resolution = sl.RESOLUTION.HD1080
            init.camera_fps = 30
            
            if not cam.is_opened():
                print("Opening ZED Camera ")
            status = cam.open(init)
            if status != sl.ERROR_CODE.SUCCESS:
                print(repr(status))
                exit()
            
            runtime = sl.RuntimeParameters()
            mat = sl.Mat()
            
            key = ''
            while key != 113:  # for 'q' key
                err = cam.grab(runtime)
                if err == sl.ERROR_CODE.SUCCESS:
                    cam.retrieve_image(mat, sl.VIEW.LEFT_UNRECTIFIED)
                    image = mat.get_data()
                    image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
                    key = cv2.waitKey(5)
                else:
                    key = cv2.waitKey(5)
            cam.close()
            print("ZED Camera closed")

    def timer_callback(self):
        try:
            cv2.imshow(str(self.type), self.image)
            msg = self.bridge.cv2_to_imgmsg(self.image, "bgr8")
            self.frame_publisher.publish(msg)
        except CvBridgeError as e:
            print(e)