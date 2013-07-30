from Features import HLSG
import csv

class ReportGeneratorBase(object):
	"""
	Abstract base class for generating reports as CSV files.
	"""
	def __init__(self, filename):
		self.output = filename
		self.analyses = {}

	def generate(self):
		pass


class ShollAnalysisReport(ReportGeneratorBase):
	"""
	Generates reports given a Sholl Analysis of an angiogram. The report
	includes the primary sprout count, maximum sprout count raw data dump of
	the analysis.
	"""
	def __init__(self, filename):
		super(ShollAnalysisReport, self).__init__(filename)

	def addAnalysis(self, filename, crossings, sproutCount, sproutMax):
		self.analyses[filename] = crossings, sproutCount, sproutMax

	def generate(self):
		with open(self.output, 'w') as fh:
			writer = csv.writer(fh)

			writer.writerow(['Overview'])
			for filename, data in self.analyses.items():
				crossings, sproutCount, sproutMax = data
				writer.writerow([filename])
				writer.writerow(['Sprout Count', sproutCount])
				writer.writerow(['Sprout Max', sproutMax])
				writer.writerow([])

			for filename, data in self.analyses.items():
				crossings, sproutCount, sproutMax = data
				writer.writerow([filename])
				writer.writerow(['Radius'] + crossings.keys())
				writer.writerow(['Crossings'] + crossings.values())
				writer.writerow([])
