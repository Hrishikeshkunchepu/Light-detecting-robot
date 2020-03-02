import numpy as np
import cv2
cap = cv2.VideoCapture(0)
while(True):
    #capture frame by frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    print(maxLoc)
    cv2.circle(frame, maxLoc, 5, (255, 0, 0), 2)
    cv2.imshow('not approximated',frame)
    
    dst = cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(dst)
    
    cv2.circle(frame, maxLoc, 20, (255, 0, 0), -1)
    
    
    
    
    
    
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
