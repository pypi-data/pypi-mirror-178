import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if __name__ == "__main__":
    from typing import List, Dict, Any, Optional
    import argparse
    from .utils.clear import remove_chache_folders
    from .utils.get_logger import get_logger
    from .utils.packages import check_packages

    logger = get_logger()
    check_packages(logger=logger)
from .utils.setup_folders import folder_management
from .manager.delete_parameter import delete_a_key
from .manager.experimental_reset import reset_all_experiments
from .manager.experiments_removal import remove_exp
from .manager.results_reader import ExperimentalReport
from .manager.setup_reader import ExperimentsToRun
from .manager.update_parameters import add_new_parameter
from .manager.setup_fancy_generator import fancy_generator


def get_exp_next_name(exp_folder: str) -> int:
    """
    get the exp name of the next exp to generate

    Args:
        exp_folder: path to the json files to edit
        path_to_information: path to the files that define the keys of our experiments
    """
    return len([elem for elem in os.listdir(exp_folder) if ".json" in elem]) + 1


def delete_key_in_exps(exp_folder: str, path_to_information: str) -> None:
    """
    Given a path to the general information and the exp jsons,
    we ask which parameters to remove.

    args:
        path_to_information: path to the files that define the keys of our experiments
        exp_folder: path to the json files to edit
    """
    folder_management(exp_folder=exp_folder, path_to_information=path_to_information)
    delete_a_key(exp_folder=exp_folder, path_to_information=path_to_information)


def reset_exps(
    exp_folder: str,
    path_to_information: str,
    keys_to_reset: List[str],
) -> None:
    """
    Given a list of keys, we revert all the experiments corresponding keys to their default values.

    Args:
        exp_folder: path to the json files to edit
        path_to_information: path to the files that define the keys of our experiments
        keys_to_reset: list of keys to set to their default values
    """
    folder_management(exp_folder=exp_folder, path_to_information=path_to_information)
    reset_all_experiments(
        exp_folder=exp_folder,
        path_to_information=path_to_information,
        keys_to_reset=keys_to_reset,
    )


def delete_exps(exp_folder: str, path_to_information: str) -> None:
    """
    Recursively asks which exps to remove

    Args:
        exp_folder: path to the json files to edit
        path_to_information: path to the files that define the keys of our experiments
    """
    folder_management(exp_folder=exp_folder, path_to_information=path_to_information)
    ExperimentReporter = ExperimentalReport(
        path_to_information=path_to_information, path_to_jsons=exp_folder
    )
    ExperimentReporter(show_results=False, show_exp_num=True)
    remove_exp(exp_paths=ExperimentReporter.paths)


def create_exp(exp_folder: str, path_to_information: str):
    """
    generates a new experiment

    Args:
        exp_folder: path to the json files to edit
        path_to_information: path to the files that define the keys of our experiments
    """
    folder_management(exp_folder=exp_folder, path_to_information=path_to_information)
    ExperimentReporter = ExperimentalReport(
        path_to_information=path_to_information, path_to_jsons=exp_folder
    )
    ExperimentReporter(show_results=False)

    generator = fancy_generator(
        path_to_jsons=exp_folder, path_to_information=path_to_information
    )
    exp_id = f"{get_exp_next_name(exp_folder=exp_folder)}".zfill(4)
    generator(path=f"exp{exp_id}.json")


def fancy_exp_summary(
    exp_folder: str, path_to_information: str, report: bool = False
) -> Optional[Dict[str, Any]]:
    """
    fancy print of next exp to run config and returns it. Or if report is set to true,
    simple report a summary of the experiments done.

     Args:
        exp_folder: path to the json files to edit
        path_to_information: path to the files that define the keys of our experiments
        report: bool for exectuion mode
    """
    folder_management(exp_folder=exp_folder, path_to_information=path_to_information)
    if report:
        ExperimentReporter = ExperimentalReport(
            path_to_information=path_to_information, path_to_jsons=exp_folder
        )
        ExperimentReporter()
        return None
    else:
        ExperimentReader = ExperimentsToRun(path_to_jsons=exp_folder)
        experiment_data, _ = ExperimentReader()
        if experiment_data is None:
            raise RuntimeError("no experiments to run")
        else:
            from manager.fancy_exp_summary import ExpSummarizer

            fancy_summarizer = ExpSummarizer()
            fancy_summarizer(exp_data=experiment_data)
        return experiment_data


def get_status(exp_folder: str, path_to_information: str) -> None:
    """
    prints the current status of the experiments json

     Args:
        exp_folder: path to the json files to edit
    """
    folder_management(exp_folder=exp_folder, path_to_information=path_to_information)
    ExperimentReporter = ExperimentalReport(
        path_to_information=path_to_information, path_to_jsons=exp_folder
    )
    ExperimentReporter()


def add_parameters_to_exps(exp_folder: str, path_to_information: str) -> None:
    """
    Adds more parameters option

    Args:
        exp_folder: path to the json files to edit
        path_to_information: path to the files that define the keys of our experiments
    """
    folder_management(exp_folder=exp_folder, path_to_information=path_to_information)
    add_new_parameter(exp_folder=exp_folder, path_to_information=path_to_information)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        usage=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--status",
        action="store_true",
        default=False,
        help="get experiments status",
    )
    parser.add_argument(
        "--add_param",
        action="store_true",
        default=False,
        help="add option to exps",
    )
    parser.add_argument(
        "--delete_param",
        action="store_true",
        default=False,
        help="delete option to exps",
    )
    parser.add_argument(
        "--generate",
        action="store_true",
        default=False,
        help="generate new experiment",
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        default=False,
        help="delete old experiments",
    )
    parser.add_argument(
        "--exp_folder",
        nargs="?",
        type=str,
        default="exp_jsons",
        help="path to the json that define the experiments to run",
    )
    parser.add_argument(
        "--path_to_information",
        nargs="?",
        type=str,
        default="informations",
        help="path to information jsons",
    )
    parser.add_argument(
        "--reset",
        nargs="+",
        default=[],
        type=list,
        help="list of options to reset in all exps",
    )
    args = parser.parse_args()
    if args.status:
        get_status(
            exp_folder=args.exp_folder, path_to_information=args.path_to_information
        )
    if args.add_param:
        add_parameters_to_exps(
            exp_folder=args.exp_folder, path_to_information=args.path_to_information
        )
    if args.generate:
        create_exp(
            exp_folder=args.exp_folder, path_to_information=args.path_to_information
        )
    if args.delete:
        delete_exps(
            exp_folder=args.exp_folder, path_to_information=args.path_to_information
        )
    if args.delete_param:
        delete_key_in_exps(
            exp_folder=args.exp_folder, path_to_information=args.path_to_information
        )
    if args.reset != []:
        reset_exps(
            exp_folder=args.exp_folder,
            path_to_information=args.path_to_information,
            keys_to_reset=args.reset,
        )
    remove_chache_folders()
