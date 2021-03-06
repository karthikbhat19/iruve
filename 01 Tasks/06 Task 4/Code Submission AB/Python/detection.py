'''
* Team Id          : 226
* Author List      : Suryanarayan
* Filename         : detection.py
* Theme            : Ant Bot
* Functions        : detect_sim_id,detect_color 
* Global Variables : aruco_id
'''

import numpy
import cv2
import cv2.aruco as aruco
from aruco_lib import *
import os
aruco_id = None

'''
* Function Name : detect_color
* Input         : Path to the image file
* Output        : Color - String 
* Logic         : Detects the block colors in the image.
                  Returns None if no color is detected.
* Example Call  : detect_sim_id("Image.jpg")
'''
def detect_color(path_to_image,angle):  # color detection function
    # taking 3 points from the image to get its bgr values
    # for 135 degrees  = [(150,160),(263,33),(370,155)]
    # for 45 degrees   = [(350,185),(260,75),(165,185)]
    # for 90 degrees   = [(215,285),(270,160),(430,300)]
    img = cv2.imread(path_to_image)    #reading image
    cv2.imshow("img",img)
    px = list()
    ind= list()
    px.clear()
    ind.clear()
    if(angle==90):                      
        px.append(list(img[215,285]))   #getting bgr values of that pixel and adding to list px
        px.append(list(img[270,160]))
        px.append(list(img[430,300]))

    if(angle==45):
        px.append(list(img[350,185]))
        px.append(list(img[260,75]))
        px.append(list(img[165,185]))

    if(angle==135):
        px.append(list(img[150,160]))
        px.append(list(img[263,33]))
        px.append(list(img[370,155]))

    for i in px:        # looping through the rgb values list of 3 points in the image
        maxi= max(i)
        ind.append(i.index(maxi))   #getting the index of the max value in rgb

    if(ind.count(0)>1):     #counting the no of Blue Green or Red value  
            print("BLUE")
            return "BLUE"
    if(ind.count(1)>1):     #if one color found two or more times , print that color
            print("GREEN")
            return "GREEN"
    if(ind.count(2)>1):
            print("RED")
            return "RED"

    #print(px)
    #print(ind)
    #cv2.waitKey(0)
    cv2.destroyAllWindows()

'''
* Function Name : detect_sim_id
* Input         : Path to the image file
* Output        : Aruco ID - Integer 
* Logic         : Detects the Arcuo Ids if present in the given Image file.
                  Returns None if no Aruco is detected. Uses Aruco library provided by the e-Yantra team
* Example Call  : detect_sim_id("Image.jpg")
'''
def detect_sim_id(path_to_image):
    global aruco_id
    img = cv2.imread(path_to_image) #give the name of the image with the complete path
    det_aruco_list = {}
    det_aruco_list = detect_Aruco(img)  #calling detect_Aruco from the aruco library
    #print(det_aruco_list)
    if det_aruco_list:
        aruco_id = list(det_aruco_list.keys())[0] #taking only the id value
        return aruco_id
        
#for i in range(4):
#		print(i,detect_sim_id(str(i)+".png"))

'''
* Function Name : detect_trash
* Input         : Path to the image file
* Output        : result -> Boolean value 
* Logic         : Detects the trash block if present in the given Image file.
* Example Call  : detect_sim_id("Image.jpg")
'''
def detect_trash(path_to_image):
        img= cv2.imread(path_to_image)
        #cv2.imshow("pic",img)
        #cv2.waitKey(0)
        px = list()
        count=0
        px.clear()
                             
        px.append(list(img[184,110]))   #getting bgr values of that pixel and adding to list px
        px.append(list(img[340,52]))
        px.append(list(img[430,160]))
        px.append(list(img[297,207]))
        #print(px)
        for i in px:
                if((i[0]-i[2])>60 and (i[1]-i[2])>60):
                        count=count+1
        if(count>2):
                return 'T'
        else:
                return 'W'

print(detect_trash("trash.jpg"))
