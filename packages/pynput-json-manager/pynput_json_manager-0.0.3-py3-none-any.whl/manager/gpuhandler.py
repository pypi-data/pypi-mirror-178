from typing import Any
import tensorflow as tf
import importlib.util
import sys
import subprocess


def get_mdl() -> list:
    """
    returns the gpu names
    """
    line_as_bytes = subprocess.check_output("nvidia-smi -L", shell=True)
    lines = line_as_bytes.decode("ascii").splitlines()
    output = []
    for line in lines:
        _, line = line.split(":", 1)
        line, _ = line.split("(")
        output.append(line.strip())
    return output


def _bytes_to_megabytes(bytes):
    return round((bytes / 1024) / 1024, 2)


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


def print_gpu_specs():
    """
    print name and memory available per gpu
    """
    if check_if_a_module_exists("nvidia_smi"):
        gpu_names = get_mdl()
        import nvidia_smi

        nvidia_smi.nvmlInit()
        _NUMBER_OF_GPU = nvidia_smi.nvmlDeviceGetCount()
        for gpu_id in range(_NUMBER_OF_GPU):
            handle = nvidia_smi.nvmlDeviceGetHandleByIndex(gpu_id)
            info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
            print(
                f'\033[92m{f"{gpu_names[gpu_id]}: {_bytes_to_megabytes(info.free)}Mo".center(45)}\033[0m'
            )
        nvidia_smi.nvmlShutdown()


def hardware_setup() -> Any:
    """
    enables gpu computations with tensorflow and
    returns the mirrored strategy if multiple gpus
    are dtected.
    """
    physical_devices = tf.config.list_physical_devices("GPU")

    if len(physical_devices) == 0:
        print(f"\n---------------------------------------------")
        print(f'\033[91m{f"no gpu detected, using CPU mode.".center(45)}\033[0m')
        print(f"---------------------------------------------\n")
        mirrored_strategy = None
    else:
        print(f"\n---------------------------------------------")
        for gpu in tf.config.list_physical_devices("GPU"):
            tf.config.experimental.set_memory_growth(gpu, True)
        print_gpu_specs()
        print(f"---------------------------------------------\n")
        if len(physical_devices) >= 2:
            mirrored_strategy = tf.distribute.MirroredStrategy()
        else:
            mirrored_strategy = None
    return mirrored_strategy
