import json
import sys
import os
from typing import Dict, Any
from experimental_setup.parameters_information import (
    general_information_keys,
    type_of,
    default_values,
)


class ExperimentGenerator:
    def __init__(self, path_to_jsons: str) -> None:
        self.path_to_jsons = path_to_jsons

    def save_data(self, path: str, data: Dict[str, Any]) -> None:
        """
        saves the newly created experiment
        """
        with open(os.path.join(self.path_to_jsons, path), "w") as json_file:
            json.dump(data, json_file)

    def ask_for_a_key(self, key: str) -> Any:
        """
        prompts the correct question with regards to the key
        """
        question = f"Please provide {key}".ljust(45)
        question += f"({default_values[key]})".rjust(15)
        usr_input = input(f"{question}:")
        if usr_input == "":
            usr_input = default_values[key]
        return usr_input

    def convert_key(self, key: str, a: str) -> Any:
        """
        converts the provided input to the expected type
        """
        if key not in type_of:
            return a
        try:
            if type_of[key] is bool:
                return a.lower() == "true"
            return type_of[key](a)
        except ValueError:
            print(f"ValueError: Please enter an {type_of[key]} for key {key}")
            sys.exit()

    def add_specific_information(
        self, data: Dict[str, Any], keys: list
    ) -> Dict[str, Any]:
        """
        adds quantization information
        """
        for key in keys:
            if key in ["experiment is running", "experiment is done"]:
                data[key] = False
            else:
                data[key] = self.convert_key(key=key, a=self.ask_for_a_key(key=key))
        return data

    def print_howto(self) -> None:
        """
        prints instructions
        """
        print("+" + "-" * 63 + "+")
        print(
            "| "
            + f"Instructions to generate a json file for QAT experimentation:".ljust(61)
            + " |"
        )
        print(
            "| "
            + f" 1. we will ask you for detailed informations regarding ".ljust(61)
            + " |"
        )
        print(
            "| "
            + f"    the quantization process, the dataset and model.".ljust(61)
            + " |"
        )
        print(
            "| "
            + f" 2. default values are specified in parenthesis but are not ".ljust(61)
            + " |"
        )
        print("| " + f"    a recommandation.".ljust(61) + " |")
        print(
            "| " + f" 3. to select a default value please press ENTER.".ljust(61) + " |"
        )
        print(
            "| "
            + f" 4. the json file will be the added in experiments_jsons".ljust(61)
            + " |"
        )
        print("| " + f" 5. results will also be storedi n that json".ljust(61) + " |")
        print(
            "| "
            + f" 6. it is automatically named with the last and highest value".ljust(61)
            + " |"
        )
        print(
            "| "
            + f"For any more information please contact ey@datakalab.com".ljust(61)
            + " |"
        )
        print("+" + "-" * 63 + "+")

    def __call__(self, path: str, *args: Any, **kwds: Any) -> Any:
        self.print_howto()
        data = {}
        data = self.add_specific_information(data=data, keys=general_information_keys)

        self.save_data(path=path, data=data)
