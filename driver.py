from SimpleCV import Image
from sproutogram.experiments.extractor import *
from sproutogram.experiments.naive_analysis import NaiveAnalysisExperiment
from sproutogram.experiments.noise_analysis import NoiseAnalysis

from multiprocessing import Pool
import numpy as np


def concurrent_extract(task):
    task.extract()


class Driver(object):
    """
    Drives premade sets of extraction tasks
    """
    @staticmethod
    def extract_selected():
        in_path = 'data/drug'
        report_path = 'data/drug_report'
        AveragedExtraction(in_path=in_path, out_path=in_path, report_path=report_path, bead_factor=1.2).extract()

    @staticmethod
    def extract_batch():
        in_path = 'data/samples/selected'
        report_path = 'data/reports/'
        pool = Pool(4)
        tasks = []
        for i in np.arange(1.5, 3.1, 0.1):
            tasks.append(AveragedExtraction(in_path, in_path, report_path, i))
        # for i in np.arange(1.5, 3.1, 0.1):
        #   tasks.append(ThresholdAverageExtractionTask(in_path, in_path, report_path, i))
        # for i in np.arange(1.5, 3.1, 0.1):
        #   tasks.append(MedianIntegrationExtractionTask(in_path, in_path, report_path, i))
        # for i in np.arange(1.5, 3.1, 0.1):
        #     tasks.append(ThresholdMedianIntegrationExtractionTask(in_path, in_path, report_path, i))
        pool.map(concurrent_extract, tasks)


if __name__ == '__main__':
    Driver.extract_selected()
    # experiment = NaiveAnalysisExperiment(img=Image('data/samples/mono.jpg'))
    # experiment.execute()