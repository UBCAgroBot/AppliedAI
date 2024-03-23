    def video_writer(self):
        # initialize the video capture object
        cap = cv2.VideoCapture("examples/1.mp4")

        # grab the width, height, and fps of the frames in the video stream.
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))

        # initialize the FourCC and a video writer object
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output = cv2.VideoWriter('output.mp4', fourcc, fps, (frame_width, frame_height))
        output.write(frame)
        output.release()

def verify_colorspace(self):
    lo_square = np.full((10, 10, 3), LIGHT_GREEN, dtype=np.uint8) / 255.0
    do_square = np.full((10, 10, 3), DARK_GREEN, dtype=np.uint8) / 255.0
    plt.subplot(1, 2, 1)
    plt.imshow(hsv_to_rgb(do_square))
    plt.subplot(1, 2, 2)
    plt.imshow(hsv_to_rgb(lo_square))
    plt.show()

def verify_roi(self):
    # r = cv2.selectROI(self.image)
    # imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    imCrop = self.image[ROI_Y:ROI_Y+ROI_H, ROI_X:ROI_X+ROI_W]
    plt.subplot(1, 2, 1)
    plt.imshow(imCrop)

# sliders and also image reading and while loop for displaying the image
# threshold slider