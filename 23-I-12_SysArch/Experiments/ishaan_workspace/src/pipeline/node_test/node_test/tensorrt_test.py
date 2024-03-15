from ultralytics import YOLO
import cv2
import pyzed.sl as sl

# from models.pycuda_api import TRTEngine

def main():
    tensorrt_model = YOLO('yolov8x_onnx.engine')

    init = sl.InitParameters()
    cam = sl.Camera()
    if not cam.is_opened():
        print("Opening ZED Camera...")
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
            cam.retrieve_image(mat, sl.VIEW.LEFT)
            # Convert the image to a numpy array
            image_np = mat.get_data()
            results = tensorrt_model(image_np, stream=True, show=True)
            # cv2.imshow("ZED", gray)
            key = cv2.waitKey(5)
        else:
            key = cv2.waitKey(5)
    cv2.destroyAllWindows()
    cam.close()

main()