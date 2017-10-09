#!/usr/bin/env python
import cv2
import pdb
import numpy as np
from screen_grabber import screen_grabber
thres = 0

def nothing(inte):
	pass
cap = screen_grabber((1280,720))#cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)I420, framerate=(fraction)120/1 ! nvvidconv flip-method=2 ! video/x-raw, format=(string)I420 ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
#cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)640, height=(int)360, format=(string)I420, framerate=(fraction)120/1 ! nvvidconv flip-method=2 ! video/x-raw, format=(string)I420 ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

cv2.namedWindow("filtered2")
cv2.createTrackbar('blueThres', 'filtered2', 0, 100, nothing)
cv2.createTrackbar('andHistory', 'filtered2', 0, 1, nothing) 

img_width = 1280
img_height = 720

avg2 = np.zeros((img_height, img_width, 1), "uint8")
msk = np.ones((img_height, img_width, 1), "uint8")*255
while True:
	img = cap.get_img()
	cv2.imshow("original feed", img)
	#lastImg = blueComponents
	
	filtered = np.zeros((img_height, img_width, 1), "uint8")
	filtered2 = np.zeros((img_height, img_width, 1), "uint8")
	
	
	B = img[:,:,0]
	G = img[:,:,1]
	R = img[:,:,2]

	avgBG = G / 2 + R / 2

	#pdb.set_trace()
	avgBGs = avgBG.astype(np.float32, copy = False)
	Rs = R.astype(np.float32, copy = False)

	#x,y = np.where(B > avgGR)
	
	sub = Rs - avgBGs;

	thres = cv2.getTrackbarPos('blueThres', 'filtered2')
	and2 = cv2.getTrackbarPos('andHistory', 'filtered2')

	x2, y2 = np.where(sub > thres)

	
	filtered2[x2,y2] = 255

	

	if (and2 == 0):
		cv2.imshow("filtered2", filtered2)
	else:
		avg2 = np.logical_and(lastFiltered, filtered2, msk)
		#pdb.set_trace()
		#cv2.imshow("filtered2", avg2)
		cv2.imshow("filtered2", filtered2)
		cv2.imshow("filtered22", lastFiltered)
		cv2.imshow("vg", avg2.astype(np.uint8, copy = False)*255)

	lastFiltered = filtered2
		
	#filtered[x,y] = 255
	
	#pdb.set_trace()
	#cv2.imshow("filtered", filtered)
	
	#cv2.imshow("lastFiltered", lastFiltered)
	#f = np.logical_and(filtered, lastFiltered)
	
	#cv2.imshow("f", f)
	#cv2.imshow("B", B)
	#cv2.imshow("G", G)
	#cv2.imshow("R", R)
	#cv2.imshow("avgGR", avgGR)
	if cv2.waitKey(100) & 0xFF == 27:
   		break

cv2.DestroyAllWindows()

