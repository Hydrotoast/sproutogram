from sproutogram.experiments.extractor import *

import os


DATA_DIR = "data"
RESULT_DIR = "result"


def extract_dataset(dataset):
    """Performs extraction on the specified dataset."""
    data_path = os.path.join(DATA_DIR, dataset)
    result_path = os.path.join(RESULT_DIR, dataset)

    print("Data Path: {}".format(data_path))
    print("Result Path: {}".format(result_path))

    AveragedExtraction(data_path=data_path,
                       result_path=result_path,
                       bead_factor=1.5,
                       canny_min=40,
                       canny_max=120).extract()


def list_datasets():
    """Returns a sorted list of datasets available."""
    datasets = []
    for name in os.listdir(DATA_DIR):
        if os.path.isdir(os.path.join(DATA_DIR, name)):
            datasets.append(name)
    return sorted(datasets)


def show_candidates(datasets):
    """Shows a list of the candidate datasets."""
    for index, name in enumerate(datasets):
        print("({}) {}".format(index, name))


def validate_selection(datasets, selection):
    """Validates the user selection and returns a valid selection."""
    if selection not in range(len(datasets)):
        print("Invalid selection. Please try again.\n")
        return select_dataset(datasets)
    return datasets[selection]


def select_dataset(datasets):
    """Prompts the user to select a dataset from the collection of datasets."""
    print("Datasets available")
    show_candidates(datasets)
    selection = int(input("Please select a dataset: "))
    return validate_selection(datasets, selection)


def main():
    datasets = list_datasets()
    dataset = select_dataset(datasets)
    extract_dataset(dataset)


if __name__ == '__main__':
    main()