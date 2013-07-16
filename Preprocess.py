from SimpleCV import *
from SteerableFilter import SteerableFilter

def alpha_gen():
	start = ord('A')
	end = ord('Z')
	for letter_ord in range(start, end + 1):
		yield chr(letter_ord)

def approach(img, cannyMin=100, cannyMax=300, dilateCount=3):
	# Apply Canny's Edge Detection algorithm
	imgEdges = img.edges(cannyMin, cannyMax)

	# Blood Vessel detection using a circular hough transform
	circles = imgEdges.findCircle(canny=250, thresh=120, distance=150)
	print '%d %s' % (len(circles), 'circles found')
	# circles.draw(color=Color.GREEN, width=4)

	rCoff = 1.614
	circleMask = Image(imgEdges.size())
	circleMask.dl().circle((circles[0].x, circles[0].y), circles[0].radius() * rCoff, filled=True, color=Color.WHITE)
	circleMask = circleMask.applyLayers()
	imgEdges = imgEdges - circleMask

	# imgEdges = imgEdges.applyLayers()


	# Apply dilate morphological transformation
	closedImgEdges = imgEdges.dilate(dilateCount)

	# filterConf = SteerableFilter(closedImgEdges)
	# angularAdaptivelyFiltered = filterConf.convolve((circles[0].x, circles[0].y))
	# filterConf = SteerableFilter(angularAdaptivelyFiltered)
	# angularAdaptivelyFiltered = filterConf.convolve((circles[0].x, circles[0].y))

	# Find the skeleton
	skeleton = closedImgEdges.skeletonize(10)
	blobs = skeleton.findBlobs()
	if blobs:
		blobs.draw(Color.GREEN)
	print '%d %s' % (len(blobs), 'blobs found')

	# Label blobs
	textLayer = DrawingLayer(skeleton.size())
	for letter, blob in zip(alpha_gen(), blobs):
		textLayer.text(letter, blob.centroid(), color=Color.GREEN, alpha=255) #, blob.centroid(), color=Color.GREEN)
	skeleton.addDrawingLayer(textLayer)
	skeleton = skeleton.applyLayers()

	closedImgEdges = closedImgEdges.invert()

	# frame = img.sideBySide(
	# 	imgEdges.sideBySide(
	# 		closedImgEdges.sideBySide(
	# 			skeleton.sideBySide(
	# 				angularAdaptivelyFiltered))))
	frame = img.sideBySide(
		imgEdges.sideBySide(
			closedImgEdges.sideBySide(
				skeleton)))
	return frame

