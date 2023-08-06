import json
import os
from typing import Any, Dict, Tuple


class ExperimentsToRun:
    def __init__(self, path_to_jsons: str, verbose: bool = True) -> None:
        self.path_to_jsons = path_to_jsons
        if not os.path.isdir(self.path_to_jsons):
            raise ValueError("path_to_jsons should be a directory but is not")
        if verbose:
            self.get_current_state()

    def __len__(self):
        return len(self.upcoming_experiments)

    def collect_all_experiments(self) -> list:
        json_list = []
        for file in sorted(os.listdir(self.path_to_jsons)):
            if ".json" in file:
                json_list.append(os.path.join(self.path_to_jsons, file))
        return json_list

    def read_json(self, path: str) -> Dict[Any, Any]:
        """
        extracts data from json
        """
        with open(path, "r") as f:
            data = json.load(f)
        return data

    def split_json_files(self) -> Tuple[list, list, list]:
        """
        splits experiments based on the fact that they are finished or not
        """
        finished_experiments = []
        running_experiments = []
        upcoming_experiments = []
        for cpt, json_path in enumerate(self.jsons_to_read):
            data = self.read_json(path=json_path)
            if data["experiment is done"]:
                finished_experiments.append(data)
            elif data["experiment is running"]:
                running_experiments.append(data)
            else:
                upcoming_experiments.append((json_path, data))
            if cpt == len(self.jsons_to_read) - 1:
                self.last_experiment_data = data
        return finished_experiments, running_experiments, upcoming_experiments

    def set_exp_as_running(self, json_path: str, data: Dict[Any, Any]):
        """
        when a data is loaded, it means that its experiment will be run.
        when the program is launched multiple times we don't want to run the same experiment
        multiple times so we indicate that it is running.
        """
        data["experiment is running"] = True
        with open(json_path, "w") as json_file:
            json.dump(data, json_file)

    def get_current_state(self):
        """
        updates the state of the experiments
        """
        self.jsons_to_read = self.collect_all_experiments()
        (
            self.finished_experiments,
            self.running_experiments,
            self.upcoming_experiments,
        ) = self.split_json_files()

    def print_current_state(self) -> None:
        """
        prints the state of the experiments
        """
        print("+" + 39 * "-" + "+")
        title = "current available experiments".center(39)
        print(f"|{title}|")
        print("+" + 39 * "-" + "+")
        col1 = "finished experiments".center(30)
        col2 = f"{len(self.finished_experiments)}".center(6)
        print(f"|{col1} | {col2}|")
        col1 = "running experiments".center(30)
        col2 = f"{len(self.running_experiments)}".center(6)
        print(f"|{col1} | {col2}|")
        col1 = "upcoming experiments".center(30)
        col2 = f"{len(self.upcoming_experiments)}".center(6)
        print(f"|{col1} | {col2}|")
        print("+" + 39 * "-" + "+")
        col1 = "total experiments".center(30)
        col2 = f"{len(self.finished_experiments)+len(self.running_experiments)+len(self.upcoming_experiments)}".center(
            6
        )
        print(f"|{col1} | {col2}|")
        print("+" + 39 * "-" + "+")

    def __call__(self, *args: Any, **kwds: Any) -> Tuple[Any, Any]:
        if len(self.upcoming_experiments) == 0:
            self.print_current_state()
            return None, None
        json_path = self.upcoming_experiments[0][0]
        data = self.upcoming_experiments[0][1].copy()
        self.set_exp_as_running(json_path=json_path, data=data)
        self.get_current_state()
        self.print_current_state()
        return data, json_path

    def get_config(self) -> Dict[str, Any]:
        """
        returns the current configuration of the experimets to run
        """
        config = {
            "path_to_jsons": self.path_to_jsons,
        }
        return config
