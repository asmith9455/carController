#!/usr/bin/env python
import cv2
import pdb
import numpy as np

thres = 0

def nothing(inte):
	pass

img_width = 640
img_height = 360

#cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)I420, framerate=(fraction)120/1 ! nvvidconv flip-method=2 ! video/x-raw, format=(string)I420 ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)"+str(img_width)+", height=(int)"+str(img_height)+", format=(string)I420, framerate=(fraction)120/1 ! nvvidconv flip-method=2 ! video/x-raw, format=(string)I420 ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

cv2.namedWindow("filtered2")
cv2.createTrackbar('redMax', 'filtered2', 255, 255, nothing)
cv2.createTrackbar('redMin', 'filtered2', 1, 255, nothing)
cv2.createTrackbar('blueMax', 'filtered2', 255, 255, nothing)
cv2.createTrackbar('blueMin', 'filtered2', 1, 255, nothing)
cv2.createTrackbar('greenMax', 'filtered2', 255, 255, nothing)
cv2.createTrackbar('greenMin', 'filtered2', 1, 255, nothing)
cv2.createTrackbar('andHistory', 'filtered2', 0, 1, nothing) 
cv2.createTrackbar('kernelSize(2*n+1)', 'filtered2', 2, 10, nothing) 


avg2 = np.zeros((img_height, img_width, 1), "uint8")
msk = np.ones((img_height, img_width, 1), "uint8")*255
while True:
	ret, img = cap.read()
	cv2.imshow("original feed", img)
	#lastImg = blueComponents
	
	filtered = np.zeros((img_height, img_width, 1), "uint8")
	filtered2 = np.zeros((img_height, img_width, 1), "uint8")
	filtered3 = np.zeros((img_height, img_width, 1), "uint8")
	filtered4 = np.zeros((img_height, img_width, 1), "uint8")
	
	B = img[:,:,0]
	G = img[:,:,1]
	R = img[:,:,2]

	avgBG = G / 2 + R / 2

	#pdb.set_trace()
	avgBGs = avgBG.astype(np.float32, copy = False)
	Rs = R.astype(np.float32, copy = False)

	#x,y = np.where(B > avgGR)
	
	sub = Rs - avgBGs;

	maxR = cv2.getTrackbarPos('redMax', 'filtered2')
	minR = cv2.getTrackbarPos('redMin', 'filtered2')
	maxB = cv2.getTrackbarPos('blueMax', 'filtered2')
	minB = cv2.getTrackbarPos('blueMin', 'filtered2')
	maxG = cv2.getTrackbarPos('greenMax', 'filtered2')
	minG = cv2.getTrackbarPos('greenMin', 'filtered2')
	kernelSize = cv2.getTrackbarPos('kernelSize(2*n+1)', 'filtered2')

	and2 = cv2.getTrackbarPos('andHistory', 'filtered2')

	x2, y2 = np.where((R >= minR) & (R <= maxR))
	x3, y3 = np.where((B >= minB) & (B <= maxB))
	x4, y4 = np.where((G >= minG) & (G <= maxG))
	
	filtered2[x2,y2] = 255
	filtered3[x3,y3] = 255
	filtered4[x4,y4] = 255

	filtered5 = np.logical_and(filtered2, filtered3, msk)
	filtered5 = np.logical_and(filtered5, filtered4, msk)	

	if (and2 == 0):
		cv2.imshow("filtered2", filtered5*255)
	else:
		avg2 = np.logical_and(lastFiltered, filtered5, msk)
		avg2Img = avg2.astype(np.uint8, copy = False)*255
		kSize1 = 2*kernelSize + 1
		kSize2 = 4*kernelSize + 1
		avg2Img = cv2.erode(avg2Img, np.ones((kSize1,kSize1)))
		avg2Img = cv2.dilate(avg2Img, np.ones((kSize2,kSize2)))
		avg2Img = cv2.erode(avg2Img, np.ones((kSize1,kSize1)))
		#pdb.set_trace()
		cv2.imshow("filtered2", avg2Img)

	lastFiltered = filtered5
		
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

