import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from keras.datasets import fashion_mnist
import numpy as np
from std_msgs.msg import Header
from rclpy.time import Time
import sys
from cv_bridge import CvBridge
import cv2

# pip install opencv-python
# pip install ros2-cv-bridge

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher') #size, encoding, weifth, height, data
        self.model_publisher = self.create_publisher(Image, 'image_data', 10)
        self.timer = self.create_timer(1.0, self.publish_image)
        self.bridge = CvBridge()

        (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
        self.image_data = test_images
        self.index = 0

    def publish_image(self):
        cap = cv2.VideoCapture(0)  # 0 is the default camera. Change it if you have multiple cameras.
        ret, frame = cap.read()
        
        if ret:
            image_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")

            header = Header()
            header.stamp = self.get_clock().now().to_msg()  # Current system time
            header.frame_id = str(self.index)  # Index as frame_id

            image_msg.header = header
            image_msg.is_bigendian = 0 
            image_msg.step = image_msg.width * 3  # 3 bytes per pixel for bgr8

            self.model_publisher.publish(image_msg)
            self.get_logger().info('Published image frame: %d' % self.index)
            self.index += 1

        cap.release()
        
        header = Header()
        header.stamp = self.get_clock().now().to_msg()  # Current system time
        header.frame_id = str(self.index)  # Index as frame_id

        image_msg = Image()
        image_msg.header = header
        height, width, encoding = 28, 28, 'mono8'
        image_data = self.image_data[self.index]
        image_msg.height = height
        image_msg.width = width
        image_msg.encoding = encoding
        image_msg.is_bigendian = 0 
        image_msg.step = width 
        image_msg.data = image_data.flatten().tobytes()
        msg_size = sys.getsizeof(image_msg) #compression later? -> pseudo network bandwidth measurement, sum total bytes of all data sent, divide by time elapsed for average bandwidth
        
        
        self.model_publisher.publish(image_msg)
        # self.get_logger().info(self.index) #figure out logging
        print(self.index)
        self.index += 1
        

def main(args=None):
    rclpy.init(args=args)
    image_publisher = ImagePublisher()
    rclpy.spin(image_publisher)
    image_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()