from SimpleCV import *

import os
from multiprocessing import Pool

import matplotlib.pyplot as plt

from REPL import REPL
from Extraction import *
from ShollAnalysis import *
from ReportGeneration import *

from strategy import *

"""
An Extraction task defines an atomic job for extracting and quantitatively
analyzing an image set of fibrin gel bead sprouting assays.
"""
class ExtractionTask(object):
	def __init__(self, inPath, outPath, reportPath, plotPath):
		self.inPath = inPath
		self.outPath = outPath
		self.reportPath = reportPath
		self.plotPath = plotPath
		self.analyzer = ShollAnalyzer()

	def analyzeMonoBead(self, img):
		beadExtractor = BeadExtractor(img)
		beads = beadExtractor.extract()

		sproutExtractor = SproutExtractor(img, beads)
		sprouts = sproutExtractor.extract()
		for sprout in sprouts:
			sprout.restore(width=3, distanceThreshold=24, color=Color.WHITE)
		sproutsImg = sprouts[-1].image.applyLayers()
		sproutsImg.resize(w=800).show()

		analysis = self.analyzer.analyze(sproutsImg, beads[0])

		print "\t%d sprouts found" % analysis.sproutCount
		return analysis

	def extract(self):
		imageSet = ImageSet(self.inPath)
		imageSet.sort()
		reportGen = ShollAnalysisReport(self.reportPath)
		counter = 1
		for image in imageSet:
			filename = os.path.splitext(os.path.basename(image.filename))[0]

			print 'Analyzing %d/%d: %s' % (counter, len(imageSet.filelist), filename)	
			analysis = self.analyzeMonoBead(image)

			# Sholl Analysis Plots
			self.plotShollAnalysis(analysis, filename)

			# Add to overall report
			reportGen.addAnalysis(filename, analysis)

			counter += 1
		reportGen.generate()

	def plotShollAnalysis(self, analysis, filename):
		plt.figure(1, figsize=(18, 6))
		plt.plot(analysis.crossings.keys(), analysis.crossings.values())
		plt.title('Sholl Analysis for ' + filename)
		plt.xlabel('Radius')
		plt.ylabel('Crossings')
		plt.savefig(os.path.join(self.plotPath, filename + ".png"))
		plt.clf()

class AveragedIntegrationExtractionTask(ExtractionTask):
	def __init__(self, inPath, outPath, reportPath, plotPath):
		super(ExtractionTask, self).__init__(inPath, outPath, reportPath, plotPath)
		self.analyzer = ShollAnalyzer(IntegrationStrategy.AveragedAnalysisStrategy())

class MedianIntegrationExtractionTask(ExtractionTask):
	def __init__(self, inPath, outPath, reportPath, plotPath):
		super(ExtractionTask, self).__init__(inPath, outPath, reportPath, plotPath)
		self.analyzer = ShollAnalyzer(IntegrationStrategy.MedianAnalysisStrategy())

"""
Drives premade sets of extraction tasks
"""
class Driver(object):
	def extractSelected(self):
		inPath = '../data/samples/selected'
		reportPath = '../data/reports/selected.csv'
		plotPath = '../data/reports/plots'
		task = ExtractionTask(inPath, inPath, reportPath, plotPath)
		task.extract()

def main():
	repl = REPL()
	img = Image('../data/samples/mono.jpg')
	img = img.resize(w=800)
	repl.run(img)

if __name__ == '__main__':
	driver = Driver()
	driver.extractSelected()
