from sproutogram.experiments.extractor import *

from multiprocessing import Pool
import numpy as np

import os


DATA_DIR = "data"
RESULT_DIR = "result"


def extract_selection(selection):
    data_path = os.path.join(DATA_DIR, selection)
    result_path = os.path.join(RESULT_DIR, selection)
    AveragedExtraction(data_path=data_path, result_path=result_path, bead_factor=1.2).extract()

def extract_batch():
    data_path = 'data/samples/selected'
    result_path = 'data/reports/'
    pool = Pool(4)
    tasks = []
    for i in np.arange(1.5, 3.1, 0.1):
        tasks.append(AveragedExtraction(data_path, result_path, i))
    # for i in np.arange(1.5, 3.1, 0.1):
    #   tasks.append(ThresholdAverageExtractionTask(data_path, result_path, i))
    # for i in np.arange(1.5, 3.1, 0.1):
    #   tasks.append(MedianIntegrationExtractionTask(data_path, result_path, i))
    # for i in np.arange(1.5, 3.1, 0.1):
    #     tasks.append(ThresholdMedianIntegrationExtractionTask(data_path, result_path, i))
    pool.map(concurrent_extract, tasks)


def list_datasets():
    datasets = sorted(
        name 
        for name in os.listdir(DATA_DIR) 
        if os.path.isdir(os.path.join(DATA_DIR, name))
    )
    return datasets


def select_dataset(datasets):
    for index, name in enumerate(datasets):
        print("({}) {}".format(index, name)) 
    selection = int(input("Please select a dataset: "))
    return datasets[selection]


if __name__ == '__main__':
    datasets = list_datasets()
    selection = select_dataset(datasets)
    extract_selection(selection)
