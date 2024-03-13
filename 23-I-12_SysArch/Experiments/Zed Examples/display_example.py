import cv2
import pyzed.sl as sl
import psutil

def main():
    print("Running...")
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
    
    pre_mem = psutil.Process().memory_percent()

    key = ''
    while key != 113:  # for 'q' key
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            cam.retrieve_image(mat, sl.VIEW.SIDE_BY_SIDE)
            # cam.retrieve_image(mat, sl.VIEW.SIDE_BY_SIDE, sl.MEM.GPU)
            cv2.imshow("ZED", mat.get_data())
            key = cv2.waitKey(5)
        else:
            key = cv2.waitKey(5)
    cv2.destroyAllWindows()

    post_mem = psutil.Process().memory_percent()

    cam.close()
    print("\nFINISH")
    print(f"Memory usage: {post_mem - pre_mem}%")


if __name__ == "__main__":
    main()

            # # Convert the image to a numpy array
            # image_np = mat.get_data()

            # # Convert the numpy array to a CUDA GPU Mat
            # image_gpu = cv2.cuda_GpuMat()
            # image_gpu.upload(image_np)

            # # Convert the image to grayscale using CUDA
            # gray_gpu = cv2.cuda.cvtColor(image_gpu, cv2.COLOR_BGR2GRAY)

            # # Download the grayscale image to a numpy array
            # gray = gray_gpu.download()