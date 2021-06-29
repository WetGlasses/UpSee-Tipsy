import numpy as np
import cv2 as cv
import pandas as pd
import math

red_profile = ((127, 135, 82), (180, 255, 204))


Pre_Cal = False

as_ret = 40.0/40.0

pts_x = []
pts_y = []

pts_cnt = 0

def get_point(event,x,y,flags,param):
    global pts_cnt
    if event == cv.EVENT_LBUTTONDOWN:
        if(pts_cnt<4):
            pts_x.append(x)
            pts_y.append(y)
            pts_cnt = pts_cnt + 1
            cv.circle(original,(x,y),3,(0,0,0),-1)
            print('Got New Point')
        if(pts_cnt==4):
            print('Press Q to Proceed')



def image_to_table(pixel_x , pixel_y):

    x_param = [-1.06939169e-05,  1.32745150e-01, -4.01280815e-04,  8.05402574e-02, -9.94256106e-05, -1.73083381e+01]

    y_param = [ 7.28216165e-05, -8.02924456e-02,  1.80484098e-04,  1.49512382e-01, -2.35236499e-04, 1.85501976e+01]

    x,y = pixel_x, pixel_y

    val_x = x_param[0]*x*x + x_param[1]*x + x_param[2]*x*y + x_param[3]*y + x_param[4]*y*y + x_param[5]
    val_y = y_param[0]*x*x + y_param[1]*x + y_param[2]*x*y + y_param[3]*y + y_param[4]*y*y + y_param[5]

    return val_x, val_y 

# Filter
open_windw = np.ones((5,5),np.uint8)
close_windw = np.ones((5,5),np.uint8)

cap = cv.VideoCapture(1)
cv.namedWindow('Original feed')
cv.namedWindow('After Detection')

ret, original = cap.read()

if(Pre_Cal== True):
    print('Select 4 points..')
    cv.imshow('Original feed',original)
    cv.setMouseCallback('Original feed',get_point)

    while(True):
        cv.imshow('Original feed',original)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    Points = pd.DataFrame({'X':pts_x, 'Y': pts_y})
    Points.to_csv('Perspective_Points.csv')

else:
    Points = pd.read_csv('Perspective_Points.csv')
    pts_x = list(Points.X)
    pts_y = list(Points.Y)

wdth = int(math.sqrt(math.pow((pts_x[0]-pts_x[1]),2) + math.pow((pts_y[0]-pts_y[1]),2)))
pts_src = np.array([[pts_x[0], pts_y[0]], [pts_x[1], pts_y[1]], [pts_x[2], pts_y[2]], [pts_x[3], pts_y[3]]])
pts_dts = np.array([[20, 20], [wdth, 20], [wdth, int(as_ret*wdth)],[20, int(as_ret*wdth)]])

h, status = cv.findHomography(pts_src, pts_dts)
perspect = cv.warpPerspective(original, h, ((wdth+50),(int(as_ret*wdth)+50)))

cv.imshow('Perspective',perspect)

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
    red_obj = cv.inRange(frame_HSV, red_profile[0], red_profile[1])

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
            
            act_x, act_y = image_to_table(red_Cx, red_Cy)

            print(act_x, act_y)

    else:
        cv.putText (original, 'Cannot find Red object', (60,120), 1,1, (0,255,255))


    cv.imshow('Original feed', original)
    cv.imshow('After Detection', red_obj)

    key = cv.waitKey(30)
    if key == ord('q') or key == 27:
        cv.destroyAllWindows()
        quit()