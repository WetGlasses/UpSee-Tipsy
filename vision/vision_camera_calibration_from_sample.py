import numpy as np
import cv2 as cv
import glob
import os


####################    Load images   ######################

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

for x in all_image:

    original = cv.imread(x)
    cv.imshow('Input Image', original)
    gray = cv.cvtColor(original, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, ( calibration_width, calibration_height), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        image_added += 1
        print('Got Pattern. Total:' , image_added)
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        marked = np.copy(original)
        cv.drawChessboardCorners(marked, (calibration_width,calibration_height), corners2, ret)
        cv.imshow('After Detection', marked)
        key = cv.waitKey(500)
        cv.imwrite(x[:-4] + '_tempo_marked.jpg', marked)
        objpoints.append(objp)
        imgpoints.append(corners)
        print('image added')
        
        
############# Calibration ##########################
input('Want to Calibrate?')
print('Calibrating the Camera... It will take time')

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print('Successfully Calibrated..')
print('Saving matrices..')
print(ret)
cv_file = cv.FileStorage(os.getcwd() + '/calibration/' + 'CameraCalibration.dat', cv.FILE_STORAGE_WRITE)
cv_file.write("CamMat", mtx)
cv_file.write("DistortionMat", dist)
cv_file.release()

####################### Testing Calibration ########################

input('Want to Test?')
cv_file = cv.FileStorage(os.getcwd() + '/calibration/' + 'CameraCalibration.dat', cv.FILE_STORAGE_READ)

camera_matrix = cv_file.getNode("CamMat").mat()
dist_matrix = cv_file.getNode("DistortionMat").mat()
cv_file.release()

print(camera_matrix.shape, dist_matrix.shape)

all_image = glob.glob(os.getcwd() + '/calibration/*_raw.jpg')

print(len(all_image))

for fname in all_image:

    img = cv.imread(fname)

    h,  w = img.shape[:2]
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(camera_matrix, dist_matrix, (w,h), 1, (w,h))
    
    dst = cv.undistort(img, camera_matrix, dist_matrix, newcameramtx)
    cv.imshow('Raw', img)
    cv.imshow('Undistorted', dst)
    cv.imwrite(fname[:-4] + '_undistorted.jpg', dst)

    cv.waitKey(500)

cv.destroyAllWindows()

#'''