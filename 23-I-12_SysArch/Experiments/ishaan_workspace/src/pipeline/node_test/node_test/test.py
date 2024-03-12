import time

tic = time.perf_counter_ns()
time.sleep(2)
toc = time.perf_counter_ns()

import psutil
def get_threads_cpu_percent(p, interval=0.1):
    total_percent = p.cpu_percent(interval)
    total_time = sum(p.cpu_times())
    return [('%s %s %s' % (total_percent * ((t.system_time + t.user_time)/total_time), t.id, psutil.Process(t.id).name())) for t in p.threads()]

# Get 1 available GPU, ordered by GPU load ascending
# print('First available weighted by GPU load ascending: '),
# print(GPU.getAvailable(order='load', limit=1))

gpu = GPUtil.getGPUs()[0] # firstGPU = GPU.getFirstAvailable()

# Get 1 available GPU, ordered by ID in descending order
# print('Last available: '),
# print(GPU.getAvailable(order='last', limit=1))  

# better put in separate process
# from tqdm import tqdm
# from time import sleep
# import psutil

# with tqdm(total=100, desc='cpu%', position=1) as cpubar, tqdm(total=100, desc='ram%', position=0) as rambar:
#     while True:
#         rambar.n=psutil.virtual_memory().percent
#         cpubar.n=psutil.cpu_percent()
#         rambar.refresh()
#         cpubar.refresh()
#         sleep(0.5)

# # if fancy CPU measure no work: 

# function here

# latency might require adding milliseconds + nanoseconds together?

# # grab the new total amount of time the process has used the cpu
# final_total_time = sum(proc.cpu_times())

# # grab the new system and user times for each thread
# final_thread_times = {'a': {'system': None, 'user': None}}
# for thread in proc.threads():
#     final_thread_times[psutil.Process(thread.id).name()]['system'] = thread.system_time
#     final_thread_times[psutil.Process(thread.id).name()]['user'] = thread.user_time

# # calculate how much cpu each thread used by...
# total_time_thread_a_used_cpu_over_time_interval = ((final_thread_times['a']['system']-initial_thread_times['a']['system']) + (final_thread_times['a']['user']-initial_thread_times['a']['user']))
# total_time_process_used_cpu_over_interval = final_total_time - initial_total_time

# percent_of_cpu_usage_utilized_by_thread_a = total_cpu_percent*(total_time_thread_a_used_cpu_over_time_interval/total_time_process_used_cpu_over_interval)

# yolobot inference result .msg:
string class_name
int64 top
int64 left
int64 bottom
int64 right

# yolobot yolov8 inference .msg:
std_msgs/Header header
InferenceResult[] yolov8_inference

# for subscriber: from yolov8_msgs.msg import Yolov8Inference

#!/usr/bin/env python3

import cv2
import threading
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from yolov8_msgs.msg import Yolov8Inference

bridge = CvBridge()

class Camera_subscriber(Node):

    def __init__(self):
        super().__init__('camera_subscriber')

        self.subscription = self.create_subscription(
            Image,
            'rgb_cam/image_raw',
            self.camera_callback,
            10)
        self.subscription 

    def camera_callback(self, data):
        global img
        img = bridge.imgmsg_to_cv2(data, "bgr8")

class Yolo_subscriber(Node):

    def __init__(self):
        super().__init__('yolo_subscriber')

        self.subscription = self.create_subscription(
            Yolov8Inference,
            '/Yolov8_Inference',
            self.yolo_callback,
            10)
        self.subscription 

        self.cnt = 0

        self.img_pub = self.create_publisher(Image, "/inference_result_cv2", 1)

    def yolo_callback(self, data):
        global img
        for r in data.yolov8_inference:
        
            class_name = r.class_name
            top = r.top
            left = r.left
            bottom = r.bottom
            right = r.right
            yolo_subscriber.get_logger().info(f"{self.cnt} {class_name} : {top}, {left}, {bottom}, {right}")
            cv2.rectangle(img, (top, left), (bottom, right), (255, 255, 0))
            self.cnt += 1

        self.cnt = 0
        img_msg = bridge.cv2_to_imgmsg(img)  
        self.img_pub.publish(img_msg)

if __name__ == '__main__':
    rclpy.init(args=None)
    yolo_subscriber = Yolo_subscriber()
    camera_subscriber = Camera_subscriber()

    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(yolo_subscriber)
    executor.add_node(camera_subscriber)

    executor_thread = threading.Thread(target=executor.spin, daemon=True)
    executor_thread.start()
    
    rate = yolo_subscriber.create_rate(2)
    try:
        while rclpy.ok():
            rate.sleep()
    except KeyboardInterrupt:
        pass

    rclpy.shutdown()
    executor_thread.join()

# !!! wtf is a mutltithreaded executor?
# changes rate?

#!/usr/bin/env python3

from ultralytics import YOLO
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from yolov8_msgs.msg import InferenceResult
from yolov8_msgs.msg import Yolov8Inference

bridge = CvBridge()

class Camera_subscriber(Node):

    def __init__(self):
        super().__init__('camera_subscriber')

        self.model = YOLO('~/yolobot/src/yolobot_recognition/scripts/yolov8n.pt')

        self.yolov8_inference = Yolov8Inference()

        self.subscription = self.create_subscription(
            Image,
            'rgb_cam/image_raw',
            self.camera_callback,
            10)
        self.subscription 

        self.yolov8_pub = self.create_publisher(Yolov8Inference, "/Yolov8_Inference", 1)
        self.img_pub = self.create_publisher(Image, "/inference_result", 1)

    def camera_callback(self, data):

        img = bridge.imgmsg_to_cv2(data, "bgr8")
        results = self.model(img)

        self.yolov8_inference.header.frame_id = "inference"
        self.yolov8_inference.header.stamp = camera_subscriber.get_clock().now().to_msg()

        for r in results:
            boxes = r.boxes
            for box in boxes:
                self.inference_result = InferenceResult()
                b = box.xyxy[0].to('cpu').detach().numpy().copy()  # get box coordinates in (top, left, bottom, right) format
                c = box.cls
                self.inference_result.class_name = self.model.names[int(c)]
                self.inference_result.top = int(b[0])
                self.inference_result.left = int(b[1])
                self.inference_result.bottom = int(b[2])
                self.inference_result.right = int(b[3])
                self.yolov8_inference.yolov8_inference.append(self.inference_result)

            #camera_subscriber.get_logger().info(f"{self.yolov8_inference}")

        annotated_frame = results[0].plot()
        img_msg = bridge.cv2_to_imgmsg(annotated_frame)  

        self.img_pub.publish(img_msg)
        self.yolov8_pub.publish(self.yolov8_inference)
        self.yolov8_inference.yolov8_inference.clear()

if __name__ == '__main__':
    rclpy.init(args=None)
    camera_subscriber = Camera_subscriber()
    rclpy.spin(camera_subscriber)
    rclpy.shutdown()
