import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from keras.datasets import fashion_mnist
import numpy as np
from std_msgs.msg import Header
from rclpy.time import Time

class ImagePublisher(Node):
    def __init__(self):
        super().__init__('image_publisher') #size, encoding, weifth, height, data
        self.model_publisher = self.create_publisher(Image, 'image_data', 10)
        self.timer = self.create_timer(1.0, self.publish_image)

        (train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
        self.image_data = test_images
        self.index = 0
        
        

    def publish_image(self):
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