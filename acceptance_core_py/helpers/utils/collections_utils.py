import logging
from typing import List

from acceptance_core_py.core.exception.at_exception import ATException


def check_collection_is_not_empty(collection, error_message: str = None) -> bool:
    logging.info('Checking for emptiness collection')
    if len(collection) == 0:
        if not error_message:
            error_message = f"Collection {collection=} has unexpectedly length == 0"
        raise ATException(error_message)
    return True


def is_exist_index_in_list(in_list: List, index: int) -> bool:
    return index < len(in_list)


def check_collection_for_no_duplicates(collection, error_message: str = None) -> bool:
    logging.info('Checking collection for duplicates')
    if len(collection) != len(set(collection)):
        if not error_message:
            error_message = f"Collection {collection=} has some duplicate elements."
        raise ATException(error_message)
    return True
