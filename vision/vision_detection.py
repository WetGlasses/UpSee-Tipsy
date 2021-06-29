import numpy as np
import cv2 as cv
import os

# It is good to calibrate at each light condition before using
profile = ((131, 95, 143), (180, 198, 255))

# Filter
open_windw = np.ones((20,20),np.uint8)
close_windw = np.ones((10,10),np.uint8)

# Points for Perspective correction
cv_file = cv.FileStorage(os.getcwd() + '/calibration/' + 'PerspectiveCalibration.dat', cv.FILE_STORAGE_READ)
perspect_matrix = cv_file.getNode("perspect_matrix").mat()
properties = cv_file.getNode("properties").mat()
# image Width, aspect ratio, x_axis_distance, y_axis_distance
cv_file.release()
width = int(properties[0,0])
as_ret = properties[1,0]
x_axis_distance = properties[2,0]
y_axis_distance = properties[3,0]

cap = cv.VideoCapture(1)

feed_window = 'Original feed'
distortion_window = 'Distortion filter'
perspective_window = 'Perspective filter'
color_window = 'Detection'
detection_window = 'Location'

cv.namedWindow(feed_window)
cv.namedWindow(distortion_window)
cv.namedWindow(perspective_window)
cv.namedWindow(color_window)
cv.namedWindow(detection_window)

cv.moveWindow(feed_window, 0,0)
cv.moveWindow(distortion_window, 700, 0)
cv.moveWindow(perspective_window, 1400, 0)
cv.moveWindow(color_window, 0,600)
cv.moveWindow(detection_window, 600,600)


# Camera Calibration Matrix
cv_file = cv.FileStorage(os.getcwd() + '/calibration/' + 'CameraCalibration.dat', cv.FILE_STORAGE_READ)
camera_matrix = cv_file.getNode("CamMat").mat()
dist_matrix = cv_file.getNode("DistortionMat").mat()
cv_file.release()

while(True):

    ret, original = cap.read()
    if original is None:
        break

    h,  w = original.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist_matrix, (w,h), 1, (w,h))
    undistorted = cv.undistort(original, camera_matrix, dist_matrix, newcameramtx)
    # Perspective change
    perspective = cv.warpPerspective(undistorted, perspect_matrix, (width,(int(as_ret*width))))


    # Smoothen
    frame = cv.medianBlur(perspective, 9)

    # Open and close grains
    frame = cv.morphologyEx(frame, cv.MORPH_OPEN , open_windw)
    frame = cv.morphologyEx(frame, cv.MORPH_CLOSE , close_windw)


    # Covert to HSV
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # Thresholding
    detected_obj = cv.inRange(frame_HSV, profile[0], profile[1])
    #Masking
    located_object = cv.bitwise_and(perspective, perspective, mask= detected_obj)

    # Find contours
    obj_cnt, h = cv.findContours(detected_obj, cv.RETR_TREE , cv.CHAIN_APPROX_SIMPLE )
    if(len(obj_cnt)>0):
        obj_areaX=0
        obj_pos=0
        for x in range (0, len(obj_cnt)):
            area = cv.contourArea(obj_cnt[x])
            if(area>obj_areaX):
                obj_areaX=area
                obj_pos=x

        cv.drawContours(located_object, obj_cnt, obj_pos, (255,255,0),2)

        M=cv.moments(obj_cnt[obj_pos])

        if(M['m00'] != 0):
            Cx= int(M['m10']/M['m00'])
            Cy= int(M['m01']/M['m00'])

            CoOr = str(Cx)+' , '+str(Cy)
            cv.putText (detected_obj, CoOr, (Cx, Cy),1,2, (255,255,0), 2)

            act_x = (x_axis_distance / width) * Cx 
            act_y = (y_axis_distance / width) * Cy 

            cv.putText (located_object, f"{act_x:.2f}", (0, 15),1,1, (255,255,0), 1)
            cv.putText (located_object, f"{act_y:.2f}", (0, 30),1,1, (0,255,255), 1)

    else:
        cv.putText (located_object, 'Cannot find object', (60,120), 1,1, (255,255,0))

    cv.imshow(feed_window, original)
    cv.imshow(distortion_window, undistorted)
    cv.imshow(perspective_window, perspective)
    cv.imshow(color_window, detected_obj)
    cv.imshow(detection_window, located_object)


    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        cv.destroyAllWindows()
        quit()