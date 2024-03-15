from ultralytics import YOLO
import cv2
# import pyzed.sl as sl
import time
import os

# from models.pycuda_api import TRTEngine

os.chdir('/home/user/AppliedAI/23-I-12_SysArch/Experiments/ishaan_workspace/src/pipeline/node_test/node_test')
tensorrt_model = YOLO('yolov8x_onnx.engine')
success = 1
vidObj = cv2.VideoCapture('City.mp4') 
while success: 
    success, image = vidObj.read() 
    tic = time.perf_counter_ns()
    results = tensorrt_model(image, stream=True, show=True)
    print(f"{time.perf_counter_ns() - tic}/1e6 ms")