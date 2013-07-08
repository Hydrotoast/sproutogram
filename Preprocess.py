from SimpleCV import Color

def approach1(img, cannyMin=100, cannyMax=300, dilateCount=1):
	# Apply Canny's Edge Detection algorithm
	imgEdges = img.edges(cannyMin, cannyMax)

	circles = imgEdges.findCircle(canny=250, thresh=120, distance=120)
	print(len(circles), 'circles found')
	circles.draw(Color.GREEN, width=4)
	imgEdges = imgEdges.applyLayers()

	# Apply dilate morphological transformation
	closedImgEdges = imgEdges.dilate(dilateCount)
	closedImgEdges = closedImgEdges.invert()

	frame = img.sideBySide(imgEdges.sideBySide(closedImgEdges))
	return frame
