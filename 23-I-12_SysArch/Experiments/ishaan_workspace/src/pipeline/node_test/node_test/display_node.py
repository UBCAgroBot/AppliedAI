import os
import cv2
import supervision as sv
from tabulate import tabulate
from timeloop import Timeloop
from datetime import timedelta

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from example_interfaces.srv import Trigger

# tqdm threading later or moving average in display node
# run display node on my computer -> display metric node

COLORS = sv.ColorPallete().default()

class DisplayNode(Node):
    def __init__(self):
        super().__init__('display_node') #type:ignore
        self.bridge = CvBridge()
        self.box_subscriber = self.create_subscription(String, 'bounding_boxes', self.callback, 10)
        self.boxes, self.total_mem, self.total_cpu, self.total_exec, self.total_latency, self.frame_id, self.total_frames, self.fps, self.id, self.gpu, self.gpu_mem = None, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        self.metrics = [self.total_cpu, self.total_mem, self.total_exec, self.total_latency, self.gpu, self.gpu_mem]
        self.box_annotator = sv.BoundingBoxAnnotator(color=COLORS)
        
        # Create a subscriber
    self.subscriber = self.create_subscription(
        BoundingBox,  # The message type
        'bounding_boxes',  # The topic name
        self.bounding_box_callback,  # The callback function
        10  # The queue size
    )

def bounding_box_callback(self, msg):
    # This function is called whenever a new message is received
    print(f"Received bounding box: {msg.box}, score: {msg.score}, class: {msg.class}")
    
    # use milliseconds instead?
    loop = Timeloop()
    @loop.job(interval=timedelta(seconds=1.000))
    def fps_counter(self):
        self.fps = self.totalframes
        self.total_frames = 0

    def callback(self, msg):
        self.boxes = msg.data
        metric_list = msg.header.split(' ')
        for index, metric in enumerate(self.metrics[1:len(self.metrics) - 1]):
            self.metric += metric_list[index + 1]
        self.total_frames = metric_list[0]

    def process_image(self, cv_image):
        # assumed boxes is a list of bounding boxes represented as [x, y, w, h]
        # for box in self.boxes: #type: ignore
        #     x, y, w, h = box
        #     cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        bounding_box_annotator = sv.BoundingBoxAnnotator()
        annotated_frame = bounding_box_annotator.annotate(
            scene=cv_image.copy(),
            detections=self.boxes
        )

        # Display the image in a new window
        cv2.imshow(f"FPS: {self.fps}", annotated_frame)

    def display_metrics(self):
        cv2.destroyAllWindows()
        print("="*40, "Average System Metrics", "="*40)
        avg_list = []
        for metric in self.metrics:
            avg_list.append(metric / self.total_frames)
        print(tabulate(avg_list, headers=("CPU", "Memory", "Execution Time", "Latency", "GPU", "GPU Memory")))
        raise SystemExit

def main(args=None):
    rclpy.init(args=args)
    display_node = DisplayNode()
    try:
        rclpy.spin(display_node)
    except SystemExit:    
        rclpy.logging.get_logger("Quitting").info('Done')
    display_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

# cv2 display:
key = ''
while key != 113:  # for 'q' key
    err = cam.grab(runtime)
    if err == sl.ERROR_CODE.SUCCESS:
        cam.retrieve_image(mat, sl.VIEW.LEFT_UNRECTIFIED)
        self.index += 1
        raw_image = mat.get_data()
        # cv2.imshow(f"ZED Camera", image)
        converted_image = cv2.cvtColor(raw_image, cv2.COLOR_RGBA2RGB)
        # cv2.imshow(f"ZED Camera", converted_image)
        
        self.publish_image(converted_image)
        key = cv2.waitKey(5)
    else:
        key = cv2.waitKey(5)
cv2.destroyAllWindows()       

# rolling average over numnber of frames
            # bounding_box.xmin = box[0]
            # bounding_box.ymin = box[1]
            # bounding_box.xmax = box[2]
            # bounding_box.ymax = box[3]
            # bounding_box.probability = score
            # bounding_box.Class = class_
        # Draw the bounding boxes on the image

from cv2 import rectangle, putText, FONT_HERSHEY_SIMPLEX
for box, score, class_ in zip(boxes, scores, classes):
    # Draw the bounding box
    rectangle(image_with_boxes, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)

    # Draw the class and score
    putText(image_with_boxes, f"{class_}: {score}", (box[0], box[1] - 5), FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # ...