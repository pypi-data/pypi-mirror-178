import os
import sys
import random


def is_package_available(package_name):
    """
    It checks if a Python package is installed.

    Args:
        package_name (string):  A Python package name

    Returns:
        True if the Python package is installed, False otherwise.
    """
    available = False
    if package_name in sys.modules:
        available = True
    return available


def numpy_seed(seed=None):
    """
    It imports and seeds Numpy, if it's installed on the system.

    Args:
        Void

    Returns:
        Void
    """
    if is_package_available("numpy"):
        import numpy as np
        if seed is None:
            np.random.seed(random.randint(1, 1E6))
        else:
            np.random.seed(seed)


def torch_seed(seed=None):
    """
    It imports and seeds Torch, if it's installed.

    Args:
        Void

    Returns:
        Void
    """
    if is_package_available("torch"):
        import torch
        if seed is None:
            torch.manual_seed(random.randint(1, 1E6))
            torch.cuda.manual_seed_all(random.randint(1, 1E6))
        else:
            torch.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)


def python_seed(seed=None):
    """
    It seeds OS-based Python RNGs.

    Args:
        Void

    Returns:
        Void
    """
    if seed is None:
        os_seed = random.randint(1, 1E6)
        os.environ['PYTHONHASHSEED'] = str(os_seed)
    else:
        os.environ['PYTHONHASHSEED'] = str(seed)


def universal_seed(seed=1234):
    """
    It seeds all the native Python RNGs as well as Numpy and Torch (if the
    latter two are already installed)

    Args:
        seed (long int):    The seed for the RNGs

    Returns:
        void
    """
    random.seed(seed)
    numpy_seed(seed=seed)
    torch_seed(seed=seed)
    python_seed(seed=seed)
