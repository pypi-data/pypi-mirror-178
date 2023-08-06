import json
import os
from typing import List


def reset_all_experiments(
    exp_folder: str,
    path_to_information: str = os.path.abspath(__file__),
    keys_to_reset: List[str] = ["experiment is running", "experiment is done"],
) -> None:
    """
    while debugging we may change every operations in the graph
    thus rendering every past experimental result irrelevant
    consequently, we might want to reset the exp.

    Args:
        exp_folder: path to the json files to edit
        path_to_information: path to the files that define the keys of our experiments
        keys_to_reset: list of keys to set to their default values
    """
    with open(os.path.join(path_to_information, "default_values.json"), "r") as f:
        default_values = json.load(f)
    for json_file in os.listdir(exp_folder):
        with open(os.path.join(exp_folder, json_file), "r") as f:
            data = json.load(f)
        for key in keys_to_reset:
            data[key] = default_values[key]
        with open(os.path.join(exp_folder, json_file), "w") as json_file:
            json.dump(data, json_file)
