import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
from HandTrackingModule import handDetector
import time
import keyboard

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
    # 5. convert coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # Update interpolation for vertical movement
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # Move Mouse
            pyautogui.moveTo(clocX, clocY)
            plocX, plocY = clocX, clocY

        elif fingers[3] == 1:
            pyautogui.scroll(50)
        
        elif fingers[4] == 1:
            pyautogui.scroll(-50)


        elif fingers[1] == 1 and fingers[2] == 1:
            length, _, _ = detector.findDistance(8, 12, img)
            if length < 40:
                pyautogui.click(button='left')
            elif length > 40:  # Ensure thumb is not up for right-click
                pyautogui.click(button='right')
        
        elif all(fingers):
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(1)
            time.sleep(0.1)
            pyautogui.keyUp('ctrl')

# Check if all fingers are closed for zoom out
        elif fingers[0] == 1 and fingers[4] == 1:
            pyautogui.keyDown('ctrl')
            pyautogui.scroll(-0.5)
            time.sleep(0.1)
            pyautogui.keyUp('ctrl')

        '''elif fingers[0] == 1:
            # Capture a screenshot
            pyautogui.screenshot()

            # Save the screenshot (you can customize the filename and location)
            screenshot.save("screenshot.png")  '''  
                    

    else:
        if mouse_down:
            pyautogui.mouseUp()
            mouse_down = False

    cv2.imshow("Virtual Mouse", img)
    if cv2.waitKey(1) == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()