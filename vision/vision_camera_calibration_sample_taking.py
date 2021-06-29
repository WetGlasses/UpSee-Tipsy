import numpy as np
import cv2 as cv
import glob
import os


calibration_width = 9
calibration_height = 6
calibration_size = 2 # cm

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((calibration_height * calibration_width,3), np.float32)
objp[:,:2] = np.mgrid[0:calibration_width,0:calibration_height].T.reshape(-1,2)

objp = objp * calibration_size
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

cap = cv.VideoCapture(1)

cv.namedWindow('Input Image')
cv.namedWindow('After Detection')

all_image = glob.glob(os.getcwd() + '/calibration/*_raw.jpg')
image_added = 0

while(True):

    ret, original = cap.read()
    cv.imshow('Input Image', original)
    gray = cv.cvtColor(original, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, ( calibration_width, calibration_height), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        print('Got Pattern.')
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        marked = np.copy(original)
        cv.drawChessboardCorners(marked, (calibration_width,calibration_height), corners2, ret)
        cv.imshow('After Detection', marked)
        print('Current total image:', image_added , 'Press "Q" to use the current frame and "C" to start calibrating..')
        key = cv.waitKey(30)
        if key == ord('q'):

            print('Ho vai')
            cv.imwrite(os.getcwd() + '/calibration/' + str(image_added) + '_raw.jpg', original)
            cv.imwrite(os.getcwd() + '/calibration/' + str(image_added) + '_marked.jpg', marked)

            objpoints.append(objp)
            imgpoints.append(corners)
            print('image added')
            image_added += 1
        
        elif key == ord('c'):
            break
    key = cv.waitKey(30)

