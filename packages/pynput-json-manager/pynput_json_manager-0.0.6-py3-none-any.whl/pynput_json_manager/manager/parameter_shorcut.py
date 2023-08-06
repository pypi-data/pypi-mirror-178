from .parameters_information import get_inforamtion


def get_shortcut(key: str, path_to_information: str) -> str:
    """
    gets shortcut for exp parameter (to get a readable table)

    Args:
        key: key for which we search the corresponding shortcut
        path_to_information: path to the files that define the keys of our experiments
    """
    shortcuts, _, _, _ = get_inforamtion(path_to_information=path_to_information)
    if key in shortcuts:
        return shortcuts[key]
    return key
