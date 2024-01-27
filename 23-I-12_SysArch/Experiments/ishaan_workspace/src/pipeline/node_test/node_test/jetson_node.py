import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
import tensorflow as tf
import numpy as np

class CNNNode(Node):
    def __init__(self):
        super().__init__('cnn_node')
        
        # Create a publisher
        self.model_publisher = self.create_publisher(String, 'classification', 10)
        # Create a subscriber
        self.camera_subscriber = self.create_subscription(Image, 'image_data', self.callback, 10)
    
    def callback(self, msg):
        self.get_logger().info(f"Received: {msg.header}")
        self.publish_result(self.process_data(msg.data))
    
    def process_data(self, data):
        # Load model from file
        model = tf.keras.models.load_model('/home/ishaan_datta/Downloads/model.h5')
        # Normalize image values
        print(type(data))
        data = np.array(data)
        data = data / 255.0
        data = np.reshape(data, (1, data.shape[0], data.shape[1], 1))
        # Add RGB values
        data = tf.image.grayscale_to_rgb(tf.expand_dims(data, axis=-1))
        # Resize images to 32x32
        data = tf.image.resize(data, (32, 32))
        # Produce and one-hot encode label output of model
        prediction = self.model.predict(data)
        prediction = np.argmax(prediction, axis=1)
        return prediction
    
    def publish_result(self, result):
        msg = String()
        msg.data = f'Object identified as: {result}'
        self.model_publisher.publish(msg)
        self.get_logger().info(msg.data)

# colcon build --packages-select node_test
# make it delay sending until package is received and processed (buffer processing)

def main(args=None):
    rclpy.init(args=args)
    cnn_node = CNNNode()
    rclpy.spin(cnn_node)
    cnn_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
