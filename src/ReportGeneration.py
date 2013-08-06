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
		"""Generates the report as CSV."""
		pass


class ShollAnalysisReport(ReportGeneratorBase):
	"""
	Generates reports given a Sholl Analysis of an angiogram. The report
	includes the primary sprout count, maximum sprout count raw data dump of
	the analysis.
	"""
	def __init__(self, filename):
		super(ShollAnalysisReport, self).__init__(filename)

	def addAnalysis(self, filename, analysis):
		"""
		Appends an analysis of the specified filename to the report.

		:param filename: name of the file analyzed
		:param analysis: analysis of the file
		"""
		self.analyses[filename] = analysis

	def generate(self):
		with open(self.output, 'w') as fh:
			writer = csv.writer(fh)

			writer.writerow(['Overview'])
			sortedItems = sorted(self.analyses.items())
			for filename, analysis in sortedItems:
				writer.writerow([filename])
				writer.writerow(['Sprout Count', analysis.sproutCount])
				writer.writerow(['Critical Value', analysis.criticalValue])
				writer.writerow(['Sprout Maximum', analysis.sproutMaximum])
				writer.writerow(['Shoenen Ramification Index', '%.2f' % analysis.ramificationIndex])
				writer.writerow([])

			for filename, analysis in sortedItems:
				writer.writerow([filename])
				writer.writerow(['Radius'] + analysis.crossings.keys())
				writer.writerow(['Crossings'] + analysis.crossings.values())
				writer.writerow([])
