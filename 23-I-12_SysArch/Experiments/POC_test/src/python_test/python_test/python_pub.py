import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Header, String

import cv2
from cv_bridge import CvBridge, CvBridgeError
import pyzed.sl as sl

class PythonPub(Node):
    def __init__(self):
        super().__init__('pub_node') #type: ignore
        self.bridge = CvBridge()
        self.model_publisher = self.create_publisher(Image, 'image_data', 10)
        print(cv2.__version__)
    
        def camera_publisher(self):
            init = sl.InitParameters()
            cam = sl.Camera()
            
            if not cam.is_opened():
                pass
            status = cam.open(init)
            if status != sl.ERROR_CODE.SUCCESS:
                print(repr(status))
                exit()
            
            runtime = sl.RuntimeParameters()
            mat = sl.Mat()
            
            key = ''
            while key != 113:  # for 'q' key
                err = cam.grab(runtime)
                if err == sl.ERROR_CODE.SUCCESS:
                    cam.retrieve_image(mat, sl.VIEW.LEFT_UNRECTIFIED)
                    image = mat.get_data()
                    self.publish_image(image)
                    key = cv2.waitKey(5)
                else:
                    key = cv2.waitKey(5)
            cam.close()
    
        def publish_image(self, image):
            header = Header()
            header.stamp = self.get_clock().now().to_msg()
            try:
                image_msg = self.bridge.cv2_to_imgmsg(image, encoding='8UC4')
            except CvBridgeError as e:
                self.get_logger().info(e)
                print(e)
                
            image_msg.header = header
            image_msg.is_bigendian = 0 
            image_msg.step = image_msg.width * 3

            self.model_publisher.publish(image_msg)

def main(args=None):
    rclpy.init(args=args)
    pub_node = PythonPub()
    try:
        rclpy.spin(pub_node)
    except SystemExit:
        rclpy.logging.get_logger("Quitting").info('Done')
    pub_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()