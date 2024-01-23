import rclpy
from rclpy.node import Node
from std_msgs.msg import Image
from keras.datasets import fashion_mnist
from cv_bridge import cv_bridge
import cv2
import numpy as np

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher')
        self.model_publisher = self.create_publisher(Image, 'image_data', 10)
        self.timer = self.create_timer(1.0, self.publish_image)

        (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
        self.image_data = test_images
        self.index = 0

    def publish_image(self):
        image = self.image_data[self.index]
        msg = self.bridge.cv2_to_imgmsg(image, encoding='gray8')
        self.model_publisher.publish(msg)
        # self.get_logger().info(msg.data)
        self.index += 1
        

def main(args=None):
    rclpy.init(args=args)
    image_publisher = ImagePublisher()
    rclpy.spin(image_publisher)
    image_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
