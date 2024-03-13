import time
import os
import psutil
import cv2

# from numba import jit
# argparse for choosing model

import rclpy
from rclpy.time import Time
from rclpy.node import Node
from std_msgs.msg import Header, String
from sensor_msgs.msg import Image
from BoundingBox.msg import BoundingBox
from cv_bridge import CvBridge, CvBridgeError

class JetsonNode(Node):
    def __init__(self):
        super().__init__('jetson_node') #type:ignore
        self.bridge = CvBridge()
        
        self.inference = BoundingBox()
        
        self.model_publisher = self.create_publisher(BoundingBox, 'bounding_boxes', 10)
        self.camera_subscriber = self.create_subscription(Image, 'image_data', self.callback, 10)
        self.camera_subscriber
        self.frames, self.cpu, self.mem, self.time, self.latency, self.pid, self.frame_id, self.save = 0, 0, 0, 0, 0, 0, 0, True
        self.tensorrt_init()
    
    def tensorrt_init(self):
        try:
            self.model = torch.jit.load("trt_model.ts").cuda()
        except Exception as e:
            try:
                model = torch.load('yolov5s.pt', model_math='fp32').eval().to("cuda") # replace with ONNX
                self.model = torch_tensorrt.compile(model, inputs=[torch_tensortt([1, 3, 1280, 1280])], enabled_precisions={'torch.half'}, debug=True)
                self.save = False
            except Exception as e:
                self.get_logger().info(f"Error: {e}")
                raise SystemExit
        finally:
            self.get_logger().info("Model loaded successfully")
    
    def callback(self, msg):
        now = self.get_clock().now()
        self.get_logger().info(f"Received: {msg.header.frame_id}")
        latency = now - Time.from_msg(msg.header.stamp)
        print(f"Latency: {latency.nanoseconds / 1e6} milliseconds")
        
        try:
            image  = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
        except CvBridgeError as e:
            print(e)
        
        # height, width, channels = image.shape
        # print(height, width, channels)
        
        self.latency, self.frame_id, self.frames = latency.nanoseconds / 1e6, msg.header.frame_id, self.frames + 1
        self.preprocessing(image)
        
    
    def preprocessing(self, image):
        # Resize and normalize the image
        resized_image = cv2.resize(image, (1280, 1280))  # YOLOv5 uses a 640x640 input size
        normalized_image = resized_image / 255.0  # Normalize pixel values to [0, 1]
        input_image = torch.from_numpy(normalized_image).permute(2, 0, 1).float()  # Convert to torch tensor and rearrange dimensions
        output = input_image.unsqueeze(0)  # Add a batch dimension
        self.detection(output)

    def detection(self, data):
        # pid = os.getpid()
        # print(pid)

        tic = time.perf_counter_ns()
        # pre_mem = psutil.Process(pid).memory_percent()
        # pre_cpu = psutil.Process(pid).cpu_percent(interval=None)
        with torch.no_grad():
            detections = self.model(data)
        # post_cpu = psutil.Process(pid).cpu_percent(interval=None)
        # post_mem = psutil.Process(self.pid).memory_percent()
        toc = time.perf_counter_ns()
        
        # self.cpu = ((self.post_cpu-self.pre_cpu)/self.time) * 100
        # self.mem = post_mem - pre_mem
        self.time = (toc-tic)/1e6
        self.gpu = 0 # gpu.load*100
        self.gpu_mem = 0 # (gpu.memoryUsed / gpu.memoryTotal) * 100
        
        # self.get_logger().info(f"CPU usage: {self.cpu}%")
        # self.get_logger().info(f"GPU usage: {self.gpu}%")
        # self.get_logger().info(f"GPU VRAM usage: {self.gpu_mem}%")
        # self.get_logger().info(f"Memory usage: {self.mem}%")
        # self.get_logger().info(f"Execution time: {self.time} milliseconds")
        # annotated_frame = results[0].plot()
        self.publish_result(detections)
        self.detections.clear()
    
    def postprocessing(self, output):
        
        # self.inference_result = InferenceResult()
        # b = box.xyxy[0].to('cpu').detach().numpy().copy()  # get box coordinates in (top, left, bottom, right) format
        # c = box.cls
        for r in results:
            boxes = r.boxes
            for box in boxes:
                self.inference.box = box
                self.inference.score = r.scores
                self.inference.class_num = r.pred
                self.model_publisher.publish(self.inference)

        # self.yolov8_inference.yolov8_inference.append(self.inference_result)
        
        # Apply non-maximum suppression
        boxes = output[..., :4]  # Bounding box coordinates
        scores = output[..., 4]  # Objectness scores
        classes = output[..., 5:].argmax(dim=-1)  # Class labels
        keep = nms(boxes, scores, iou_threshold=0.5)  # Indices of boxes to keep
        self.publish_result(boxes[keep], scores[keep], classes[keep])
    
    def publish_result(self, boxes, scores, classes):
        for box, score, classes in zip(boxes, scores, classes):
            msg = BoundingBox()
            msg.box = box.tolist()
            msg.score = score.item()
            msg.classes = classes.item()
            
            header = Header()
            header.metrics = f"{self.frame_id} {self.cpu} {self.mem} {self.time} {self.latency} {self.gpu} {self.gpu_mem} {self.frames} {self.fps} {self.id}"
            
            self.get_logger().info(msg.data)
            self.publisher.publish(msg)
    
    def display_metrics(self):
        self.get_logger().info(f'Frame loss: {((self.frames/self.frame_id)*100):0.1f}')
        if self.save == False:
            pass
            # trt_traced_model = torch.jit.trace(trt_gm, inputs)
            # torch.jit.save(trt_traced_model, "trt_model.ts")
        raise SystemExit

def main(args=None):
    rclpy.init(args=args)
    jetson_node = JetsonNode()
    try:
        rclpy.spin(jetson_node)
    except KeyboardInterrupt:
        print("qq...")
        jetson_node.display_metrics()
        torch._dynamo.reset()
        rclpy.logging.get_logger("Quitting").info('Done')
    except SystemExit:   
        print("qqq...")
        jetson_node.display_metrics()
        torch._dynamo.reset()
        rclpy.logging.get_logger("Quitting").info('Done')

    rclpy.spin(jetson_node)
    jetson_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()