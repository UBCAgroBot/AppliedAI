import time
import sys
import cv2
import os
from pathlib import Path

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Header
from cv_bridge import CvBridge, CvBridgeError

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher') #type: ignore
        self.bridge = CvBridge()
        self.download_path = str(Path.home() / 'Downloads')
        self.frames = self.import_image_files()
        self.model_publisher = self.create_publisher(Image, 'image_data', 10)
        self.publish_image()
    
    def import_image_files(self):
        images = []
        for filename in os.listdir(self.download_path):
            img = cv2.imread(os.path.join(self.download_path, filename))
            if img is not None:
                images.append(img)
        return images
    
    def import_image_frames(self):
        # zed implementation goes here
        pass

    def publish_image(self):
        tic = time.perf_counter()
        total_data = 0
        for index, frame in enumerate(self.frames):
            header = Header()
            header.stamp = self.get_clock().now().to_msg()
            header.frame_id = str(index) 

            try:
                image_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            except CvBridgeError as e:
                self.get_logger().info(e)
                print(e)
                
            image_msg.header = header
            image_msg.is_bigendian = 0 
            image_msg.step = image_msg.width * 3

            self.model_publisher.publish(image_msg)
            size = sys.getsizeof(image_msg)
            self.get_logger().info(f'Published image frame: {index} with message size {size}')
            total_data += size
            
        toc = time.perf_counter()
        bandwidth = total_data / (toc - tic)
        self.get_logger().info(f'Published {len(self.frames)} images in {toc - tic:0.4f} seconds with average network bandwidth of {bandwidth} bytes per second')

def main(args=None):
    rclpy.init(args=args)
    image_publisher = ImagePublisher()
    rclpy.spin(image_publisher)
    image_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()