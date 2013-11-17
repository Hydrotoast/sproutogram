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
	def __init__(self, inPath, outPath, reportPath):
		self.inPath = inPath
		self.outPath = outPath
		self.methodName = self.__class__.__name__ + str(self.analyzer.beadFactor)
		self.reportPath = os.path.join(reportPath, self.methodName)
		self.plotPath = os.path.join(self.reportPath, 'plots')
		if not os.path.exists(self.reportPath):
			os.makedirs(self.reportPath)
		if not os.path.exists(self.plotPath):
			os.makedirs(self.plotPath)

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

# 		print "\t%d sprouts found" % analysis.sproutCount
		return analysis

	def extract(self):
		imageSet = ImageSet(self.inPath)
		imageSet.sort()
		reportGen = ShollAnalysisReport(os.path.join(self.reportPath, self.methodName + '.csv'))
		counter = 1
		print 'Extracting using %s' % self.methodName
		for image in imageSet:
			filename = os.path.splitext(os.path.basename(image.filename))[0]

# 			print 'Analyzing %d/%d: %s' % (counter, len(imageSet.filelist), filename)	
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

class AveragedExtractionTask(ExtractionTask):
	def __init__(self, inPath, outPath, reportPath, beadFactor=1.5, stepSize=1):
		self.analyzer = ShollAnalyzer(IntegrationStrategy.AveragedAnalysisStrategy(), beadFactor, stepSize)
		super(AveragedExtractionTask, self).__init__(inPath, outPath, reportPath)

class ThresholdAverageExtractionTask(ExtractionTask):
	def __init__(self, inPath, outPath, reportPath, beadFactor=1.5, stepSize=1):
		self.analyzer = ShollAnalyzer(IntegrationStrategy.ThresholdAverageStrategy(), beadFactor)
		super(ThresholdAverageExtractionTask, self).__init__(inPath, outPath, reportPath)

class MedianIntegrationExtractionTask(ExtractionTask):
	def __init__(self, inPath, outPath, reportPath, beadFactor=1.5, stepSize=1):
		self.analyzer = ShollAnalyzer(IntegrationStrategy.MedianAnalysisStrategy(), beadFactor, stepSize)
		super(MedianIntegrationExtractionTask, self).__init__(inPath, outPath, reportPath)
		
def concurrentExtract(task):
	task.extract()

"""
Drives premade sets of extraction tasks
"""
class Driver(object):
	def extractSelected(self):
		inPath = '../data/samples/selected'
		reportPath = '../data/reports/'
		pool = Pool(4)
		tasks = []
# 		for i in np.arange(1.5, 3.1, 0.1):
# 			task = AveragedExtractionTask(inPath, inPath, reportPath, i)
# 			task.extract()
 		for i in np.arange(1.5, 3.1, 0.1):
 			tasks.append(ThresholdAverageExtractionTask(inPath, inPath, reportPath, i))
# 		for i in np.arange(1.5, 3.1, 0.1):
# 			tasks.append(MedianIntegrationExtractionTask(inPath, inPath, reportPath, i))
		pool.map(concurrentExtract, tasks)

if __name__ == '__main__':
	driver = Driver()
	driver.extractSelected()
