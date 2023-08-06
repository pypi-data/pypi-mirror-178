"""Regroups tool for the package.
"""
import logging
import os
from typing import List

from . import __name__ as package_name

logger = logging.getLogger(__name__)

def create_path_if_needed(directory: str):
    """Creates directory if it doesn't exist.

    Parameters
    ----------
    directory : str
        Path to directory to create.

    Raises
    ------
    ValueError
        If directory can't be created.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    elif os.path.islink(directory) or os.path.isfile(directory):
        raise ValueError('Unable to create directory %r' % directory)

def remove_duplicates(input_list: List) -> List:
    """Removes duplicate values in a list.

    Parameters
    ----------
    input_list : List
        Input list.

    Returns
    -------
    List
        Output list.
    """
    return [value for index, value in enumerate(input_list) if value not in input_list[index+1:]]
