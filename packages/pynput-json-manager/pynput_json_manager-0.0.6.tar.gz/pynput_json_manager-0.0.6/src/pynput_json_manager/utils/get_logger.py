import logging
import os


def get_root_dir() -> str:
    """
    This function retrieves the root dir of this package.
    """
    return os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


def get_logger(log_file: str = "logs.log") -> logging.Logger:
    """
    This function creates a logger that we use through out the package.

    Args:
        log_file: relative file name for the log file to be stored in src/utils/../../logs/.
    """
    root_dir = os.getcwd()
    log_dir = os.path.join(root_dir, "logs")
    if "logs" not in os.listdir(root_dir):
        os.mkdir(log_dir)
    if log_file == "logs.log" and log_file in os.listdir(log_dir):
        os.remove(os.path.join(log_dir, log_file))
    if log_file in os.listdir(log_dir):
        raise ValueError(f"the provided log file already exists : {log_file}")
    formatter = logging.Formatter("%(message)s")
    handler_info = logging.FileHandler(
        os.path.join(log_dir, log_file), mode="a", encoding="utf-8"
    )
    handler_info.setFormatter(formatter)
    handler_info.setLevel(logging.INFO)
    logger = logging.getLogger("upperbound_logger")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler_info)
    return logger
