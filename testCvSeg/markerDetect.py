#!/usr/bin/env python
import cv2
import pdb
import numpy as np
from screen_grabber import screen_grabber
thres = 0

def getSmBounds(regionsWithRatio):
	smBounds = []
	for region in regionsWithRatio:
		regionWidth = region[1]
		regionEndCol = region[0]
		startCol = regionEndCol - regionWidth*5
		endCol = regionEndCol + regionWidth
		smBounds.append([startCol, endCol])
	return smBounds

def checkRatios(ordered_regions, difThresh):
	thirdLastWidth = 0
	secondLastWidth = 0
	lastWidth = 0
	regionsWithRatio = []
	delay = 0
	for region in ordered_regions:
		thisWidth = region[1]
		
		#pdb.set_trace()
		if delay < 2:
			delay += 1
			secondLastWidth = lastWidth
			lastWidth = thisWidth
			continue

		ratio = float (lastWidth) / thisWidth
		ratio2 = float (secondLastWidth) / lastWidth
		ratio3 = float (thirdLastWidth) / secondLastWidth

		thirdLastWidth = secondLastWidth
		secondLastWidth = lastWidth
		lastWidth = thisWidth

		b1 = abs(ratio - 1.0) < difThresh 
		b2 = abs(ratio2 - 1.0) < difThresh
		b3 = abs(ratio3 - 1.0) < difThresh
		#pdb.set_trace()
		if b1 and b2 and b3 and region[2] == 0:
			 regionsWithRatio.append(region)

	return regionsWithRatio

def solidRegionWidths(img_row):

	#img_row = [[0], [0], [255], [255], [255], [0]]

	#img_row.append([-1])	#so that the last region will trigger the append region with code

	lastPixel = img_row[0][0]
	regionWidths = []
	firstPix = 0;
	col = 0
	state = 0
	
	for pixel in img_row:
		
		pix_val = pixel[0]
		
		if(lastPixel != pix_val):
			regionWidths.append([col - 1, col - firstPix, lastPixel])
			firstPix = col #set the first pixel of the next region
		lastPixel = pix_val
		col+=1

	regionWidths.append([col - 1, col - firstPix, lastPixel])

	#pdb.set_trace()
	return regionWidths

def getOrdered1Regions(img_row):
	lastPixel = 0
	ordered_regions = []
	currentRegion = []
	col = 0
	
	for pixel in img_row:
		pix_val = pixel[0]
		if (lastPixel == 0 and pix_val == 255):
			currentRegion.append(col)
			#pdb.set_trace()
		if (lastPixel == 255 and pix_val == 0):
			currentRegion.append(col)
			ordered_regions.append(currentRegion)
			currentRegion = []
			#pdb.set_trace()	
		lastPixel = pix_val
		col+=1
	#pdb.set_trace()
	return ordered_regions

def nothing(inte):
	pass

img_width = 1280
img_height = 720

#cap = cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)I420, framerate=(fraction)120/1 ! nvvidconv flip-method=2 ! video/x-raw, format=(string)I420 ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")
cap = screen_grabber((img_width, img_height))#cv2.VideoCapture("nvcamerasrc ! video/x-raw(memory:NVMM), width=(int)1280, height=(int)720, format=(string)I420, framerate=(fraction)120/1 ! nvvidconv flip-method=2 ! video/x-raw, format=(string)I420 ! videoconvert ! video/x-raw, format=(string)BGR ! appsink")

cv2.namedWindow("filtered2")
cv2.createTrackbar('redMax', 'filtered2', 40, 255, nothing)
cv2.createTrackbar('redMin', 'filtered2', 0, 255, nothing)
cv2.createTrackbar('blueMax', 'filtered2', 40, 255, nothing)
cv2.createTrackbar('blueMin', 'filtered2', 0, 255, nothing)
cv2.createTrackbar('greenMax', 'filtered2', 40, 255, nothing)
cv2.createTrackbar('greenMin', 'filtered2', 0, 255, nothing)
cv2.createTrackbar('andHistory', 'filtered2', 0, 1, nothing)
cv2.createTrackbar('kernelSize(2*n+1)', 'filtered2', 2, 10, nothing) 
cv2.createTrackbar('difThresh', 'filtered2', 20, 100, nothing)
cv2.createTrackbar('lineSpacing', 'filtered2', 10, 50, nothing)
cv2.createTrackbar('blurInput', 'filtered2', 0, 1, nothing)
cv2.createTrackbar('blurAmount', 'filtered2', 2, 10, nothing)

avg2 = np.zeros((img_height, img_width, 1), "uint8")
msk = np.ones((img_height, img_width, 1), "uint8")*255
while True:


	boolBlur = cv2.getTrackbarPos('blurInput', 'filtered2')
	blurAmt = cv2.getTrackbarPos('blurAmount', 'filtered2')
	img = cap.get_img()

	if boolBlur:
		img = cv2.medianBlur(img, blurAmt*2+1)

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
	skipNum = cv2.getTrackbarPos('lineSpacing', 'filtered2') + 1

	and2 = cv2.getTrackbarPos('andHistory', 'filtered2')
	#and2 = 1
	difThreshInt = cv2.getTrackbarPos('difThresh', 'filtered2')
	difThresh = float(difThreshInt) / 100

	x2, y2 = np.where((R >= minR) & (R <= maxR))
	x3, y3 = np.where((B >= minB) & (B <= maxB))
	x4, y4 = np.where((G >= minG) & (G <= maxG))
	
	filtered2[x2,y2] = 255
	filtered3[x3,y3] = 255
	filtered4[x4,y4] = 255

	filtered5 = np.logical_and(filtered2, filtered3, msk)
	filtered5 = np.logical_and(filtered5, filtered4, msk)

	

	img2show = filtered5
	img2show_bin = filtered5

	if (and2 == 1):
		#avg2 = np.logical_and(lastFiltered, filtered5, msk)
		#avg2Img = avg2.astype(np.uint8, copy = False)*255
		kSize1 = 2*kernelSize + 1
		kSize2 = 4*kernelSize + 1
		filtered5 = cv2.erode(filtered5, np.ones((kSize1,kSize1)))
		filtered5 = cv2.dilate(filtered5, np.ones((kSize2,kSize2)))
		filtered5 = cv2.erode(filtered5, np.ones((kSize1,kSize1)))
		img2show[:,:,0] = filtered5[:,:]

	#pdb.set_trace()


	img2show = img2show*255

	num_img_rows = img2show.shape[0]
	num_img_cols = img2show.shape[1]
	skipCnt = 0

	rows = []
	leftCols = []
	rightCols = []
	regionCount = 0
	

	for i in range(num_img_rows):
		skipCnt+=1
		if skipCnt % skipNum != 0:
			continue
		
		#pdb.set_trace()

		regions = solidRegionWidths(img2show[i, :])
		
		obj = checkRatios(regions, difThresh)
		
		smBounds = getSmBounds(obj)

		for smBound in smBounds:
			rows.append(i)
			leftCols.append(smBound[0])
			rightCols.append(smBound[1])
			regionCount += 1

		for pair in obj:
			cv2.line(img, (pair[0] - pair[1], i), (pair[0], i), (0,0,255), 1)

	#rows are already in order
	leftCols.sort()
	rightCols.sort()

	if (regionCount > 0):
		medVal = regionCount//2
		rowAvg = rows[medVal]
		leftColAvg = leftCols[medVal]
		rightColAvg = rightCols[medVal]
	
		cv2.line(img, (leftColAvg, rowAvg), (rightColAvg, rowAvg), (255,0,0), 3)

	cv2.imshow("filtered2", img2show)
	cv2.imshow("altered", img2show)
	cv2.imshow("original feed", img)

	if cv2.waitKey(100) & 0xFF == 27:
   		break

cv2.DestroyAllWindows()

