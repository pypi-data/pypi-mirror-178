import os
import json
from typing import Any, Dict, Tuple
from pynput.keyboard import Key, Listener
from .setup_reader import ExperimentsToRun
import sys


current_key = None


def on_press(key):
    pass


def on_release(key):
    global current_key
    current_key = key
    return False


class fancy_generator:
    def __init__(self, path_to_jsons: str, path_to_information: str) -> None:
        self.pressed_enter = False
        self.path_to_jsons = path_to_jsons
        self.path_to_information = path_to_information
        self.ExperimentReader = ExperimentsToRun(
            path_to_jsons=path_to_jsons, verbose=False
        )
        self.ExperimentReader.get_current_state()
        if len(self.ExperimentReader.jsons_to_read) == 0:
            self.last_experiment_data = None
        else:
            self.last_experiment_data = (
                self.ExperimentReader.last_experiment_data.copy()
            )
        with open(
            os.path.join(self.path_to_information, "general_information_keys.json"), "r"
        ) as f:
            self.keys = json.load(f)["keys"][2:]
        with open(
            os.path.join(self.path_to_information, "possible_values.json"), "r"
        ) as f:
            self.possible_str = {
                key: value for key, value in json.load(f).items() if key in self.keys
            }
        with open(os.path.join(self.path_to_information, "type_of.json"), "r") as f:
            self.types = {
                key: value for key, value in json.load(f).items() if key in self.keys
            }
        with open(
            os.path.join(self.path_to_information, "default_values.json"), "r"
        ) as f:
            self.defaults = {
                key: value for key, value in json.load(f).items() if key in self.keys
            }
        with open(os.path.join(self.path_to_information, "precision.json"), "r") as f:
            self.float_values_precision = {
                key: value for key, value in json.load(f).items() if key in self.keys
            }

    def get_current_values(
        self, key: str, current_option: int, modifier: int, highlight: bool = False
    ) -> Tuple[str, Any]:
        if highlight:
            marker1 = "["
            marker2 = "]"
        else:
            marker1 = ""
            marker2 = ""
        if key in self.possible_str:
            option_str = (
                f"{self.possible_str[key][(current_option - 1) % len(self.possible_str[key])]}"
                f"    {marker1}\033[1m{self.possible_str[key][current_option % len(self.possible_str[key])]}\033[0m{marker2}"
                f"   {self.possible_str[key][(current_option + 1) % len(self.possible_str[key])]}"
            )
            option_value = self.possible_str[key][
                current_option % len(self.possible_str[key])
            ]
        elif key in self.types:
            if self.types[key] == "bool":
                if current_option % 2 == 1:
                    option_str = f"False    {marker1}\033[1mTrue\033[0m{marker2}"
                else:
                    option_str = f"{marker1}\033[1mFalse\033[0m{marker2}    True"
                option_value = current_option % 2 == 1
            elif self.types[key] == "int":
                option_value = int(self.defaults[key]) + modifier
                option_str = f"{marker1}\033[1m{option_value}\033[0m{marker2}"
            elif self.types[key] == "float":
                option_value = float(self.defaults[key]) + modifier * float(
                    self.float_values_precision[key]
                )
                option_str = f"{marker1}\033[1m{option_value}\033[0m{marker2}"
            else:
                option_str = "to do"
        return option_str, option_value

    def handle_a_key(
        self, key: str, initial_option: int = 0, intial_modifier: int = 0
    ) -> Tuple[Any, str, int, int]:
        base_request = f"\rPlease provide {key}".ljust(60)
        current_option = initial_option
        modifier = intial_modifier
        typed_value = ""
        if self.pressed_enter:
            option_str, option_value = self.get_current_values(
                key=key,
                current_option=current_option,
                modifier=modifier,
                highlight=True,
            )
            print(base_request + str(option_value) + " " * len(option_str))
            last_string = base_request + str(option_value) + " " * len(option_str)
        while not self.pressed_enter:
            if typed_value == "":
                option_str, option_value = self.get_current_values(
                    key=key,
                    current_option=current_option,
                    modifier=modifier,
                    highlight=True,
                )
            else:
                option_str = typed_value
                if self.types[key] == "int":
                    option_value = int(typed_value)
                elif self.types[key] == "float":
                    option_value = float(typed_value)
            print(base_request + option_str, end="")

            with Listener(on_press=on_press, on_release=on_release) as listener:
                a = listener.join()
            if current_key == Key.shift or current_key == Key.shift_r:
                pass
            elif current_key == Key.backspace:
                if len(typed_value) > 0:
                    typed_value = typed_value[:-1]
            elif current_key == Key.enter or current_key == Key.down:
                if typed_value == "":
                    option_str, option_value = self.get_current_values(
                        key=key,
                        current_option=current_option,
                        modifier=modifier,
                        highlight=True,
                    )
                else:
                    option_str = typed_value + " " * 5
                    if self.types[key] == "int":
                        option_value = int(typed_value)
                    elif self.types[key] == "float":
                        option_value = float(typed_value)
                if key in self.types:
                    if self.types[key] == "float":
                        print(
                            base_request + f"{option_value:.2f}" + " " * len(option_str)
                        )
                        last_string = (
                            base_request + f"{option_value:.2f}" + " " * len(option_str)
                        )
                    else:
                        print(base_request + str(option_value) + " " * len(option_str))
                        last_string = (
                            base_request + str(option_value) + " " * len(option_str)
                        )
                else:
                    print(base_request + str(option_value) + " " * len(option_str))
                    last_string = (
                        base_request + str(option_value) + " " * len(option_str)
                    )
                if current_key == Key.enter:
                    self.pressed_enter = True
                break
            elif current_key == Key.right:
                current_option += 1
                modifier += 1
            elif current_key == Key.left:
                current_option += -1
                modifier += -1
            elif current_key == Key.up:
                return None, None, None, None
            elif current_key == Key.space and key in self.types:
                if "int" == self.types[key]:
                    modifier = -int(self.defaults[key])
            elif (
                current_key.char
                in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]
                and key in self.types
            ):
                if "int" == self.types[key]:
                    typed_value += current_key.char
                    option_str = typed_value
                    modifier = int(typed_value) - int(self.defaults[key])
                if "float" == self.types[key]:
                    typed_value += current_key.char
                    option_str = typed_value
                    modifier = (float(typed_value) - float(self.defaults[key])) / float(
                        self.float_values_precision[key]
                    )
            print(base_request + option_str + "    ", end="")
        if key in self.possible_str:
            selected_option = current_option % len(self.possible_str[key])
            modifier = 0
        elif self.types[key] == "bool":
            selected_option = int(option_value)
            modifier = 0
        else:
            selected_option = 0
        return option_value, last_string, selected_option, modifier

    def clear_line(self, l: int):
        blank = " " * l * 2
        print(f"\r{blank}\033[A\r", end="")

    def get_modifiers_options(self) -> Tuple[Dict[int, int]]:
        cpt = 0
        modifiers = {key: 0 for key in self.keys}
        options_selected = {key: 0 for key in self.keys}
        if self.last_experiment_data is None:
            return modifiers, options_selected
        while cpt < len(self.keys):
            key = self.keys[cpt]
            previous_value = self.last_experiment_data[key]
            if previous_value == "-":
                previous_value = self.defaults[key]
            if key in self.possible_str:
                options_selected[key] = self.possible_str[key].index(previous_value)
            elif "int" == self.types[key]:
                modifiers[key] = int(previous_value) - int(self.defaults[key])
            elif "float" == self.types[key]:
                modifiers[key] = (
                    float(previous_value) - float(self.defaults[key])
                ) / float(self.float_values_precision[key])
            elif "bool" == self.types[key]:
                if self.last_experiment_data[key] == "-":
                    self.last_experiment_data[key] = self.defaults[key] == "true"
                options_selected[key] = int(self.last_experiment_data[key])

            cpt += 1
        return modifiers, options_selected

    def build_exp(self) -> Dict[str, Any]:
        new_exp = {"experiment is running": False, "experiment is done": False}
        cpt = 0
        lines_length = {}
        modifiers, options_selected = self.get_modifiers_options()
        while cpt < len(self.keys):
            if cpt < 0:
                cpt = 0
            key = self.keys[cpt]
            if key == "model .h5 file name":
                initial_option = options_selected[self.keys[cpt - 1]]
            elif key in options_selected:
                initial_option = options_selected[key]
            else:
                initial_option = 0
            intial_modifier = modifiers[key]
            value, last_string, selected_option, modifier = self.handle_a_key(
                key=key, initial_option=initial_option, intial_modifier=intial_modifier
            )
            if value is not None:
                lines_length[cpt] = len(last_string)
                new_exp[key] = value
                options_selected[key] = selected_option
                modifiers[key] = modifier
                cpt += 1
            else:
                cpt -= 1
                if cpt >= 0:
                    self.clear_line(l=lines_length[cpt])
        return new_exp

    def __call__(self, path: str, *args: Any, **kwds: Any) -> Any:
        self.pressed_enter = False
        new_exp = self.build_exp()
        with open(os.path.join(self.path_to_jsons, path), "w") as json_file:
            json.dump(new_exp, json_file)


if __name__ == "__main__":
    fancy_generator(path_to_jsons="../experiments_jsons")("test.json")
