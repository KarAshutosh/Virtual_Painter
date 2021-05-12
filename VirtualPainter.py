import cv2
import numpy as np

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

hMin = 32
hMax = 66
sMin = 49
sMax = 196
vMin = 166
vMax = 255

drawSpace = np.zeros((480,780,3), np.uint8)
drawSpace[:] = 255, 0, 255


def drawOnCanvas(myPoints):
    for point in myPoints:
        cv2.circle(drawSpace, (point[0], point[1]), 10, (255, 255, 0), cv2.FILLED)

def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 250:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x + w // 2, y

myPoints = []

def findColor(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    newPoints = []
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])
    mask = cv2.inRange(imgHSV, lower, upper)
    x, y = getContours(mask)
    cv2.circle(drawSpace, (x, y), 15, (255, 255, 0), cv2.FILLED)
    if x != 0 and y != 0:
        newPoints.append([x, y])
    return newPoints


while True:
    success, imgf = cap.read()
    img = cv2.flip(imgf, 1)

    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])
    mask = cv2.inRange(imgHSV, lower, upper)
    cv2.imshow("mask", mask)

    drawSpace[30:90, 650:770] = 255, 0, 0               # for exit
    drawSpace[120:180, 650:770] = 255, 0, 0             # for clear
    drawSpace[210:270, 650:770] = 255, 0, 0             # for drawing

    key = cv2.waitKey(1)

    newPoints = []

    cv2.imshow("Virtual Painter", drawSpace)

    if key == 101:  # ascii for letter 'e'
        drawSpace[30:90, 650:770] = 0, 255, 0
        cv2.imshow("Virtual Painter", drawSpace)
        cv2.waitKey(250)
        break

    elif key == 100:  # ascii for letter 'd'
        newPoints = findColor(img)
        drawSpace[210:270, 650:770] = 0, 255, 0
        cv2.imshow("Virtual Painter", drawSpace)
        cv2.waitKey(1)

    elif key == 99:  # ascii for letter 'c'
        drawSpace[:] = 255, 0, 255
        drawSpace[30:90, 650:770] = 255, 0, 0               # for exit
        drawSpace[210:270, 650:770] = 255, 0, 0             # for drawing
        while key == 99:
            key = cv2.waitKey(10)
            drawSpace[120:180, 650:770] = 0, 255, 0
            cv2.imshow("Virtual Painter", drawSpace)
            cv2.waitKey(250)








