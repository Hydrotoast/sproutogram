from SimpleCV import *

import os

from REPL import REPL
from Extraction import *
from ShollAnalysis import *
from ReportGenerator import *

class Driver(object):
	def extractSprouts(self, img):
		beadExtractor = BeadExtractor(img)
		beads = beadExtractor.extract()

		sproutExtractor = SproutExtractor(img, beads)
		sprouts = sproutExtractor.extract()
		sprouts.draw(color=Color.RED, width=4)
		sproutsImg = sprouts[-1].image
		frame = img.sideBySide(sproutsImg)
		frame.show()
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

		imgEdges = img.edges(100,300)
		dilatedEdges = imgEdges.dilate(2)
		skeleton = dilatedEdges.skeletonize(10)
		analyzer = ShollAnalyzer(skeleton)
		analysis = analyzer.analyze(beads[0])
		return analysis, analyzer.sproutCount(), analyzer.sproutMaximum()

	def runExtractions(self):
		monoBead = Image('../data/samples/mono.jpg')
		monoBead = monoBead.resize(w=800)
		# self.extractMonoBead(monoBead)
		# self.extractSprouts(monoBead)
		self.analyzeMonoBead(monoBead)

	def extractSelected(self):
		imageSet = ImageSet('../data/samples/selected')
		reportGen = ShollAnalysisReport()
		reportGen.setOutput('../data/reports/selected.csv')
		for image in imageSet:
			filename = os.path.basename(image.filename)
			print 'Analyzing: %s' % filename		
			image = image.resize(w=800)
			analysis, sproutCount, sproutMax = self.analyzeMonoBead(image)
			reportGen.addAnalysis(filename, analysis, sproutCount, sproutMax)
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
