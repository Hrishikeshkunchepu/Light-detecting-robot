import numpy as np
import cv2
import math
import time
import RPi.GPIO as GPIO


#servo declarations
servo = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo,GPIO.OUT)
p=GPIO.PWM(servo,50)# 50hz frequency
p.start(2.5)



#usb camera declarations
cap = cv2.VideoCapture(0)
store = [320,240]
c = 0
slope = 0
#control pins for the motors
r = 8
l = 16#control for right motor
m = 13
n = 15#control for left motor
GPIO.setup(r, GPIO.OUT,initial=0)
GPIO.setup(l, GPIO.OUT,initial=0)

while(True):
    #capture frame by frame
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dst = cv2.GaussianBlur(gray,(5,5),cv2.BORDER_DEFAULT)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(dst)
    
    cv2.circle(frame, maxLoc, 20, (255, 0, 0), -1)
    
    print(maxLoc)
    
    for x in maxLoc:
        store.append(x)
    
    print(store)
    x1, x2, y1, y2 = store[0], store[2], store[1], store[3]
    cv2.line(frame, (x1, y1), (x2, y2), (0,255,0), 10)
         
        
    
    a = math.sqrt((math.pow((store[3]-store[1]),2)+math.pow((store[2]-store[0]),2)))    
    print("distance=", a)
    if store[2] == 240:
        print("slope = 0")
    else:
        slope = math.atan((store[3]-320)/(store[2]-240))
    angle_to_mid_deg = int(slope * 180.0 / math.pi)  # angle (in degrees) to center vertical line
    #steering_angle = angle_to_mid_deg + 90  # this is the steering angle needed 
    print("slope=",angle_to_mid_deg )
    #move = drive(angle_to_mid_deg, store[3],store[2])
    i = store[3]
    j = store[2]
    #angle_to_mid_deg = k
    if (i < 240) and (j <320):
        p.ChangeDutyCycle(8.5)
        GPIO.output(l, GPIO.HIGH)
        GPIO.output(r, GPIO.LOW)
        GPIO.output(l, GPIO.LOW)
        GPIO.output(l, GPIO.HIGH)
        print("1quadrant")
    
    elif (i > 240 and j <320):
        p.ChangeDutyCycle(6.0)
        GPIO.output(l, GPIO.LOW)
        GPIO.output(r, GPIO.HIGH)
        GPIO.output(l, GPIO.LOW)
        GPIO.output(l, GPIO.HIGH)
        print("2nd quadrant")
    
    elif (i > 240 and j > 320):
        p.ChangeDutyCycle(9.5)
        GPIO.output(l, GPIO.HIGH)
        GPIO.output(r, GPIO.LOW)
        GPIO.output(l, GPIO.HIGH)
        GPIO.output(l, GPIO.LOW)
        print("3rd quadrant")
    
    
    else:
        p.ChangeDutyCycle(9.5)
        GPIO.output(l, GPIO.LOW)
        GPIO.output(r, GPIO.HIGH)
        GPIO.output(l, GPIO.LOW)
        GPIO.output(l, GPIO.HIGH)
        
        print("4th quadrant" )
        
    
    
    
    
    del store[2]
    del store[2]
    print(store)
    
    
       
        
        
    
    
    
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup() 