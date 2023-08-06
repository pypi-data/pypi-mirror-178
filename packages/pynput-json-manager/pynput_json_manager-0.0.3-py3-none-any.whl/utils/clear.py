import os
import shutil


def remove_chache_folders(current_repo: str = ""):
    """
    clears the pycache folders

    Args:
        current_repo: repository to clear
    """
    if current_repo == "":
        new_refs = [elem for elem in os.listdir()]
    else:
        new_refs = [current_repo + "/" + elem for elem in os.listdir(current_repo)]
    for elem in new_refs:
        if os.path.isdir(elem):
            if "__pycache__" in elem:
                shutil.rmtree(elem)
            else:
                remove_chache_folders(current_repo=elem)
