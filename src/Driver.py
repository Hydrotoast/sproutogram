from SimpleCV import *

import os

from REPL import REPL
from Extraction import *
from ShollAnalysis import *
from ReportGeneration import *

class Driver(object):
	def extractSprouts(self, img):
		beadExtractor = BeadExtractor(img)
		beads = beadExtractor.extract()

		sproutExtractor = SproutExtractor(img, beads)
		sprouts = sproutExtractor.extract()

		sproutsImg = sprouts[-1].image

		for sprout in sprouts:
			sprout.restore(width=3, distanceThreshold=10)
		sproutsImgRestored = sprouts[-1].image
		sproutsImgRestored.show()

		raw_input()

	def extractMonoBead(self, img):
		extractor = HLSGExtractor(img)
		hlsgs = extractor.extract()
		for hlsg in hlsgs:
			img.dl().circle((hlsg.bead.x, hlsg.bead.y), hlsg.bead.radius(), color=Color.GREEN, width=5)
			for sprout in hlsg.sprouts:
				img.dl().line(sprout.end_points[0], sprout.end_points[1], color=Color.RED, width=3)
		# hlsgs.draw()
		img.show()
		raw_input()
		# for hlsg in hlsgs:
		# 	print hlsg

	def analyzeMonoBead(self, img):
		beadExtractor = BeadExtractor(img)
		beads = beadExtractor.extract()

		# Preprocessing steps
		imgEdges = img.edges(100,300)
		dilatedEdges = imgEdges.dilate(2)
		skeleton = dilatedEdges.skeletonize(10)

		analyzer = ShollAnalyzer(skeleton, beads[0])
		analysis = analyzer.analyze()
		return analysis

	def analyzeMonoBeadWithRestoration(self, img):
		beadExtractor = BeadExtractor(img)
		beads = beadExtractor.extract()

		sproutExtractor = SproutExtractor(img, beads)
		sprouts = sproutExtractor.extract()

		oImg = sproutExtractor.img
		for sprout in sprouts:
			sprout.restore(width=3, distanceThreshold=10)
		sproutsImg = sprouts[-1].image
		sproutsImg.show()

		analyzer = ShollAnalyzer(sproutsImg, beads[0])
		analysis = analyzer.analyze()
		return analysis

	def runExtractions(self):
		monoBead = Image('../data/samples/mono.jpg')
		monoBead = monoBead.resize(w=800)
		self.extractSprouts(monoBead)
		# self.extractMonoBead(monoBead)

	def extractSelected(self):
		imageSet = ImageSet('../data/samples/selected')
		reportGen = ShollAnalysisReport('../data/reports/selected.csv')
		for image in imageSet:
			filename = os.path.basename(image.filename)
			print 'Analyzing: %s' % filename		
			image = image.resize(w=800)
			analysis = self.analyzeMonoBeadWithRestoration(image)
			reportGen.addAnalysis(filename, analysis)
		reportGen.generate()

def main():
	repl = REPL()
	img = Image('../data/samples/mono.jpg')
	img = img.resize(w=800)
	repl.run(img)

if __name__ == '__main__':
	driver = Driver()
	# driver.runExtractions()
	driver.extractSelected()
