import os
import cv2

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from example_interfaces.srv import Trigger

class DisplayNode(Node):
    def __init__(self):
        super().__init__('display_node') #type:ignore
        self.bridge = CvBridge()
        self.box_subscriber = self.create_subscription(String, 'bounding_box_coords', self.callback, 10)
        self.client = self.create_client(Trigger, 'image_data_service')
        
    def callback(self, msg):
        self.boxes = list(msg.data)
        req = Trigger.Request()
        future = self.client.call_async(req)
        future.add_done_callback(self.future_callback)
    
    def future_callback(self, future):
        try:
            response = future.result()
            if response.success:
                image_data = response.message  # Assuming the message is the image data
                cv_image = self.bridge.imgmsg_to_cv2(image_data, "bgr8")
                self.process_image(cv_image)
        except Exception as e:
            self.get_logger().error('Service call failed %r' % (e,))

    # assumed boxes is a list of bounding boxes represented as [x, y, w, h]
    def process_image(self, cv_image):
        # For example, if `boxes` is a list of bounding boxes, each represented as [x, y, w, h]

        for box in self.boxes: #type: ignore
            x, y, w, h = box
            cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the image in a new window
        cv2.imshow("Image window", cv_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    display_node = DisplayNode()
    rclpy.spin(display_node)
    display_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()