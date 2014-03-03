from .repositories import session, TrainData
import csv
import math
import sqlite3
import pickle


def calculate_rmse(analyses):
    train_data = session.query(TrainData).all()
    human_counts = dict(zip(map(lambda train_datum: train_datum.filename, train_data), train_data))
    variance = sum(
        [(analysis.sprout_count - human_counts[filename].focus_sprout_count) ** 2
         for filename, analysis in analyses])
    return math.sqrt(variance / float(len(human_counts)))


def calculate_branching_count_rmse(analyses):
    train_data = session.query(TrainData).all()
    human_counts = dict(zip(map(lambda train_datum: train_datum.filename, train_data), train_data))
    variance = sum(
        [(analysis.auxiliary_branch_count - human_counts[filename].auxiliary_branch_count) ** 2
         for filename, analysis in analyses])
    return math.sqrt(variance / float(len(human_counts)))


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

    def generate(self):
        with open(self.output, 'w') as fh:
            sorted_items = sorted(self.analyses.items())
            sprount_count_rmse = calculate_rmse(sorted_items)
            auxiliary_branch_count_rmse = calculate_branching_count_rmse(sorted_items)
            writer = csv.writer(fh)

            writer.writerow(['Overview'])
            writer.writerow(['Sprout Count RMSE: ', sprount_count_rmse])
            writer.writerow(['Branching Count RMSE: ', auxiliary_branch_count_rmse])

            for filename, analysis in sorted_items:
                writer.writerow([filename])
                writer.writerow(['Sprout Count', analysis.sprout_count])
                writer.writerow(['Critical Value', analysis.critical_value])
                writer.writerow(['Total Branch Count', analysis.total_branch_count])
                writer.writerow(['Branching Factor', '%.2f' % analysis.branching_factor])
                writer.writerow(['Auxiliary Branch Count', '%.2f' % analysis.auxiliary_branch_count])
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
                            .format(self.method, filename, analysis.sprout_count,
                            analysis.critical_value, analysis.sprout_maximum,
                            analysis.ramification_index, analysis.branching_count, analysis.troc_average))

            for filename, analysis in sorted_items:
                cur.execute("INSERT OR IGNORE INTO sholl_analysis VALUES ('{0:s}', '{1:s}')"
                            .format(filename, pickle.dumps(analysis.crossings)))
