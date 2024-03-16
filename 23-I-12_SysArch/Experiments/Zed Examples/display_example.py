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
    print(pre_mem)

    key = ''
    while key != 113:  # for 'q' key
        post_mem = psutil.Process().memory_percent()
        
        print(f"Memory usage: {(post_mem - pre_mem) * 100:.2f}%")
        err = cam.grab(runtime)
        if err == sl.ERROR_CODE.SUCCESS:
            cam.retrieve_image(mat, sl.VIEW.LEFT)
            # Convert the image to a numpy array
            image_np = mat.get_data()

            # Convert the numpy array to a CUDA GPU Mat
            image_gpu = cv2.cuda_GpuMat()
            image_gpu.upload(image_np)

            # Convert the image to grayscale using CUDA
            gray_gpu = cv2.cuda.cvtColor(image_gpu, cv2.COLOR_BGRA2GRAY)
            
            # Download the grayscale image to a numpy array
            gray = gray_gpu.download()
            cv2.imshow("ZED", gray)
            key = cv2.waitKey(5)
        else:
            key = cv2.waitKey(5)
    cv2.destroyAllWindows()

    cam.close()
    print("\nFINISH")

if __name__ == "__main__":
    main()