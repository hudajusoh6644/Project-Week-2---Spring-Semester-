#project week 2 - group 14
#shape detection and arrow code
#this code only detect the basic shapes not the arrows 
#library
import cv2
import numpy as np

#resolution of video
frameWidth = 1280
frameHeight = 720

#size of window for video 
cap = cv2.VideoCapture(0)
cap.set(4,frameWidth)
cap.set(5,frameHeight)


def empty(x):
    pass


cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",640,240)
cv2.createTrackbar("Threshold1","Parameters", 100,255,empty)
cv2.createTrackbar("Threshold2","Parameters", 200,255,empty)
cv2.createTrackbar("Area","Parameters",3000,3300,empty)


def getContours(imgDil, imgContours):
    contours, hierarchy = cv2.findContours(imgDil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    font = cv2.FONT_HERSHEY_COMPLEX  # Define the font here if used only in this function

    for cnt in contours:
        areaMin = cv2.getTrackbarPos("Area", "Parameters")
        area = cv2.contourArea(cnt)
        if area > areaMin:
            cv2.drawContours(imgContours, cnt, -1, (255, 0, 255), 3)  # Draw the contour
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(len(approx))
            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(imgContours,(x,y),(x+w,y+h),(0,255,0),3)#detect the green rectangle for each object
            cv2.putText(imgContours, "Points: "+str(len(approx)),(x + w + 20, y + 20),
                         cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),0) #print the point (red colour)
            cv2.putText(imgContours, "Area: "+str(int(area)),(x + w + 20, y + 45),
                        cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),0) #print the area (red colour)
            edges = len(approx)
            if(edges == 3):
                cv2.putText(imgContours, "triangle ",(x + w + 20, y + 65),
                        cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),0) #triangle
            elif(edges == 4):
                cv2.putText(imgContours, "rectangle/square ",(x + w + 20, y + 65),
                        cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),0) #square/rectangle
            elif(edges == 5):
                cv2.putText(imgContours, "pentagon ",(x + w + 20, y + 65),
                        cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),0) #hexagon
            elif(edges == 6):
                cv2.putText(imgContours, "hexagon ",(x + w + 20, y + 65),
                        cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),0) #hexagon
            elif(edges == 7):
                M = cv2.moments(cnt) 
                if M['m00'] != 0: 
                    cx = int(M['m10']/M['m00']) 
                    cy = int(M['m01']/M['m00']) 
  
                    base = max(approx, key=lambda p: ((cx - p[0][0])**2 + (cy - p[0][1])**2)**0.5) 
                    tip = min(approx, key=lambda p: ((cx - p[0][0])**2 + (cy - p[0][1])**2)**0.5) 
  
                    arrow_direction = "" 
                    dx = base[0][0] - tip[0][0] 
                    dy = base[0][1] - tip[0][1] 
  
                    if abs(dx) > abs(dy): 
                        arrow_direction = "Left" if dx > 0 else "Right" 
                    else: 
                        arrow_direction = "Down" if dy > 0 else "Up" 
  
  
                    cv2.putText(imgContours, arrow_direction + "Arrow:", (x + w + 20,y + 65), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 0) 
            elif(edges == 8):
                cv2.putText(imgContours, "circle  ",(x + w + 20,y + 65),
                        cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),0) #circle
            elif(edges == 9):
                cv2.putText(imgContours, "partial circle : ",(x + w + 20,y + 65),
                        cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),0) #partial circle    
            else:
                cv2.putText(imgContours, "unknown: ",(x + w + 20,y + 65),
                        cv2.FONT_HERSHEY_COMPLEX,0.7,(0,0,255),0) #unknown shape            


while cap.isOpened():
    ret,img = cap.read()
    imgContours = img.copy()
    imgBlur = cv2.GaussianBlur(img, (7,7),1)#blur video - can detect the egdes better
    imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)
    t1 = cv2.getTrackbarPos("Threshold1","Parameters")
    t2 = cv2.getTrackbarPos("Threshold2","Parameters")
    #print(t1,t2)
    imgCanny = cv2.Canny(imgGray,t1,t2)#black&white video (thin outline)
    
    
    kernel = np.ones((5,5))
    imgDil = cv2.dilate(imgCanny,kernel,iterations=1)#black&white video (thick outline)
    getContours(imgDil,imgContours=imgContours)
    
    imgGray = cv2.cvtColor(imgGray,cv2.COLOR_GRAY2BGR)
    imgCanny = cv2.cvtColor(imgCanny,cv2.COLOR_GRAY2BGR)
    imgDil = cv2.cvtColor(imgDil,cv2.COLOR_GRAY2BGR)
    imgStack = np.hstack([img,imgContours])#stack the display
    
    #cv2.imshow("Original Image", img)# display original image 
    #cv2.imshow('Blur Image', imgBlur)# display blur image
    cv2.imshow('output', imgStack)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()
