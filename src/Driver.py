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

		print "%d beads detected" % len(beads)
		print "%d sprout blobs detected" % len(sprouts)

		sproutsImg = sprouts[-1].image
		for sprout in sprouts:
			sprout.restore(width=3, distanceThreshold=48, color=Color.TEAL)
			# sprout.draw(color=Color.BLUE, width=4)
		sproutsImgRestored = sprouts[-1].image

		sproutsImgRestored.applyLayers().resize(w=1024).show()

	def extractMonoBead(self, img):
		extractor = HLSGExtractor(img)
		hlsgs = extractor.extract()
		for hlsg in hlsgs:
			img.dl().circle((hlsg.bead.x, hlsg.bead.y), hlsg.bead.radius(), color=Color.GREEN, width=5)
			for sprout in hlsg.sprouts:
				img.dl().line(sprout.end_points[0], sprout.end_points[1], color=Color.RED, width=3)

	def analyzeMonoBead(self, img):
		beadExtractor = BeadExtractor(img)
		beads = beadExtractor.extract()

		sproutExtractor = SproutExtractor(img, beads)
		sprouts = sproutExtractor.extract()
		# for sprout in sprouts:
		# 	sprout.restore(width=3, distanceThreshold=24, color=Color.WHITE)
		sproutsImg = sprouts[-1].image.applyLayers()
		sproutsImg.resize(w=800).show()

		analyzer = ShollAnalyzer(sproutsImg, beads[0])
		analysis = analyzer.analyze()
		print "\t%d sprouts found" % analysis.sproutCount
		return analysis

	def runExtractions(self):
		imageSet = ImageSet('../data/samples/selected')
		for image in imageSet:
			filename = os.path.basename(image.filename)
			print 'Analyzing: %s' % filename		
			self.extractSprouts(image)

	def extractSelected(self):
		imageSet = ImageSet('../data/samples/selected')
		reportGen = ShollAnalysisReport('../data/reports/selected.csv')
		for image in imageSet:
			filename = os.path.basename(image.filename)
			print 'Analyzing: %s' % filename		
			analysis = self.analyzeMonoBead(image)
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
