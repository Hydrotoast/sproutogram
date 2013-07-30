from Features import HLSG
import csv

class ReportGenerator(object):
	def __init__(self):
		self.analyses = {}

	def setOutput(self, filename):
		self.output = filename

	def formatHLSG(self, hlsg):
		formatStr = "HLSG at (%d, %d) with %d sprouts"
		return formatStr % (hlsg.bead.x, hlsg.bead.y, len(hlsg.sprouts))

	def generate(self):
		pass


class ShollAnalysisReport(ReportGenerator):
	def __init__(self):
		super(ShollAnalysisReport, self).__init__()

	def addAnalysis(self, filename, analysis, sproutCount, sproutMax):
		self.analyses[filename] = analysis, sproutCount, sproutMax

	def generate(self):
		with open(self.output, 'w') as fh:
			writer = csv.writer(fh)

			writer.writerow(['Overview'])
			for filename, data in self.analyses.items():
				(analysis, sproutCount, sproutMax) = data
				writer.writerow([filename])
				writer.writerow(['Sprout Count', sproutCount])
				writer.writerow(['Sprout Max', sproutMax])
				writer.writerow([])

			for filename, data in self.analyses.items():
				(analysis, sproutCount, sproutMax) = data
				writer.writerow([filename])
				writer.writerow(['Radius'] + analysis.keys())
				writer.writerow(['Crossings'] + analysis.values())
				# writer.writerow(['Radius', 'Crossings'])
				# for radius, counts in analysis.items():
				# 	writer.writerow([str(radius), str(counts)])
				writer.writerow([])
