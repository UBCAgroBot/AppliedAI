from time import perf_counter
import sys
import cv2
import os
from pathlib import Path
import pyzed.sl as sl

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Header, String
from cv_bridge import CvBridge, CvBridgeError
from example_interfaces.srv import Trigger

class CameraNode(Node):
    def __init__(self):
        super().__init__('camera_node') #type: ignore
        self.bridge = CvBridge()
        self.download_path = str(Path.home() / 'Downloads')
        # replace self.camera with parameter
        self.index, self.camera, self.type = 0, True, "8UC4"
        self.off_publisher = self.create_publisher(String, 'off', 10)
        self.model_publisher = self.create_publisher(Image, 'image_data', 10)

        if self.camera == True:
            self.camera_publisher()
        else:
            self.type = "JPG"
            self.picture_publisher()
    
    def picture_publisher(self):
        for filename in os.listdir(self.download_path):
            img = cv2.imread(os.path.join(self.download_path, filename))
            if img is not None:
                self.index += 1
                self.publish_image(img)
    
    def camera_publisher(self):
        init = sl.InitParameters()
        cam = sl.Camera()

        if not cam.is_opened():
            print("Opening ZED Camera ")
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
                self.index += 1
                raw_image = mat.get_data()
                # cv2.imshow(f"ZED Camera", image)
                converted_image = cv2.cvtColor(raw_image, cv2.COLOR_BGRA2RGB)
                self.publish_image(converted_image)
                key = cv2.waitKey(5)
            else:
                key = cv2.waitKey(5)

        # cv2.destroyAllWindows()                
        cam.close()
        print("ZED Camera closed")
        raise SystemExit
        # raise KeyboardInterrupt

    def publish_image(self, image):
        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = str(self.index) 

        try:
            image_msg = self.bridge.cv2_to_imgmsg(image, encoding='RGB8')
        except CvBridgeError as e:
            print(e)
        image_msg.header = header
        image_msg.is_bigendian = 0 
        image_msg.step = image_msg.width * 3

        self.model_publisher.publish(image_msg)
        self.get_logger().info(f'Published image frame: {self.index}')

def main(args=None):
    rclpy.init(args=args)
    camera_node = CameraNode()
    try:
        rclpy.spin(camera_node)
    except SystemExit:
        print("works")
        camera_node.display_metrics()
        rclpy.logging.get_logger("Quitting").info('Done')
    except KeyboardInterrupt:
        print("works")
        rclpy.logging.get_logger("Quitting").info('Done')
        camera_node.display_metrics()
    camera_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()