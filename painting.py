import cv2
import numpy as np
frameWidth=640
frameHeight=480
webcam = cv2.VideoCapture(0)
webcam.set(3, frameWidth)
webcam.set(4, frameHeight)
webcam.set(10,200)#brightness

#colors hsv values
myColors = [[18,78,52,154,255,255]#yellow
            ,[40,89,82,104,255,255]#green
            ,[101,97,53,179,252,255]]#pink
def findColor(img, myColors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        getContours(mask)
        #cv2.imshow(str(color[0]),mask)
def getContours(img):
    contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)#it retrieves the outer contours
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)

        if area>500:#avoiding noise
            cv2.drawContours(imgResult, cnt, -1, (255,0,0),3)
            #calculate curve length, curve length will help us approximate the cornes of our shape
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)

            #x and y of bounding
            x, y, w, h = cv2.boundingRect(approx)
while True:
    success, img = webcam.read()
    imgResult = img.copy()
    findColor(img, myColors)
    cv2.imshow('Video',imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
