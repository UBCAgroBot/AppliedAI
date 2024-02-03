import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import Image
import tensorflow as tf
import numpy as np
import time
import psutil

# self.get_logger().info(f"Received: {msg.header}") works, logger file and to terminal would be nice -> dedicated module
# header information should be passed from camera node with metrics logged from that side and all in csv or what?

class CNNNode(Node):
    def __init__(self):
        super().__init__('cnn_node')
        
        # Create a publisher
        self.model_publisher = self.create_publisher(String, 'classification', 10)
        # Create a subscriber
        self.camera_subscriber = self.create_subscription(Image, 'image_data', self.callback, 10)
        # Load model
        self.model = tf.keras.models.load_model('/home/ishaan_datta/Downloads/model.h5') # replace with general directory within resource?
        
        # self.timer = self.create_timer(1.0, self.timer_callback)
        
    def timer_callback(self): # for testing purposes, adds overhead to system, measures cpu usage of process
        pass
        
    
    def callback(self, msg):
        self.get_logger().info(f"Received: {msg.header}")
        now = self.get_clock().now()
        latency = now - rclpy.time.Time.from_msg(msg.header.stamp)
        print(f"Latency: {latency.nanoseconds / 1e6} milliseconds")
        self.publish_result(self.process_data(msg.data))
    
    def process_data(self, data):
        start_time = time.time()
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
        cpu_usage = psutil.cpu_percent() 
        # cpu_usage = psutil.Process(pid).cpu_percent() # where pid is the process ID of your ROS 2 node
        # psutil.Process(pid).memory_percent()
        memory_usage = psutil.virtual_memory().percent
        prediction = np.argmax(prediction, axis=1)
        end_time = time.time()
        execution_time = end_time - start_time
        return prediction, execution_time # could possibly use function decorator to time execution of function
    
    def publish_result(self, result, execution_time):
        msg = String()
        msg.header.frame_id = f'execution_time: {execution_time}'
        msg.data = f'Object identified as: {result}'
        msg.header.stamp = self.get_clock().now().to_msg()
        self.model_publisher.publish(msg)
        self.get_logger().info(msg.data)

# colcon build --packages-select node_test
# make it delay sending until package is received and processed (buffer processing)
# max cpu usage, initialized variable + comparison, average using metrics later, how to find process IDs

def main(args=None):
    rclpy.init(args=args)
    cnn_node = CNNNode()
    rclpy.spin(cnn_node)
    cnn_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
