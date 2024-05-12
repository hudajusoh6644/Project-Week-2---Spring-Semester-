#project week 2 - group 14
#line following code
#this code only follow black line using this speed the track can be completed in 86s 
import RPi.GPIO as GPIO
import time
import cv2
import numpy as np


 

# GPIO pin setup

basespeed = 40

KP=0.21#to make the curves easier and make it go straight when the value is smaller (0.22 works)

KD=0.0176#to oscillat eback on track >>value means more oscillation, << value means less oscillation (0.0195 kinda works)

last_error=0

 

# setup GPIO pins

GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

en = 22

enB = 18

GPIO.setup(15, GPIO.OUT)

GPIO.setup(13, GPIO.OUT)

GPIO.setup(11, GPIO.OUT)

GPIO.setup(7, GPIO.OUT)

GPIO.setup(en,GPIO.OUT)

GPIO.setup(enB,GPIO.OUT)

 

#ADJUSTS SPEED

pulse1=GPIO.PWM(en,60) #setting the frequency to 1kHz

pulse2=GPIO.PWM(enB,63)

pulse1.start(40) #starting duty cycle at 25%

pulse2.start(40) #starting duty cycle at 25%

#functions for the car

 

def forward():

         print("straight")

         GPIO.output(15,GPIO.HIGH)

         GPIO.output(13,GPIO.LOW)

         GPIO.output(11,GPIO.HIGH)

         GPIO.output(7,GPIO.LOW)

         print("forward")

 

 

def right():

        print("right")

        GPIO.output(15,GPIO.HIGH)

        GPIO.output(13,GPIO.LOW)

        GPIO.output(11,GPIO.LOW)

        GPIO.output(7,GPIO.HIGH)

def left():

        print("left")

        GPIO.output(15,GPIO.LOW)

        GPIO.output(13,GPIO.HIGH)

        GPIO.output(11,GPIO.HIGH)

        GPIO.output(7,GPIO.LOW)

       

 

# Initialize camera

cap = cv2.VideoCapture(0)

cap.set(3, 384)  # Frame width

cap.set(4, 288)  # Frame height

 

def detect_line_and_adjust(frame):

    desired_position = frame.shape[1] / 2  # Center of the frame

    dead_zone_range = 12  # Dead zone range - ADJUST THIS IF THE LINE IS THICKER THAN EXPECTED. SMALLER DEAD ZONE RANGE = BETTER ACCURACY BUT MORE ZIG ZAGS(intial is 20)

 

    # Image processing

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

 

    if contours:

        cnt = max(contours, key=cv2.contourArea)

        M = cv2.moments(cnt)

        if M["m00"] != 0:

            cX = int(M["m10"] / M["m00"])

 

            if cX < desired_position - dead_zone_range:

                right()

            elif cX > desired_position + dead_zone_range:

                left()

            else:

                forward()

 

            cv2.circle(frame, (cX, int(frame.shape[0] / 3)), 5, (255, 0, 0), -1)

            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 1)

 

 

    return frame

 

def main():

    try:

        while True:

            ret, frame = cap.read()

            if not ret:

                break

 

            processed_frame = detect_line_and_adjust(frame)

            cv2.imshow("Line Following", processed_frame)

 

            if cv2.waitKey(1) & 0xFF == ord('q'):

                break

    finally:

        cap.release()

        cv2.destroyAllWindows()

        stop()

        GPIO.cleanup()

 

if __name__ == "__main__":

       main()
