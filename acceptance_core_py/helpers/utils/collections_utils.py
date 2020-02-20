import logging

from acceptance_core_py.core.exception.at_exception import ATException


def check_collection_is_not_empty(collection) -> bool:
    logging.info(f"Checking for emptiness of collections")
    if len(collection) == 0:
        raise ATException(f"Collection {str(collection)} is has unexpectedly len == 0")
    return True


