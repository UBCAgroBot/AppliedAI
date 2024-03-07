import pyzed.sl as sl

# Create a ZED camera object
zed = sl.Camera()

# Set configuration parameters
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.AUTO # Use HD720 opr HD1200 video mode, depending on camera type.
init_params.camera_fps = 30 # Set fps at 30

# Open the camera
err = zed.open(init_params)
if (err != sl.ERROR_CODE.SUCCESS) :
    exit(-1)

# Grab an image
if (zed.grab() == sl.ERROR_CODE.SUCCESS) :
    # Capture 50 frames and stop
    i = 0
    image = sl.Mat()
    while (i < 50) :
        # Grab an image
        if (zed.grab() == sl.ERROR_CODE.SUCCESS) :
            # A new image is available if grab() returns SUCCESS
            zed.retrieve_image(image, sl.VIEW.LEFT) # Get the left image
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.IMAGE) # Get the timestamp at the time the image was captured
            print("Image resolution: {0} x {1} || Image timestamp: {2}\n".format(image.get_width(), image.get_height(),
                    timestamp.get_milliseconds()))
            i = i+1

# Close the camera
zed.close()

# Create a ZED camera object
zed = sl.Camera()

# Enable recording with the filename specified in argument
output_path = sys.argv[0]
recordingParameters = sl.RecordingParameters()
recordingParameters.compression_mode = sl.SVO_COMPRESSION_MODE.H264
recordingParameters.video_filename = output_path
err = zed.enable_recording(recordingParameters)

while not exit_app:
    # Each new frame is added to the SVO file
    zed.grab()

# Disable recording
zed.disable_recording()

# Create a ZED camera object
zed = sl.Camera()

# Set SVO path for playback
input_path = sys.argv[1]
init_parameters = sl.InitParameters()
init_parameters.set_from_svo_file(input_path)

# Open the ZED
zed = sl.Camera()
err = zed.open(init_parameters)

svo_image = sl.Mat()
while not exit_app:
    if zed.grab() == sl.ERROR_CODE.SUCCESS:
        # Read side by side frames stored in the SVO
        zed.retrieve_image(svo_image, sl.VIEW.SIDE_BY_SIDE)
        # Get frame count
        svo_position = zed.get_svo_position()
    elif zed.grab() == sl.ERROR_CODE.END_OF_SVOFILE_REACHED:
        print("SVO end has been reached. Looping back to first frame")
        zed.set_svo_position(0)

# Create an RGBA sl.Mat object
image_zed = sl.Mat(zed.get_camera_information().camera_resolution.width, zed.get_camera_information().camera_resolution.height, sl.MAT_TYPE.U8_C4)
# Retrieve data in a numpy array with get_data()
image_ocv = image_zed.get_data()

# In Python, OpenCV stores images in NumPy arrays. Since the ZED SDK uses its own sl.Mat class to store image data, we provide a function get_data() to convert the sl.Mat matrix into a NumPy array.

# UVC capture: You can also use the ZED as a standard UVC camera in OpenCV to capture raw stereo video
import cv2
import numpy

# Open the ZED camera
cap = cv2.VideoCapture(0)
if cap.isOpened() == 0:
    exit(-1)

# Set the video resolution to HD720 (2560*720)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True :
    # Get a new frame from camera
    retval, frame = cap.read()
    # Extract left and right images from side-by-side
    left_right_image = numpy.split(frame, 2, axis=1)
    # Display images
    cv2.imshow("frame", frame)
    cv2.imshow("right", left_right_image[0])
    cv2.imshow("left", left_right_image[1])
    if cv2.waitKey(30) >= 0 :
        break

exit(0)

# Set exposure to 50% of camera framerate
zed.set_camera_settings(sl.VIDEO_SETTINGS.EXPOSURE, 50)
# Set white balance to 4600K
zed.set_camera_settings(sl.VIDEO_SETTINGS.WHITE_BALANCE, 4600)
# Reset to auto exposure
zed.set_camera_settings(sl.VIDEO_SETTINGS.EXPOSURE, -1)