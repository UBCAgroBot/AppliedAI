import time
import os
import cv2
import psutil
import GPUtil
import supervision as sv
from ultralytics import YOLO
# from numba import jit

import rclpy
from rclpy.time import Time
from rclpy.node import Node
from std_msgs.msg import Header, String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class JetsonNode(Node):
    def __init__(self):
        super().__init__('jetson_node') #type:ignore
        self.bridge = CvBridge()
        self.model_publisher = self.create_publisher(String, 'bounding_boxes', 10)
        self.camera_subscriber = self.create_subscription(Image, 'image_data', self.callback, 10)
        self.off_subscriber = self.create_subscription(String, 'off', self.display_metrics, 10)
        self.frames, self.cpu, self.mem, self.time, self.latency, self.pid = 0, 0, 0, 0, 0, 0
        self.model = YOLO('yolov8s.pt')
        self.tensorrt_init()
    
    def tensorrt_init(self):
        pass
    
    def callback(self, msg):
        self.get_logger().info(f"Latency of {msg.header.frame_id} is {(self.get_clock().now().nanoseconds() - msg.header.stamp.nanoseconds()) / 1e6} milliseconds")
        # self.get_logger().info(f"Received: {msg.header.frame_id}")
        # now = self.get_clock().now()
        # latency = now - Time.from_msg(msg.header.stamp)
        # print(f"Message transmisison latency: {latency.nanoseconds / 1e6} milliseconds")
        # self.latency, self.frame_id, self.frames = latency.nanoseconds / 1e6, msg.header.frame_id, self.frames + 1
        # try:
        #     cv_image  = self.bridge.imgmsg_to_cv2(msg)
        #     self.detection(cv_image)
        # except CvBridgeError as e:
        #     self.get_logger().info(e)
        #     print(e)

    def high_precision_sleep(self, duration):
        start_time = time.perf_counter()
        while True:
            elapsed_time = time.perf_counter() - start_time
            remaining_time = duration - elapsed_time
            if remaining_time <= 0:
                break
            if remaining_time > 0.02:  # Sleep for 5ms if remaining time is greater
                time.sleep(max(remaining_time/2, 0.0001))  # Sleep for the remaining time or minimum sleep interval
            else:
                pass
    
    def preprocessing(self, data):
        pass

    def detection(self, data):
        pid = os.getpid()

        tic = time.perf_counter_ns()
        # pre_mem = psutil.Process(pid).memory_percent()
        # pre_cpu = psutil.Process(pid).cpu_percent(interval=None)
        # result = self.model(data)[0]
        self.high_precision_sleep(0.001)
        # post_cpu = psutil.Process(pid).cpu_percent(interval=None)
        # post_mem = psutil.Process(self.pid).memory_percent()
        toc = time.perf_counter_ns()
        
        # self.cpu = ((self.post_cpu-self.pre_cpu)/self.time) * 100
        # self.mem = post_mem - pre_mem
        self.time = (toc-tic)/1e6
        self.gpu = 0 # gpu.load*100
        self.gpu_mem = 0 # (gpu.memoryUsed / gpu.memoryTotal) * 100
        
        # self.get_logger().info(f"CPU usage: {self.cpu}%")
        # self.get_logger().info(f"GPU usage: {self.gpu}%")
        # self.get_logger().info(f"GPU VRAM usage: {self.gpu_mem}%")
        # self.get_logger().info(f"Memory usage: {self.mem}%")
        # self.get_logger().info(f"Execution time: {self.time} milliseconds")
        
        # detections = sv.Detections.from_ultralytics(result)
        # self.publish_result(detections)
    
    def publish_result(self, bounding_boxes):
        header = Header()
        header.metrics = f"{self.frame_id} {self.cpu} {self.mem} {self.time} {self.latency} {self.gpu} {self.gpu_mem} {self.frames} {self.fps} {self.id}"
        msg = String()
        msg.data = bounding_boxes
        self.model_publisher.publish(msg)
        self.get_logger().info(msg.data)
    
    def display_metrics(self):
        self.get_logger().info(f'Frame loss: {((self.frames/self.last_frame_id)*100):0.1f}')
        raise SystemExit

def main(args=None):
    rclpy.init(args=args)
    jetson_node = JetsonNode()
    try:
        rclpy.spin(jetson_node)
    except KeyboardInterrupt:
        print("josy...")
        jetson_node.display_metrics()
        rclpy.logging.get_logger("Quitting").info('Done')
    except SystemExit:   
        print("josy...")
        jetson_node.display_metrics()
        rclpy.logging.get_logger("Quitting").info('Done')

    rclpy.spin(jetson_node)
    jetson_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()