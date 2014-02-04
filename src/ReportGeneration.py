from training import HumanCounts
import csv
import math
import sqlite3
import pickle


class ReportGeneratorBase(object):
    """
    Abstract base class for generating reports as CSV files.
    """
    def __init__(self, filename):
        self.output = filename
        self.analyses = {}

    def add_analysis(self, filename, analysis):
        """
        Appends an analysis of the specified filename to the report.

        :param filename: name of the file analyzed
        :param analysis: analysis of the file
        """
        self.analyses[filename] = analysis

    def generate(self):
        """Generates the report."""
        pass


class CSVReportGenerator(ReportGeneratorBase):
    """
    Generates reports given a Sholl Analysis of an angiogram. The report
    includes the primary sprout count, maximum sprout count raw data dump of
    the analysis.
    """
    def __init__(self, filename):
        super(CSVReportGenerator, self).__init__(filename)

    def calculate_rmse(self, analyses):
        variance = sum(
            [(analysis.sproutCount - HumanCounts.data[filename].focusCounts) ** 2
                for filename, analysis in analyses])
        return math.sqrt(variance / float(len(HumanCounts.data)))

    def calculate_branching_count_rmse(self, analyses):
        variance = sum(
            [(analysis.branchingCount - HumanCounts.data[filename].branchingCount) ** 2
                for filename, analysis in analyses])
        return math.sqrt(variance / float(len(HumanCounts.data)))

    def generate(self):
        with open(self.output, 'w') as fh:
            sorted_items = sorted(self.analyses.items())
            sprount_count_rmse = self.calculate_rmse(sorted_items)
            branching_count_rmse = self.calculate_branching_count_rmse(sorted_items)
            writer = csv.writer(fh)

            writer.writerow(['Overview'])
            writer.writerow(['Sprout Count RMSE: ', sprount_count_rmse])
            writer.writerow(['Branching Count RMSE: ', branching_count_rmse])
            # print 'Sprout Count RMSE: ', sproutCountRMSE
            # print 'Branching Count RMSE: ', branchingCountRMSE

            for filename, analysis in sorted_items:
                writer.writerow([filename])
                writer.writerow(['Sprout Count', analysis.sproutCount])
                writer.writerow(['Critical Value', analysis.criticalValue])
                writer.writerow(['Sprout Maximum', analysis.sproutMaximum])
                writer.writerow(['Shoenen Ramification Index', '%.2f' % analysis.ramificationIndex])
                writer.writerow(['Branching Count', '%.2f' % analysis.branchingCount])
                writer.writerow([])

            for filename, analysis in sorted_items:
                writer.writerow([filename])
                writer.writerow(['Radius'] + analysis.crossings.keys())
                writer.writerow(['Crossings'] + analysis.crossings.values())
                writer.writerow([])


class DBReportGenerator(CSVReportGenerator):
    def __init__(self, dbfilename, method):
        super(DBReportGenerator, self).__init__(dbfilename)
        self.method = method

    def generate(self):
        with sqlite3.connect(self.output) as conn:
            cur = conn.cursor()
            sorted_items = sorted(self.analyses.items())

            for filename, analysis in sorted_items:
                cur.execute("INSERT OR IGNORE INTO feature VALUES ('{0:s}', '{1:s}', '{2:.2f}', '{3:.2f}', '{4:.2f}', '{5:.2f}', '{6:.2f}', '{7:.2f}')"
                            .format(self.method, filename, analysis.sproutCount,
                            analysis.criticalValue, analysis.sproutMaximum,
                            analysis.ramificationIndex, analysis.branchingCount, analysis.trocAverage))

            for filename, analysis in sorted_items:
                cur.execute("INSERT OR IGNORE INTO sholl_analysis VALUES ('{0:s}', '{1:s}')"
                            .format(filename, pickle.dumps(analysis.crossings)))
