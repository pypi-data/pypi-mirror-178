from typing import Any
import importlib.util
import sys
import os
import logging
from importlib.metadata import version

PACKAGES_HAVE_BEEN_CHECKED = False


def check_python(logger: logging.Logger) -> None:
    """
    This function checks that the python version in use is 3+.

    Args:
        logger: logs the package check
    """
    if sys.version_info[0] == 3:
        if sys.version_info[1] >= 9:
            print(f"\033[92m\u2714\033[0m Python version ", end="")
            print(f"{sys.version_info[0]}.{sys.version_info[1]}", end="")
            print(f".{sys.version_info[2]}")
            logger.info(
                f"\033[92m\u2714\033[0m Python version "
                f"{sys.version_info[0]}.{sys.version_info[1]}"
                f".{sys.version_info[2]}"
            )
        else:
            print(
                f"you are using python{sys.version_info[0]}" f".{sys.version_info[1]}"
            )
            print(f"this code was tested with python 3.9.7")
            print(f"you might need to upgrade your version")
            logger.info(
                f"you are using python{sys.version_info[0]}" f".{sys.version_info[1]}"
            )
            logger.info(f"this code was tested with python 3.9.7")
            logger.info(f"you might need to upgrade your version")
    else:
        print(f"you are using python{sys.version_info[0]}")
        print(f"this code only works in python 3")
        logger.info(f"you are using python{sys.version_info[0]}")
        logger.info(f"this code only works in python 3")


def check_if_a_module_exists(module_name: str) -> bool:
    """
    This function checks if a module can be loaded
    """
    if module_name in sys.modules:
        return True
    elif (importlib.util.find_spec(module_name)) is not None:
        return True
    else:
        return False


def check_module_version(module_name: str) -> Any:
    """
    This function gets the version of a module

    Args:
        module_name: name of the python module to check
    """
    if check_if_a_module_exists(module_name=module_name):
        if module_name == "batch_normalization_folding":
            return version("tensorflow-batchnorm-folding")
        module = importlib.import_module(module_name)
        if module_name == "dotenv":
            return "0.20.0"
        elif module_name == "pynput":
            import pynput

            module_spec = importlib.util.spec_from_file_location(
                "_info", os.path.join(os.path.dirname(pynput.__file__), "_info.py")
            )
            version_module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(version_module)
            version_tuple = version_module.__version__
            return f"{version_tuple[0]}.{version_tuple[1]}.{version_tuple[2]}"
        elif module_name == "nvidia_smi":
            return "7.352.0"
        elif module_name == "official":
            return "2.9.2"
        return module.__version__
    return None


def create_model_folder() -> None:
    """
    This functions creates a folder where we can save the quantized models
    """
    if "quantized_models" not in os.listdir(".."):
        os.mkdir("../quantized_models")


def compare_versions(v1, v2) -> bool:
    """
    This function comapres two versions, usual use consist in
    ensuring that a module has a satisfactory version for stable use

    Args:
        module_name: name of the python module to check
    """
    if v1 is None:
        return False
    if v1[0] > v2[0]:
        return True
    elif v1[0] == v2[0]:
        if v1[1] > v2[1]:
            return True
        elif v1[1] == v2[1]:
            if v1[2] >= v2[2]:
                return True
    return False


def check_packages(logger: logging.Logger) -> None:
    """
    checks that all the required packages are installed

    Args:
        logger: logs the package check
    """
    global PACKAGES_HAVE_BEEN_CHECKED
    if not PACKAGES_HAVE_BEEN_CHECKED:
        print()

        check_python(logger=logger)
        module_v_int = []
        module_v_str = []
        pip_commands = [
            "pip install --upgrade pynput",
        ]
        missing_modules = False
        packages_to_check = ["pynput"]
        recommended_version = [(1, 7, 0)]
        for package in packages_to_check:
            module_version = check_module_version(module_name=package)
            if module_version is None:
                module_v_int.append(None)
                module_v_str.append("-")
                missing_modules = True
            else:
                module_v_str.append(module_version)
                module_v_int.append([int(e) for e in module_version.split(".")])

        pip_commands_to_run = []
        column_0 = ["package"]
        column_1 = ["current version"]
        column_2 = ["recommended version"]
        column_3 = ["checks"]
        for (version, v_str, reco_version, pip_command, name) in zip(
            module_v_int,
            module_v_str,
            recommended_version,
            pip_commands,
            packages_to_check,
        ):
            if compare_versions(version, reco_version):
                column_3.append("\u2714")
            else:
                column_3.append("\u2717")
                pip_commands_to_run.append(pip_command)
            column_2.append(f"{reco_version[0]}.{reco_version[1]}.{reco_version[2]}")
            column_1.append(v_str)
            column_0.append(name)

        l0 = len(max(column_0, key=len))
        l1 = len(max(column_1, key=len))
        l2 = len(max(column_2, key=len))
        l3 = len(max(column_3, key=len))
        limiter = "+" + (l0 + l1 + l2 + l3 + 11) * "-" + "+"
        print(limiter)
        logger.info(limiter)
        for cpt, (s0, s1, s2, s3) in enumerate(
            zip(column_0, column_1, column_2, column_3)
        ):
            if cpt == 0:
                color = "\033[1m"
                end_c = "\033[0m"
                color_ = ""
                end_c_ = ""
                assert_color = ""
                assert_end_c = ""
            else:
                color = ""
                end_c = ""
                color_ = "\033[4m"
                end_c_ = "\033[0m"
                assert_color = "\033[92m"
                if s3 == "\u2717":
                    assert_color = "\033[91m"
                assert_end_c = "\033[0m"
            print(
                f"| {color}{s0.center(l0)}{end_c} | {color}{s1.center(l1)}{end_c} "
                f"| {color}{(color_ + s2 + end_c_).center(l2 + len(end_c_) + len(color_))}{end_c} "
                f"| {assert_color}{color}{s3.center(l3)}{end_c}{assert_end_c} |"
            )
            logger.info(
                f"| {color}{s0.center(l0)}{end_c} | {color}{s1.center(l1)}{end_c} "
                f"| {color}{(color_ + s2 + end_c_).center(l2 + len(end_c_) + len(color_))}{end_c} "
                f"| {assert_color}{color}{s3.center(l3)}{end_c}{assert_end_c} |"
            )
        print(limiter)
        logger.info(limiter)

        PACKAGES_HAVE_BEEN_CHECKED = True
        if len(pip_commands_to_run) != 0:
            print("to install/upgrade missing dependencies please use:")
            logger.info("to install/upgrade missing dependencies please use:\n")
            for pip in pip_commands_to_run:
                print(f"\t{pip}")
                logger.info(f"\t{pip}")
        if missing_modules:
            sys.exit()


if __name__ == "__main__":
    check_packages()
