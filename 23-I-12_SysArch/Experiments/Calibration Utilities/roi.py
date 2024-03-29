import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

os.chdir("23-I-12_SysArch/Experiments/Calibration Utilities")
image = cv2.imread("test.jpg")

height, width, _ = image.shape 
window_height, window_width = height, width

roi_x = 1
roi_w = width
roi_y = 1
roi_h = height

def onTrack1(val):
    global roi_x
    roi_x=val
    print('roi x',roi_x)
def onTrack2(val):
    global roi_w
    roi_w=val
    print('roi w',roi_w)
def onTrack3(val):
    global roi_y
    roi_y=val
    print('roi y',roi_y)
def onTrack4(val):
    global roi_h
    roi_h=val
    print('roi h',roi_h)

cv2.namedWindow('roi calibration', cv2.WINDOW_NORMAL)
cv2.resizeWindow('roi calibration', window_width, window_height)
cv2.moveWindow('roi calibration',0,0)

cv2.createTrackbar('x pos','roi calibration',1,width-1,onTrack1)
cv2.createTrackbar('width','roi calibration',width,width,onTrack2)
cv2.createTrackbar('y pos','roi calibration',1,height-1,onTrack3)
cv2.createTrackbar('height','roi calibration',height,height,onTrack4)

while True:
    frame = image[roi_y:roi_h+1, roi_x:roi_w+1]
    
    blank_image = np.zeros((window_height, window_width, 3), np.uint8)
    x_offset = max((window_width - frame.shape[1]) // 2, 0)
    y_offset = max((window_height - frame.shape[0]) // 2, 0)
    
    blank_image[y_offset:y_offset+frame.shape[0], x_offset:x_offset+frame.shape[1]] = frame
    
    cv2.imshow('roi calibration', blank_image)
    if cv2.waitKey(1) & 0xff ==ord('q'):
        break

cv2.destroyAllWindows()