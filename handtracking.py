import time

import cv2

import HandTrack30Fps as hmt

import numpy as np

import math

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

ptime = 0
ctime = 0
cap = cv2.VideoCapture(0)
detector = hmt.handDetector(detecCon=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMasterVolumeLevel()
# volume.GetMute()
volRange = volume.GetVolumeRange()
volume.SetMasterVolumeLevel(0, None)

minVol = volRange[0]
maxVol = volRange[1]

while True:

    success, img = cap.read()

    img = detector.findHands(img, draw=False)

    lmlist = detector.findPositon(img, draw=False)

    if len(lmlist) > 0:
        x1, x2 = lmlist[4][1], lmlist[8][1]
        y1, y2 = lmlist[4][2], lmlist[8][2]

        cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0))

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        # print(length)

        vol = np.interp(length, [50, 250], [minVol, maxVol])

        print(vol)

        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

    ctime = time.time()
    fps = 1 / (ctime - ptime)

    ptime = ctime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
