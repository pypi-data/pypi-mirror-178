from genericpath import isdir
import numpy as np
import json
import os
from typing import Any, Dict, Tuple
from .parameter_shorcut import get_shortcut


class ExperimentalReport:
    __report_file_path__ = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "experimental_results.txt"
    )

    def __init__(self, path_to_jsons: str, path_to_information: str) -> None:
        self.path_to_jsons = path_to_jsons
        self.path_to_information = path_to_information
        self.get_all_jsons()

    def get_all_jsons(self) -> None:
        """
        collects all the path of the json files of the experiments.
        """
        if os.path.isdir(self.path_to_jsons):
            self.paths = [
                os.path.join(self.path_to_jsons, elem)
                for elem in sorted(os.listdir(self.path_to_jsons))
                if ".json" in elem
            ]
        else:
            self.paths = [self.path_to_jsons]

    def read_json(self, path: str) -> Dict[Any, Any]:
        """
        extracts data from json
        """
        with open(path, "r") as f:
            data = json.load(f)
        return data

    def extract_data(self) -> list:
        """
        for each experiment we read its json file and if the exp is done
        we add its specs and resutls to the list of results to report.
        """
        list_of_meta_data_to_report = [self.read_json(path=path) for path in self.paths]
        return list_of_meta_data_to_report

    def convert_value_to_str(self, value: Any) -> Tuple[str, int]:
        """
        convert booleans to check marks, floats to good format,...
        """
        if isinstance(value, float):
            value = f"{value:.3f}"
            value_len = len(value)
        elif isinstance(value, bool):
            if value:
                value = "\033[92m\u2714\033[0m"
            else:
                value = "\033[91m\u2717\033[0m"
            value_len = 1
        else:
            value = str(value)
            value_len = len(value)
        return value, value_len

    def extract_column_info(
        self, meta_data: list, show_results: bool
    ) -> Tuple[list, list, list]:
        """
        return headers and content per exp
        """
        headers = []
        column_width = []
        for data in meta_data:
            for key in data:
                if key not in headers:
                    if key not in ["model .h5 file name"]:
                        if not show_results:
                            if key not in ["result", "experiment date"]:
                                headers.append(key)
                                column_width.append(
                                    len(
                                        get_shortcut(
                                            key=key,
                                            path_to_information=self.path_to_information,
                                        )
                                    )
                                )
                        else:
                            headers.append(key)
                            column_width.append(
                                len(
                                    get_shortcut(
                                        key=key,
                                        path_to_information=self.path_to_information,
                                    )
                                )
                            )
        content = []
        for data in meta_data:
            row = []
            for cpt_key, key in enumerate(headers):
                if key in data:
                    value, value_len = self.convert_value_to_str(data[key])
                    row.append(value)
                    column_width[cpt_key] = max(column_width[cpt_key], value_len)
                else:
                    row.append("-")
            content.append(row)
        column_width = (np.array(column_width) + 2).tolist()
        return headers, content, column_width

    def nice_print(
        self,
        headers: list,
        content: list,
        column_width: list,
        show_exp_num: bool = False,
    ) -> str:
        """
        nice printing of the experimental results
        """
        output_str = ""
        separator = "+" + "-" * (len(column_width) - 1 + np.sum(column_width)) + "+"
        print(separator)
        output_str += separator + "\n"
        header_string = "|"
        for cpt, header in enumerate(headers):
            header_string += (
                f"{get_shortcut(key=header, path_to_information=self.path_to_information)}".center(
                    column_width[cpt]
                )
                + "|"
            )
        print(header_string)
        output_str += header_string + "\n"
        print(separator)
        output_str += separator + "\n"
        for row_number, row in enumerate(content):
            content_string = "|"
            for cpt, elem in enumerate(row):
                if "Cifar" in elem:
                    content_string += (
                        "\033[94m" + f"{elem}".center(column_width[cpt]) + "\033[0m|"
                    )
                elif "ImageNet" in elem:
                    content_string += (
                        "\033[96m" + f"{elem}".center(column_width[cpt]) + "\033[0m|"
                    )
                elif "glue" in elem.lower():
                    content_string += (
                        "\033[95m" + f"{elem}".center(column_width[cpt]) + "\033[0m|"
                    )
                elif elem in ["\033[92m\u2714\033[0m", "\033[91m\u2717\033[0m"]:
                    content_string += f"{elem}".center(column_width[cpt] + 9) + "|"
                else:
                    content_string += f"{elem}".center(column_width[cpt]) + "|"
            if show_exp_num:
                print(content_string + f" ({row_number+1})")
            else:
                print(content_string)
            output_str += content_string + "\n"
        print(separator)
        output_str += separator + "\n"
        return output_str

    def save_to_file(self, txt: str) -> None:
        """
        save as a .txt the fancy print
        """
        with open(self.__report_file_path__, "w") as f:
            f.write(txt)

    def __call__(
        self,
        save: bool = True,
        show_results: bool = True,
        show_exp_num: bool = False,
        *args: Any,
        **kwds: Any,
    ) -> Any:
        list_of_meta_data_to_report = self.extract_data()
        if len(list_of_meta_data_to_report) == 0:
            return None
        headers, content, column_width = self.extract_column_info(
            meta_data=list_of_meta_data_to_report, show_results=show_results
        )
        if save:
            self.save_to_file(
                self.nice_print(
                    headers=headers,
                    content=content,
                    column_width=column_width,
                    show_exp_num=show_exp_num,
                )
            )
        else:
            self.nice_print(
                headers=headers,
                content=content,
                column_width=column_width,
                show_exp_num=show_exp_num,
            )
