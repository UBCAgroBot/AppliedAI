import os
import cv2

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class CNNNode(Node):
    def __init__(self):
        super().__init__('display_node') #type:ignore
        self.bridge = CvBridge()
        self.model_publisher = self.create_publisher(String, 'bounding_box_coords', 10)
        self.camera_subscriber = self.create_subscription(Image, 'image_data', self.callback, 10)
        # self.model = 
    
    def callback(self, msg):
        self.get_logger().info(f"Received: {msg.header}")
        now = self.get_clock().now()
        latency = now - Time.from_msg(msg.header.stamp)
        print(f"Message transmisison latency: {latency.nanoseconds / 1e6} milliseconds")
        self.preprocess_data(msg.data)

def main(args=None):
    rclpy.init(args=args)
    display_node = DisplayNode()
    rclpy.spin(cnn_node)
    cnn_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
