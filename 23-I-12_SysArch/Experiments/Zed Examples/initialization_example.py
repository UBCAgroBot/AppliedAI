import pyzed.sl as sl

# The API can be used with two different video inputs: the ZED live video (Live mode) or video files recorded in SVO format with the ZED API (Playback mode).

# nitial parameters let you adjust camera resolution, FPS, depth sensing parameters and more. These parameters can only be set before opening the camera and cannot be changed while the camera is in use.

# Create a ZED camera object
zed = sl.Camera()

# Set configuration parameters
init_params = sl.InitParameters()
init_params.camera_resolution = sl.RESOLUTION.HD1080 
init_params.camera_fps = 30 

# Open the camera
err = zed.open(init_params)
if (err != sl.ERROR_CODE.SUCCESS) :
    exit(-1)

# You can set the following initial parameters:

#     Camera configuration parameters, using the camera_* entries (resolution, image flip...).
#     SDK configuration parameters, using the sdk_* entries (verbosity, GPU device used...).
#     Depth configuration parameters, using the depth_* entries (depth mode, minimum distance...).
#     Coordinate frames configuration parameters, using the coordinate_* entries (coordinate system, coordinate units...).
#     SVO parameters to use Stereolabs video files with the ZED SDK (filename, real-time mode...)

# Get camera information (serial number)
zed_serial = zed.get_camera_information().serial_number
print("Hello! This is my serial number: ", zed_serial)

# Close the camera
zed.close()