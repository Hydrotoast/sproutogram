from sproutogram.experiments.extractor import *

import os


DATA_DIR = "data"
RESULT_DIR = "result"


def extract_dataset(dataset):
    data_path = os.path.join(DATA_DIR, dataset)
    result_path = os.path.join(RESULT_DIR, dataset)
    AveragedExtraction(data_path=data_path, result_path=result_path, bead_factor=1.5).extract()


def list_datasets():
    datasets = sorted(
        name 
        for name in os.listdir(DATA_DIR) 
        if os.path.isdir(os.path.join(DATA_DIR, name))
    )
    return datasets


def select_dataset(datasets):
    print("Datasets available")
    candidates = []
    for index, name in enumerate(datasets):
        candidates.append(index)
        print("({}) {}".format(index, name)) 
    selection = int(input("Please select a dataset: "))

    # Validation
    if selection not in candidates:
        print("Invalid selection. Please try again.\n")
        return select_dataset(datasets)

    return datasets[selection]


if __name__ == '__main__':
    datasets = list_datasets()
    dataset = select_dataset(datasets)
    extract_dataset(dataset)
