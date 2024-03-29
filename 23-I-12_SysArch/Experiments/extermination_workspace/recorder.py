def video_writer(self, frame, fps=20):
    # grab the width, height, and fps of the frames in the video stream.
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]

    # initialize the FourCC and a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    output = cv2.VideoWriter('output.mp4', fourcc, fps, (frame_width, frame_height))
    output.write(frame)
    output.release()

import cv2
import numpy as np

# Assume you have a list of frames and corresponding time intervals
frames = [...]  # This should be a list of numpy arrays representing your images

# Assume you have a list of timestamps for each frame
timestamps = [...]  # This should be a list of timestamps

# Calculate the time intervals
time_intervals = [j-i for i, j in zip(timestamps[:-1], timestamps[1:])]
# Please replace the timestamps with your actual data. The timestamps should be in a format that supports subtraction, such as datetime.datetime objects or Unix timestamps (seconds since the epoch).

# Define the codec using VideoWriter_fourcc and create a VideoWriter object
# We arbitrarily use 25 FPS here for the output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 25.0, (640, 480))

for frame, interval in zip(frames, time_intervals):
    # Calculate how many times to duplicate the frame based on the time interval
    duplicates = int(round(interval * 25))  # 25 is the FPS of the output video

    for _ in range(duplicates):
        # Write the frame to the output video
        out.write(frame)

# Release the VideoWriter when done
out.release()