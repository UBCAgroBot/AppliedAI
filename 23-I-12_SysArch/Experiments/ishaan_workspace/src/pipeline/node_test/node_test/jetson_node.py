import time
import os
import cv2
import psutil

import rclpy
from rclpy.time import Time
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from ultralytics import YOLO

import tensorflow as tf #!!! this and numpy compatibilty issue > numpy needs to be higher version for zed camera, but requires lower version for tensorflow -> build from source?
import numpy as np # onnx to load model and optimize?

class CNNNode(Node):
    def __init__(self):
        super().__init__('cnn_node') #type:ignore
        self.bridge = CvBridge()
        self.model_publisher = self.create_publisher(String, 'bounding_box_coords', 10)
        self.camera_subscriber = self.create_subscription(Image, 'image_data', self.callback, 10)
        #self.model = YOLO(weights)
    
    def callback(self, msg):
        self.get_logger().info(f"Received: {msg.header}")
        now = self.get_clock().now()
        latency = now - Time.from_msg(msg.header.stamp)
        print(f"Message transmisison latency: {latency.nanoseconds / 1e6} milliseconds")
        self.preprocess_data(msg.data)
    
    def measure_system_performance(self, func):
        def wrapper(*args, **kwargs):
            pid = os.getpid()
            pre_cpu = psutil.Process(pid).cpu_percent(interval=None)
            pre_mem = psutil.Process(pid).memory_percent()
            tic = time.perf_counter_ns()
            result = func(*args, **kwargs)
            toc = time.perf_counter_ns()
            post_cpu = psutil.Process(pid).cpu_percent(interval=None)
            post_mem = psutil.Process(pid).memory_percent()
            self.get_logger.info(f"Function {func.__name__} execution time: {(toc-tic)/1e6} milliseconds")
            self.get_logger.info(f"Function {func.__name__} CPU usage: {post_cpu - pre_cpu}%")
            self.get_logger.info(f"Function {func.__name__} Memory usage: {post_mem - pre_mem}%")
            return result
        return wrapper
            
    def preprocess_data(self, data):
        # here...
        self.detection(data)

    @measure_system_performance() #functools?
    def detection(self, data):
        bounding_boxes = self.model.predict(data)
        self.publish_result(bounding_boxes)
    
    def publish_result(self, bounding_boxes):
        msg = String()
        msg.data = bounding_boxes
        self.model_publisher.publish(msg)
        self.get_logger().info(msg.data)

def main(args=None):
    rclpy.init(args=args)
    cnn_node = CNNNode()
    rclpy.spin(cnn_node)
    cnn_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
