import numpy as np
import cv2 as cv

# It is good to calibrate at each light condition before using
profile = ((130, 91, 149), (180, 238, 255))

# Filter
open_windw = np.ones((5,5),np.uint8)
close_windw = np.ones((5,5),np.uint8)

cap = cv.VideoCapture(1)
cv.namedWindow('Original feed')
cv.namedWindow('After distortion filter')
cv.namedWindow('After Detection')

while(True):

    ret, original = cap.read()
    if original is None:
        break

    # Smoothen
    frame = cv.medianBlur(original, 9)

    # Open and close grains
    frame = cv.morphologyEx(frame, cv.MORPH_OPEN , open_windw)
    frame = cv.morphologyEx(frame, cv.MORPH_CLOSE , close_windw)


    # Covert to HSV
    frame_HSV = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    blue_obj = cv.inRange(frame_HSV, blue_profile[0], blue_profile[1])
    red_obj = cv.inRange(frame_HSV, red_profile[0], red_profile[1])

    # Find contours of blue
    blue_cnt, h = cv.findContours(blue_obj, cv.RETR_TREE , cv.CHAIN_APPROX_SIMPLE )
    if(len(blue_cnt)>0):
        blue_areaX=0
        blue_pos=0
        for x in range (0, len(blue_cnt)):
            area = cv.contourArea(blue_cnt[x])
            if(area>blue_areaX):
                blue_areaX=area
                blue_pos=x

        cv.drawContours(original, blue_cnt, blue_pos, (255,255,0),2)

        M=cv.moments(blue_cnt[blue_pos])

        if(M['m00'] != 0):
            blue_Cx= int(M['m10']/M['m00'])
            blue_Cy= int(M['m01']/M['m00'])
            cv.circle(original, (blue_Cx, blue_Cy), 5, (255,255,0), 2)

            CoOr = str(blue_Cx)+' , '+str(blue_Cy)
            cv.putText (original, CoOr, (blue_Cx,blue_Cy),1,2, (255,255,0), 2)

    else:
        cv.putText (original, 'Cannot find Blue object', (60,120), 1,1, (255,255,0))
    

    # Find contours of red
    red_cnt, h = cv.findContours(red_obj, cv.RETR_TREE , cv.CHAIN_APPROX_SIMPLE )
    if(len(red_cnt)>0):
        red_areaX=0
        red_pos=0
        for x in range (0, len(red_cnt)):
            area = cv.contourArea(red_cnt[x])
            if(area>red_areaX):
                red_areaX=area
                red_pos=x

    
        cv.drawContours(original, red_cnt, red_pos, (0,255,255),2)

        M=cv.moments(red_cnt[red_pos])
        
        if(M['m00'] != 0):
            red_Cx= int(M['m10']/M['m00'])
            red_Cy= int(M['m01']/M['m00'])
            cv.circle(original, (red_Cx, red_Cy), 5, (255,255,0), 2)

            CoOr = str(red_Cx)+' , '+str(red_Cy)
            cv.putText (original, CoOr, (red_Cx,red_Cy),1,2, (0,255,255), 2)
            print(CoOr)

    else:
        cv.putText (original, 'Cannot find Red object', (60,120), 1,1, (0,255,255))


    cv.imshow('Original feed', original)
    cv.imshow('After Detection: Blue', blue_obj)
    cv.imshow('After Detection: Red', red_obj)

    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        cv.destroyAllWindows()
        quit()