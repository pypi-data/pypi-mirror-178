import os
import copy


def remove_a_specified_exp(
    idx: int, exp_paths: list, number_files_already_removed: int
) -> int:
    """
    Given the index of the exp and the list of paths of the exps, we remove the specified file.

    Args:
        idx: index of exp to remove
        exp_paths: list of exp paths
        number_files_already_removed: number of already removed paths
    """
    os.remove(exp_paths[idx - number_files_already_removed])
    for cpt in range(
        idx + 1 - number_files_already_removed,
        len(exp_paths) - number_files_already_removed,
    ):
        old_name = exp_paths[cpt]
        new_name = exp_paths[cpt - 1]
        os.rename(old_name, new_name)
    number_files_already_removed += 1
    return number_files_already_removed


def remove_exp(exp_paths: list):
    """
    Iteratively removes exps in list.
    
    Args:
        exp_paths: list of exp paths
    """
    local_list = copy.deepcopy(exp_paths)
    id_exp = (
        int(
            input(
                f"Please select as Id from {1} to {len(local_list)} (negative value to stop)  : "
            )
        )
        - 1
    )
    number_files_already_removed = 0
    while id_exp >= 0:
        number_files_already_removed = remove_a_specified_exp(
            idx=id_exp,
            exp_paths=local_list,
            number_files_already_removed=number_files_already_removed,
        )
        id_exp = (
            int(
                input(
                    f"Please select as Id from {1} to {len(local_list)} (negative value to stop)  : "
                )
            )
            - 1
        )
