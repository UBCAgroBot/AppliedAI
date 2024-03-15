from ultralytics import YOLO
import cv2
# import pyzed.sl as sl
import time
import os

# from models.pycuda_api import TRTEngine

def main():
    os.chdir('/home/user/AppliedAI/23-I-12_SysArch/Experiments/ishaan_workspace/src/pipeline/node_test/node_test')
    tensorrt_model = YOLO('yolov8x_onnx.engine')
    print(os.getcwd())
    # init = sl.InitParameters()
    # cam = sl.Camera()
    # if not cam.is_opened():
    #     print("Opening ZED Camera...")
    # status = cam.open(init)
    # if status != sl.ERROR_CODE.SUCCESS:
    #     print(repr(status))
    #     exit()

    # runtime = sl.RuntimeParameters()
    # mat = sl.Mat()
    # image_np = mat.get_data()

    # key = ''
    # while key != 113:  # for 'q' key
    #     err = cam.grab(runtime)
    #     if err == sl.ERROR_CODE.SUCCESS:
    #         cam.retrieve_image(mat, sl.VIEW.LEFT)
    #         # Convert the image to a numpy array
    #         image_np = mat.get_data()
    #         tic = time.perf_counter_ns()
    #         results = tensorrt_model('city.mp4', stream=True, show=True)
    #         print(f"{time.perf_counter_ns() - tic}/1e6 ms")
    #         # results.show()
    #         # cv2.imshow("ZED", gray)
    #         key = cv2.waitKey(5)
    #     else:
    #         key = cv2.waitKey(5)
    # cv2.destroyAllWindows()
    # cam.close()
    
    
    tic = time.perf_counter_ns()
    results = tensorrt_model('city.mp4', stream=True, show=True)
    print(f"{time.perf_counter_ns() - tic}/1e6 ms")

main()