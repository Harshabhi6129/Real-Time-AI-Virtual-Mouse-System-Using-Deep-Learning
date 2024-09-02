import cv2
import numpy as np 
import time
from keys import *
from handTracker import *
from pynput.keyboard import Controller
import pyperclip

def getMousPos(event, x, y, flags, param):
    global clickedX, clickedY
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONUP:
        clickedX, clickedY = x, y
    if event == cv2.EVENT_MOUSEMOVE:
        mouseX, mouseY = x, y

def calculateIntDistance(pt1, pt2):
    return int(((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** 0.5)

# Creating keys
w, h = 80, 60
startX, startY = 40, 400
start1X, start1Y = 40 , 330
keys = []
numbers = list("1234567890")
letters = list("QWERTYUIOPASDFGHJKLZXCVBNM")
for i,l in enumerate(numbers):
    keys.append(Key(start1X + i * w + i * 5, start1Y, w, h, l))
for i, l in enumerate(letters):
    if i < 10:
        keys.append(Key(startX + i * w + i * 5, startY, w, h, l))
    elif i < 19:
        keys.append(Key(startX + (i - 10) * w + i * 5, startY + h + 5, w, h, l))  
    else:
        keys.append(Key(startX + (i - 19) * w + i * 5, startY + 2 * h + 10, w, h, l)) 

keys.append(Key(startX + 25, startY + 3 * h + 15, 5 * w, h, "Space"))
keys.append(Key(startX + 8 * w + 50, startY + 2 * h + 10, w, h, "clr"))
keys.append(Key(startX + 5 * w + 30, startY + 3 * h + 15, 5 * w, h, "<--"))
#keys.append(Key(25,170,900,200, ""))



showKey = Key(300, 5, 80, 50, 'Show')
exitKey = Key(300, 65, 80, 50, 'Exit')
copyKey = Key(780, 5, 80, 50, 'Copy')
nextLineKey = Key(780, 65, 80, 50, 'Next Line')  # New Next Line button

superbuttons=[showKey,exitKey,copyKey,nextLineKey]

# Adjusted height for the text box to accommodate multiple lines
textBoxHeight = 120
textBox = Key(startX, startY - textBoxHeight - 5, 10 * w + 9 * 5, textBoxHeight, '')

delayo = 1.0  # Adjust this value as needed

# Time of the last Next Line action
last_time = time.time()


cap = cv2.VideoCapture(0)
ptime = 0

# Initiating the hand tracker
tracker = HandTracker(detectionCon=1)

# Getting frame's height and width
frameHeight, frameWidth, _ = cap.read()[1].shape
showKey.x = int(frameWidth * 1.5) - 85
exitKey.x = int(frameWidth * 1.5) - 85

clickedX, clickedY = 0, 0
mouseX, mouseY = 0, 0

show = False
cv2.namedWindow('video')
counter = 0
previousClick = 0

keyboard = Controller()
while True:
    if counter > 0:
        counter -= 1
        
    signTipX, signTipY = 0, 0
    thumbTipX, thumbTipY = 0, 0

    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame, (int(frameWidth * 1.5), int(frameHeight * 1.5)))
    frame = cv2.flip(frame, 1)

    # Find hands
    frame = tracker.findHands(frame)
    lmList = tracker.getPostion(frame, draw=False)
    if lmList:
        signTipX, signTipY = lmList[8][1], lmList[8][2]
        thumbTipX, thumbTipY = lmList[4][1], lmList[4][2]
        if calculateIntDistance((signTipX, signTipY), (thumbTipX, thumbTipY)) < 50:
            centerX = int((signTipX + thumbTipX) / 2)
            centerY = int((signTipY + thumbTipY) / 2)
            cv2.line(frame, (signTipX, signTipY), (thumbTipX, thumbTipY), (0, 255, 0), 2)
            cv2.circle(frame, (centerX, centerY), 5, (0, 255, 0), cv2.FILLED)

    ctime = time.time()
    fps = int(1 / (ctime - ptime))

    cv2.putText(frame, str(fps) + " FPS", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    showKey.drawKey(frame, (255, 255, 255), (0, 0, 0), 0.1, fontScale=0.5)
    exitKey.drawKey(frame, (255, 255, 255), (0, 0, 0), 0.1, fontScale=0.5)
    copyKey.drawKey(frame, (255, 255, 255), (0, 0, 0), 0.1, fontScale=0.5)
    nextLineKey.drawKey(frame, (255, 255, 255), (0, 0, 0), 0.1, fontScale=0.5)

    cv2.setMouseCallback('video', getMousPos)

    if showKey.isOver(mouseX, mouseY):
        showKey.drawKey(frame, (0, 255, 0), (0, 0, 0), 0.1, fontScale=0.5)  # Change color when hovered
    if exitKey.isOver(mouseX, mouseY):
        exitKey.drawKey(frame, (0, 255, 0), (0, 0, 0), 0.1, fontScale=0.5)  # Change color when hovered
    if copyKey.isOver(mouseX, mouseY):
        copyKey.drawKey(frame, (0, 255, 0), (0, 0, 0), 0.1, fontScale=0.5)  # Change color when hovered
    if nextLineKey.isOver(mouseX, mouseY):
        nextLineKey.drawKey(frame, (0, 255, 0), (0, 0, 0), 0.1, fontScale=0.5)  # Change color when hovered


    if showKey.isOver(clickedX, clickedY):
        show = not show
        showKey.text = "Hide" if show else "Show"
        clickedX, clickedY = 0, 0

    if exitKey.isOver(clickedX, clickedY):
        break

    if copyKey.isOver(clickedX, clickedY):
        pyperclip.copy(textBox.text)
        print("Text copied to clipboard")
        clickedX, clickedY = 0, 0

    if nextLineKey.isOver(clickedX, clickedY):
        textBox.text += "\n"  # Add new line to the text box
        clickedX, clickedY = 0, 0

    alpha = 0.5
    if show:
        #textBox.drawKey(frame, (255, 255, 255), (0, 0, 0), 0.3)
        # above to not to show centered text
        
        #cv2.rectangle(frame,(25,170),(925,375),(128,128,128),2)
        # Split text into lines based on newline characters
        lines = textBox.text.split('\n')
        
        # Render each line of text on the frame
        line_y = textBox.y + textBox.h - 190
        for line in lines:
            cv2.putText(frame, line, (textBox.x + 10, line_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            line_y += 30

        for k in keys:
            if k.isOver(mouseX, mouseY) or k.isOver(signTipX, signTipY):
                alpha = 0.1
                if k.isOver(clickedX, clickedY):
                    if k.text == '<--':
                        textBox.text = textBox.text[:-1]
                    elif k.text == 'clr':
                        textBox.text = ''
                    elif len(textBox.text) < 999:
                        if k.text == 'Space':
                            textBox.text += " "
                        else:
                            textBox.text += k.text
                    
                if k.isOver(thumbTipX, thumbTipY):
                    clickTime = time.time()
                    if clickTime - previousClick > 0.4:
                        if k.text == '<--':
                            textBox.text = textBox.text[:-1]
                        elif k.text == 'clr':
                            textBox.text = ''
                        elif len(textBox.text) < 30:
                            if k.text == 'Space':
                                textBox.text += " "
                            else:
                                textBox.text += k.text
                                keyboard.press(k.text)
                        previousClick = clickTime
            k.drawKey(frame, (255, 255, 255), (0, 0, 0), alpha=alpha)
            alpha = 0.5
        
        if exitKey.isOver(signTipX, signTipY):
            break

        for control_key in superbuttons:  # Only check the last four keys (control keys)
            if control_key.isOver(signTipX, signTipY):
                control_key.drawKey(frame, (0, 255, 0))  # Highlight control key in green
                if control_key.text == 'Copy':
                    current_time = time.time()
                    if current_time - last_time >= delayo:
                        pyperclip.copy(textBox.text)
                        print("Text copied to clipboard")
                        last_time = current_time
                if control_key.text == 'Next Line':
                    current_time = time.time()
                    if current_time - last_time >= delayo:
                        textBox.text += '\n'
                        last_time = current_time
                if control_key.text == 'Show':
                    current_time = time.time()
                    if current_time - last_time >= delayo:
                        show = not show
                        showKey.text = "Hide" if show else "Show"
                        signTipX, signTipY = 0, 0
                        last_time = current_time
                    
                if control_key.text == 'Exit':
                    print("Text copied to clipboard")
                    break
                    '''current_time = time.time()
                    if current_time - last_time >= delayo:
                        break  # Exit the loop and terminate the program
                        
                        last_time = current_time'''
                    

    clickedX, clickedY = 0, 0
    ptime = ctime
    cv2.imshow('video', frame)

    # Check for key press to exit
    pressedKey = cv2.waitKey(1)
    if pressedKey == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

