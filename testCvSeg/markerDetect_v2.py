#!/usr/bin/env python
import cv2
import pdb
import numpy as np

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

def getStopMarkerSize(imageIn, imgToDrawOn):

	img = imageIn.clone()

	img_width = 640
	img_height = 360

	filtered = np.zeros((img_height, img_width, 1), "uint8")
	filtered2 = np.zeros((img_height, img_width, 1), "uint8")
	filtered3 = np.zeros((img_height, img_width, 1), "uint8")
	filtered4 = np.zeros((img_height, img_width, 1), "uint8")
	
	B = img[:,:,0]
	G = img[:,:,1]
	R = img[:,:,2]

	#algorithm parameters
	boolBlur = True
	maxR = 40
	minR = 0
	maxB = 40
	minB = 0
	maxG = 40
	minG = 0
	kernelSize = 2
	skipNum = 5
	and2 = 1
	difThreshInt = 20

	if boolBlur:
		img = cv2.medianBlur(img, blurAmt*2+1)


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

	#img2show is the result of filtering


	img2show = img2show*255

	num_img_rows = img2show.shape[0]
	num_img_cols = img2show.shape[1]
	skipCnt = 0

	rows = []
	leftCols = []
	rightCols = []
	regionCount = 0
	

	for i in xrange(num_img_rows):
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


	#grab the median
	if (regionCount > 0):
		medVal = regionCount//2
		rowAvg = rows[medVal]
		leftColAvg = leftCols[medVal]
		rightColAvg = rightCols[medVal]
	
		cv2.line(imgToDrawOn, (leftColAvg, rowAvg), (rightColAvg, rowAvg), (255,0,0), 3)

		return rightColAvg - leftColAvg
	else:
		return -1.0


