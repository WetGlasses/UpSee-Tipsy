import cv2 as cv
import argparse
import os
import time
import pandas as pd
import math
import numpy as np

max_value = 255
max_value_H = 360//2
low_H = 0
low_S = 0
low_V = 0
high_H = max_value_H
high_S = max_value
high_V = max_value

window_capture_name = 'Video Feed'
window_calibrated_name = 'After Distortion correction'
window_detection_name = 'Detection after thresholding'
window_perspective_name = 'After perspective correction'

low_H_name = 'Low H'
low_S_name = 'Low S'
low_V_name = 'Low V'
high_H_name = 'High H'
high_S_name = 'High S'
high_V_name = 'High V'


Pre_Cal = True

def on_low_H_thresh_trackbar(val):
    global low_H
    global high_H
    low_H = val
    low_H = min(high_H-1, low_H)
    cv.setTrackbarPos(low_H_name, window_detection_name, low_H)
def on_high_H_thresh_trackbar(val):
    global low_H
    global high_H
    high_H = val
    high_H = max(high_H, low_H+1)
    cv.setTrackbarPos(high_H_name, window_detection_name, high_H)
def on_low_S_thresh_trackbar(val):
    global low_S
    global high_S
    low_S = val
    low_S = min(high_S-1, low_S)
    cv.setTrackbarPos(low_S_name, window_detection_name, low_S)
def on_high_S_thresh_trackbar(val):
    global low_S
    global high_S
    high_S = val
    high_S = max(high_S, low_S+1)
    cv.setTrackbarPos(high_S_name, window_detection_name, high_S)
def on_low_V_thresh_trackbar(val):
    global low_V
    global high_V
    low_V = val
    low_V = min(high_V-1, low_V)
    cv.setTrackbarPos(low_V_name, window_detection_name, low_V)
def on_high_V_thresh_trackbar(val):
    global low_V
    global high_V
    high_V = val
    high_V = max(high_V, low_V+1)
    cv.setTrackbarPos(high_V_name, window_detection_name, high_V)

x_axis_distance = 40.0
y_axis_distance = 40.0
as_ret = x_axis_distance/x_axis_distance

pts_x = []
pts_y = []

pts_cnt = 0

def get_point(event,x,y,flags,param):
    global pts_cnt, dst
    if event == cv.EVENT_LBUTTONDOWN:
        if(pts_cnt<4):
            pts_x.append(x)
            pts_y.append(y)
            pts_cnt = pts_cnt + 1
            cv.circle(dst,(x,y),3,(0,0,255),-1)
            print('Got New Point')
        if(pts_cnt==4):
            print('Press Q to Proceed')



def calibrate():

    cap = cv.VideoCapture(1)
    
    cv_file = cv.FileStorage(os.getcwd() + '/calibration/' + 'CameraCalibration.dat', cv.FILE_STORAGE_READ)
    camera_matrix = cv_file.getNode("CamMat").mat()
    dist_matrix = cv_file.getNode("DistortionMat").mat()
    cv_file.release()

    # Perspective Calibration
    global dst, pts_x, pts_y


    print('Press "Q" to start calibration process.')
    while(True):
        ret, original = cap.read()

        # Camera calibration
        h,  w = original.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist_matrix, (w,h), 1, (w,h))
        dst = cv.undistort(original, camera_matrix, dist_matrix, newcameramtx)

        cv.imshow(window_capture_name, original)
        cv.imshow(window_calibrated_name, dst)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    
    if(Pre_Cal== True):
        print('Select 4 points..')
        cv.destroyWindow(window_capture_name)
        cv.setMouseCallback(window_calibrated_name,get_point)

        while(True):
            cv.imshow(window_calibrated_name,dst)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        wdth = int(math.sqrt(math.pow((pts_x[0]-pts_x[1]),2) + math.pow((pts_y[0]-pts_y[1]),2)))
        pts_src = np.array([[pts_x[0], pts_y[0]], [pts_x[1], pts_y[1]], [pts_x[2], pts_y[2]], [pts_x[3], pts_y[3]]])
        pts_dts = np.array([[0, 0], [wdth, 0], [wdth, int(as_ret*wdth)],[0, int(as_ret*wdth)]])

        perspect_matrix, status = cv.findHomography(pts_src, pts_dts)
        properties = np.array([wdth , as_ret, x_axis_distance, y_axis_distance])
        cv_file = cv.FileStorage(os.getcwd() + '/calibration/' + 'PerspectiveCalibration.dat', cv.FILE_STORAGE_WRITE)
        cv_file.write("properties", properties)
        cv_file.write("perspect_matrix", perspect_matrix)
        cv_file.release()

    else:

        cv_file = cv.FileStorage(os.getcwd() + '/calibration/' + 'PerspectiveCalibration.dat', cv.FILE_STORAGE_READ)
        perspect_matrix = cv_file.getNode("DistortionMat").mat()
        wdth = cv_file.getNode("width").mat()
        cv_file.release()


    perspect = cv.warpPerspective(dst, perspect_matrix, (wdth,(int(as_ret*wdth))))
    
    cv.imshow(window_perspective_name,perspect)

    cv.namedWindow(window_detection_name)
    cv.namedWindow(window_calibrated_name)

    cv.createTrackbar(low_H_name, window_detection_name , low_H, max_value_H, on_low_H_thresh_trackbar)
    cv.createTrackbar(high_H_name, window_detection_name , high_H, max_value_H, on_high_H_thresh_trackbar)
    cv.createTrackbar(low_S_name, window_detection_name , low_S, max_value, on_low_S_thresh_trackbar)
    cv.createTrackbar(high_S_name, window_detection_name , high_S, max_value, on_high_S_thresh_trackbar)
    cv.createTrackbar(low_V_name, window_detection_name , low_V, max_value, on_low_V_thresh_trackbar)
    cv.createTrackbar(high_V_name, window_detection_name , high_V, max_value, on_high_V_thresh_trackbar)

    #(480, 640, 3) (3, 3) 461
    while True:
        
        ret, img = cap.read()
        if img is None:
            break

        # Camera calibration
        h,  w = img.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist_matrix, (w,h), 1, (w,h))
        dst = cv.undistort(img, camera_matrix, dist_matrix, newcameramtx)

        # Perspective correction
        perspect = cv.warpPerspective(dst, perspect_matrix, (wdth,(int(as_ret*wdth))))

        frame_HSV = cv.cvtColor(perspect, cv.COLOR_BGR2HSV)
        frame_threshold = cv.inRange(frame_HSV, (low_H, low_S, low_V), (high_H, high_S, high_V))
        
        cv.imshow(window_capture_name, img)
        cv.imshow(window_calibrated_name, dst)
        cv.imshow(window_perspective_name, perspect)
        cv.imshow(window_detection_name, frame_threshold) 
        

        key = cv.waitKey(30)
        if key == ord('q') or key == 27:
            cv.destroyAllWindows()
            return ((low_H, low_S, low_V), (high_H, high_S, high_V))

print(calibrate())