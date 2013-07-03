def approach1(img, cannyMin=100, cannyMax=300, dilateCount=1):
	# Apply Canny's Edge Detection algorithm
	imgEdges = img.edges(cannyMin, cannyMax)

	# Apply dilate morphological transformation
	closedImgEdges = imgEdges.dilate(dilateCount)
	closedImgEdges = closedImgEdges.invert()

	frame = img.sideBySide(imgEdges.sideBySide(closedImgEdges))
	return frame

def approach2(img, binarizeThresh=80, dilateCount=1):
	# Binarize
	imgEdges = img.binarize(binarizeThresh=80)

	# Apply dilate morphological transformation
	closedImgEdges = imgEdges.dilate(dilateCount=1)
	closedImgEdges = closedImgEdges.invert()

	frame = img.sideBySide(imgEdges.sideBySide(closedImgEdges))
	return frame
