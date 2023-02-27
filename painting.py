import cv2
import numpy as np
frameWidth=640
frameHeight=480
webcam = cv2.VideoCapture(0)
webcam.set(3, frameWidth)
webcam.set(4, frameHeight)
webcam.set(10,200)#brightness

#colors hsv values
#write your own values by detecting from taking_color.py
myColors = [[18,78,52,154,255,255]#yellow
            ,[40,89,82,104,255,255]#green
            ,[101,97,53,179,252,255]]#pink

myColorValues = [[0,255,255],[0,255,0],[142,0,255]]   ##BGR
myPoints=[] #[x,y,colorId]
def findColor(img, myColors,myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count =0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),10
                   ,myColorValues[count],cv2.FILLED)
        if x != 0 and y != 0:
            newPoints.append([x, y, count])

        count+=1
        #cv2.imshow(str(color[0]),mask)

    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)#it retrieves the outer contours
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:#avoiding noise
            cv2.drawContours(imgResult, cnt, -1, (255,0,0),3)
            #calculate curve length, curve length will help us approximate the cornes of our shape
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
           #x and y of bounding
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y
def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10
                   , myColorValues[point[2]], cv2.FILLED)
while True:
    success, img = webcam.read()
    imgResult = img.copy()
    newPoints=findColor(img, myColors,myColorValues)
    if len(newPoints)!=0:
        #since we are getting a list so we cannot put a list inside a list we need all do points
        for newP in newPoints:
            myPoints.append(newP)

    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)
    cv2.imshow('Video',imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
