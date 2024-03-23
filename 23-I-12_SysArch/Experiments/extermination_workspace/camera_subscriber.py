import cv2
import numpy as np
from matplotlib.colors import hsv_to_rgb
import matplotlib.pyplot as plt
from tracker import *

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Header, String, Integer
from cv_bridge import CvBridge, CvBridgeError

PUBLISH_RATE = 10
LIGHT_GREEN = (78, 158, 124)
DARK_GREEN = (60, 255, 255)
ROI_X = 0
ROI_Y = 0
ROI_W = 100
ROI_H = 100
UPDATE_RATE = 1

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node') #type: ignore
        self.bridge = CvBridge()
        self.tracker = EuclideanDistTracker()
        self.queue = []
        self.image = None
        
        self.left.on, self.right.on = 0, 0
        self.left_camera_subscriber = self.create_subscription(Image, 'image_data', self.callback, 10)
        self.left_camera_subscriber # necessary?
        self.right_camera_subscriber = self.create_subscription(Image, 'image_data', self.callback, 10)
        self.right_camera_subscriber
        self.left_array_publisher = self.create_publisher(Integer, 'left_array_data', 10) # rate is 10 Hz?
        self.right_array_publisher = self.create_publisher(Integer, 'right_array_data', 10)

    def callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "rgb8")
            self.queue.append(cv_image)
            self.preprocess_image()
        except CvBridgeError as e:
            print(e)
    
    def preprocess_image(self):
        if len(self.queue) == 2:
            left_image = self.queue.pop(0)
            right_image = self.queue.pop(0)
            stacked_image = cv2.hconcat([left_image, right_image])
            print(stacked_image.shape)
            padded_image = cv2.copyMakeBorder(stacked_image, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0]) # add padding to make it square
            print(padded_image.shape)
            resized_image = cv2.resize(padded_image, (255, 255))
            plt.imshow(resized_image)
            plt.show()
            self.image = resized_image
            self.model_inference()
    
    def model_inference(self):
        # model inference here...
        self.postprocess_image()
    
    def postprocess_image(self):
        # Read the image
        img = cv2.imread('your file name')
        print(img.shape)
        height = img.shape[0]
        width = img.shape[1]

        # Cut the image in half
        width_cutoff = width // 2
        s1 = img[:, :width_cutoff]
        s2 = img[:, width_cutoff:]
        height,width,depth = x.shape
        return [x[height , :width//2] , x[height, width//2:]]
        plt.imshow(imCrop(yourimage)[1])
    
    def object_filter(self, side):
        within = False
        height, width, _ = self.image.shape
        # Extract Region of interest
        roi = frame[340: 720,500: 800]

        # 1. Object Detection
        mask = object_detector.apply(roi)
        _, mask = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        detections = []
        for cnt in contours:
            # Calculate area and remove small elements
            area = cv2.contourArea(cnt)
            if area > 100:
                #cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                x, y, w, h = cv2.boundingRect(cnt)
                # this function will take cropped image w/ bounding box to clean it up
    # def color_segmentation_mask(self):
    #     lower_green = np.array([78,158,124])
    #     upper_green = np.array([60, 255, 255])
    #     hsv = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV) # image should be cropped w/ bounding box dimensions (cleaning each object box)
    #     mask = cv2.inRange(hsv,lower_green,upper_green)
    #     result = cv2.bitwise_and(self.image,self.image, mask=mask) 
    #     plt.subplot(1, 2, 1)
    #     plt.imshow(mask, cmap="gray")
    #     plt.subplot(1, 2, 2)
    #     plt.imshow(result)
    #     plt.show()
    #     bbox = cv2.boundingRect(mask)
    #     if bbox is not None:
    #         x, y, w, h = bbox
    #         cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)


                detections.append([x, y, w, h])

        # 2. Object Tracking
        boxes_ids = tracker.update(detections)
        for box_id in boxes_ids:
            x, y, w, h, id = box_id
            cv2.putText(roi, str(id), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 3)

        cv2.imshow("roi", roi)
        cv2.imshow("Frame", frame)
        cv2.imshow("Mask", mask)

        key = cv2.waitKey(30)
        if key == 27:
            break
        
        # check if any of the four corners of the bounding box are within the ROI
        if within and side == "left":
            self.publish_
        else:
            self.publish_array(0)
    
    def publish_array(self, status):
        msg = Integer()
        msg.data = 1
        self.array_publisher.publish(msg)
    
    # Shift ROI to the left for more delay
    # Not sure how to implement gaussian smoothing -> copilot

# check if any of the four corners of the bounding box are within the ROI

# if any bounding boxes found: increment count, if bounding box is found per frame, make publisher send 1, otherwise publisher sends 0
# only need to add assigning IDs to each bounding box so each unique ID that enters ROI is counted once

# filtering detections that are given from bounding box model
# slider for delay (sleep timer between detection and publishing if bounding box found in area)
# either way we are making only taking in bounding box coords, no need for tags there
# one publisher for each camera, one subscriber for each camera

# image thresholding
# question for applying bounding box to cropped image for different bounding boxes found from primary detection? -> need to transform coordinates relative to the cropped image
# try padding/running both images in model, but will likely be beter to turn two engine processes