import cv2
import mediapipe as mp

import time

class handDetector():
    def __init__(self, mode = False, MaxHands = 2, detecCon = 0.5, trackCon = 0.5):
        self.mode = mode
        self.maxHands = MaxHands
        self.detectionCon = detecCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands

        self.hands = self.mpHands.Hands(self.mode,
                                        self.maxHands,self.detectionCon
                                        ,self.trackCon)

        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if (self.results.multi_hand_landmarks):
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPositon(self,img, handNo=0,draw=True):

        lmList = []

        if self.results.multi_hand_landmarks:
            myHand  = self.results.multi_hand_landmarks[handNo]



            for id, lm in enumerate(myHand.landmark):
                h,w,c = img.shape

                cx,cy = int(lm.x*w),int(lm.y*h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.putText(img, str(id), (cx+1,cy) , cv2.FONT_HERSHEY_SIMPLEX, 0.5 , (255,0,255),2)

        return lmList


def main():
    ptime = 0
    ctime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()

    while True:

        success, img = cap.read()

        img = detector.findHands(img)

        lmlist = detector.findPositon(img)

        if len(lmlist) > 0:
            print(lmlist)

        ctime = time.time()
        fps = 1/(ctime-ptime)

        ptime = ctime

        cv2.putText(img, str(int(fps)), (10,70) , cv2.FONT_HERSHEY_SIMPLEX, 3 , (255,0,255),3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == '__main__':
    main()
