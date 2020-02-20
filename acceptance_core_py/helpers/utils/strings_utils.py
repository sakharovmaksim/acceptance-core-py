import logging
import re


def is_string_found_in(needle: str, string_for_search: str) -> bool:
    logging.info(f"Searching needle string '{needle}' in string for search '{string_for_search}' with 'ignorecase'")
    return bool(re.search(needle, string_for_search, re.IGNORECASE))


def is_strings_equals(expected_string: str, actual_string: str) -> bool:
    logging.info(f"Checking if expected string '{expected_string}' "
                 f"is equals with actual string '{actual_string}' in lowercase")
    return expected_string.lower() == actual_string.lower()
