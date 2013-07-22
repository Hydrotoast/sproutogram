from math import *
from sets import Set

from SimpleCV import *
from SteerableFilter import SteerableFilter

from Geometry import *
from DisjointSet import *

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
	circleMask.dl().circle(
		(circles[0].x, circles[0].y),
		circles[0].radius() * rCoff,
		filled=True,
		color=Color.WHITE)
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
	labeledBlobs = zip(alpha_gen(), blobs)
	blobSegments = []
	if blobs:
		# Acquire blob segments
		for label, blob in labeledBlobs:
			sortedContour = sorted(
				blob.contour(), 
				key = lambda x: euclidDistance(x, (circles[0].x, circles[0].y)))
			start = sortedContour[0]
			end = sortedContour[-1]

			skeleton.dl().circle((start[0], start[1]), 8, color=Color.RED)
			skeleton.dl().circle((end[0], end[1]), 8, color=Color.BLUE)

			radialSegment = RadialSegment(label, start, end, blob)
			blobSegments.append(radialSegment)
		blobs.draw(Color.GREEN)
	print '%d %s' % (len(blobs), 'blobs found')

	sprouts = []
	distanceThreshold = 20
	hypoSegments = []
	for blobSegmentEnd in blobSegments:
		for blobSegmentStart in blobSegments:
			if blobSegmentEnd.label == blobSegmentStart.label:
				continue
			distance = euclidDistance(blobSegmentEnd.end, blobSegmentStart.start)
			if distance < distanceThreshold:
				hypoSegments.append((blobSegmentEnd, blobSegmentStart))
	
	setItems = DisjointSet(blobSegments)
	for hypoSegment in hypoSegments:
		setItems.union(
			setItems.find(hypoSegment[0]), 
			setItems.find(hypoSegment[1]))
	uniqueParents = []
	for key, value in setItems.nodes.items():
		uniqueParents.append(value.parent)

	sprouts = list(set(uniqueParents))
	print '%d sprouts found'  % len(sprouts)
	for sprout in sprouts:
		print sprout

	# Label blobs
	textLayer = DrawingLayer(skeleton.size())
	for label, blob in labeledBlobs:
		textLayer.text(
			label,
			blob.centroid(),
			color=Color.GREEN,
			alpha=255)
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

