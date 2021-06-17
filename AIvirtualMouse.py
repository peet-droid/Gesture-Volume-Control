import cv2
import numpy as np
import HandTrack30Fps as htm

import time
import autopy

hcam = 480
wcam = 640

cap = cv2.VideoCapture(0)

cap.set(3,wcam)
cap.set(4,hcam)

detector = htm.handDetector(MaxHands = 1)

wscr, hscr = autopy.screen.size()

while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmlist,bbox = detector.findPositon(img)
        if len(lmlist) != 0:
                fingers = detector.fingersUp()
                x1,y1 = lmlist[8][1:]
                x2,y2 = lmlist[12][1:]
                
                if fingers[1] == 1 and fingers[2] == 0:
                        x3 = np.interp(x1, (0,wcam),(0,wscr))
                        y3 = np.interp(y1, (0,hcam),(0,hscr))
                        autopy.mouse.move(x3,y3)
                if fingers[1] == 1 and fingers[2] == 1:
                        # 9. Find distance between fingers
                        length, img, lineInfo = detector.findDistance(8, 12, img)
                        print(length)
                        # 10. Click mouse if distance short
                        if length < 40:
                                cv2.circle(img, (lineInfo[4], lineInfo[5]),
                                15, (0, 255, 0), cv2.FILLED)
                                autopy.mouse.click()
        
        cv2.imshow('Image',img)
        cv2.waitKey(1)