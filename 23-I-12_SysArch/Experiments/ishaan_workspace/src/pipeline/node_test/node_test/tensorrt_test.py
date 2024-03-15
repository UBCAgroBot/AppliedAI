from ultralytics import YOLO
import cv2
# import pyzed.sl as sl
import time
import os

# from models.pycuda_api import TRTEngine

os.chdir('/home/user/AppliedAI/23-I-12_SysArch/Experiments/ishaan_workspace/src/pipeline/node_test/node_test')
tensorrt_model = YOLO('yolov8x_pt.engine')
success = 1
vidObj = cv2.VideoCapture('City.mp4') 
# while success: 
#     success, image = vidObj.read() 
    # tic = time.perf_counter_ns()
    
    # tensorrt_model.predict(image, device='cuda:0', )
    # print(results.speed)
    # for result in results:
    #     result.show()
    # for result in results:
    #     annotated_frame = result[0].plot()

    # Display the annotated frame
    # cv2.imshow("YOLOv8 Inference", annotated_frame)
    # print(f"{(time.perf_counter_ns() - tic)/1e6} ms")

while vidObj.isOpened():
    # Read a frame from the video
    success, frame = vidObj.read()
    
    if success:
        results = tensorrt_model(frame, stream=True)
        for result in results:
            # annotated_frame = result[0].plot()
            # print(result[0].speed)
            # print(repr(result[1]))
            # cv2.imshow("YOLOv8 Inference", annotated_frame)
            # Break the loop if 'q' is pressed
            # if cv2.waitKey(1) & 0xFF == ord("q"):
            #     break
            pass
    else:
        break

# Release the video capture object and close the display window
vidObj.release()
# cv2.destroyAllWindows()