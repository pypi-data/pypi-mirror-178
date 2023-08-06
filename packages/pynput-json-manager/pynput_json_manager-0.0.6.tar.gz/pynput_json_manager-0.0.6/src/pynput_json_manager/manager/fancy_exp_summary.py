from typing import Any, Dict, List
import numpy as np
import json
import os


class ExpSummarizer:
    def __init__(self) -> None:
        with open(os.path.join(os.path.dirname(__file__), "shortcuts.json"), "r") as f:
            self.shortcuts_names = {value: key for key, value in json.load(f).items()}

    def get_columns(self, exp_data: Dict[str, Any]) -> List[List[str]]:
        """
        creates the columns which are each a list of strings
        """
        column1 = ["parameter"]
        column2 = ["value"]
        for key, value in exp_data.items():
            if key in self.shortcuts_names:
                column1.append(self.shortcuts_names[key])
            else:
                column1.append(key)
            if isinstance(value, bool):
                if value:
                    value = "\u2714"
                else:
                    value = "\u2717"
            column2.append(str(value))
        return (column1, column2)

    def get_widths(self, columns: List[List[str]]) -> List[int]:
        widths = []
        for column in columns:
            max_width = 0
            for value in column:
                max_width = max(max_width, len(value))
            widths.append(max_width)
        return widths

    def printer(self, columns: List[List[str]], widths: List[int]) -> None:
        content = []
        for cpt_col, column in enumerate(columns):
            tmp = []
            for _, value in enumerate(column):
                if "cifar" in value.lower():
                    tmp.append(
                        "\033[94m"
                        + f"{value.lower()}".center(widths[cpt_col])
                        + "\033[0m"
                    )
                elif "imagenet" in value.lower():
                    tmp.append(
                        "\033[96m"
                        + f"{value.lower()}".center(widths[cpt_col])
                        + "\033[0m"
                    )
                elif "glue" in value.lower():
                    tmp.append(
                        "\033[95m"
                        + f"{value.lower()}".center(widths[cpt_col])
                        + "\033[0m"
                    )
                elif "\u2714" in value.lower():
                    tmp.append(
                        "\033[92m" + "\u2714".center(widths[cpt_col]) + "\033[0m"
                    )
                elif "\u2717" in value.lower():
                    tmp.append(
                        "\033[91m" + "\u2717".center(widths[cpt_col]) + "\033[0m"
                    )
                else:
                    tmp.append(value.center(widths[cpt_col]))
            content.append(tmp)
        print("+" + "-" * (np.sum(widths) + 5) + "+")
        print("| " + "current experiment summary".center(np.sum(widths) + 3) + " |")
        print("+" + "-" * (np.sum(widths) + 5) + "+")
        for cpt in range(len(content[0])):
            print(f"| {content[0][cpt]} | {content[1][cpt]} |")
            if cpt == 0:
                print("+" + "-" * (np.sum(widths) + 5) + "+")
        print("+" + "-" * (np.sum(widths) + 5) + "+")

    def __call__(self, exp_data: Dict[str, Any], *args: Any, **kwds: Any) -> Any:
        columns = self.get_columns(exp_data=exp_data)
        widths = self.get_widths(columns=columns)
        self.printer(columns=columns, widths=widths)
