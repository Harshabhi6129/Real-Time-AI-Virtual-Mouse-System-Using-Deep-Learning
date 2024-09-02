import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
from HandTrackingModule import handDetector
import time

cap = cv2.VideoCapture(0)
detector = handDetector(maxHands=1)

wScr, hScr = pyautogui.size()
smoothening = 7
plocX, plocY = 0, 0
clocX, clocY = 0, 0

mouse_position = (0, 0)
mouse_down = False
mouse_button = None
frameR = 100
wCam, hCam = 640, 480

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)

        # 4. Only index Finger :Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            pyautogui.moveTo(clocX, clocY)
            plocX, plocY = clocX, clocY

            '''elif fingers[3] == 1:
            pyautogui.scroll(10)'''

        elif fingers[4] == 1:
            pyautogui.scroll(-100)

        elif fingers[1] == 1 and fingers[2] == 1:
            length, _, _ = detector.findDistance(8, 12, img)
            if length < 40:
                if not mouse_down:
                    pyautogui.mouseDown(button='left')
                    mouse_down = True
                    mouse_button = 'left'
        elif fingers[3] == 1:
            if mouse_down:
                pyautogui.mouseUp(button='left')
                mouse_down = False
                mouse_button = None

        elif all(fingers):
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(1)
            time.sleep(0.1)
            pyautogui.keyUp('ctrl')

        elif fingers[0] == 1 and fingers[4] == 1:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(-1)
            time.sleep(0.1)
            pyautogui.keyUp('ctrl')

        # Check if thumb and index fingers are together for drag and drop
        elif fingers[0] == 1 and fingers[1] == 1:
            # Assuming you have the coordinates of the start and end positions for drag and drop
            start_position = (100, 100)  # Starting position (x, y)
            end_position = (200, 200)    # Ending position (x, y)

            # Check if thumb and index fingers are close together
            length_thumb_index, _, _ = detector.findDistance(4, 8, img, draw=False)
            if length_thumb_index < 30:
                # Perform drag and drop action
                if not mouse_down:
                    pyautogui.mouseDown(button='right')
                    mouse_down = True
                    mouse_button = 'right'

                # Move Mouse
                pyautogui.moveTo(clocX, clocY)
                plocX, plocY = clocX, clocY

                # Update the position continuously for smooth drag
                mouse_position = (clocX, clocY)

            else:
                # If fingers are not close, release the mouse button
                if mouse_down:
                    pyautogui.mouseUp(button=mouse_button)
                    mouse_down = False
                    mouse_button = None

    else:
        if mouse_down:
            pyautogui.mouseUp(button=mouse_button)
            mouse_down = False
            mouse_button = None

    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
