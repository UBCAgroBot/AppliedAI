import rclpy
import cv2
from rclpy.time import Time
from rclpy.node import Node
from std_msgs.msg import Header
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class PythonSub(Node):
    def __init__(self):
        super().__init__('sub_node') #type:ignore
        self.bridge = CvBridge()
        self.camera_subscriber = self.create_subscription(Image, 'image_data', self.callback, 10)
    
    def callback(self, msg):
        now = self.get_clock().now()
        latency = now - Time.from_msg(msg.header.stamp)
        print(f"Message transmisison latency: {latency.nanoseconds / 1e6} milliseconds")
        try:
            cv_image  = self.bridge.imgmsg_to_cv2(msg)
            cv2.imshow("ZED, cv_image")
        except CvBridgeError as e:
            self.get_logger().info(e)
            print(e)

def main(args=None):
    rclpy.init(args=args)
    sub_node = PythonSub()
    try:
        rclpy.spin(sub_node)
    except SystemExit:   
        print("josy...")
        rclpy.logging.get_logger("Quitting").info('Done')
    sub_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()