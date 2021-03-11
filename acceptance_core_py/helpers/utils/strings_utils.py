import logging
import re


def is_string_found_in(
    needle: str, string_for_search: str, silent: bool = False
) -> bool:
    if not silent:
        logging.info(
            f"Searching needle string '{needle}' in string for search '{string_for_search}' with 'ignorecase'"
        )
    return is_regex_found_in(needle, string_for_search, silent)


def is_regex_found_in(regex: str, string_for_search: str, silent: bool = False) -> bool:
    if not silent:
        logging.info(
            f"Searching regex '{regex}' in string for search '{string_for_search}' with 'ignorecase'"
        )
    return bool(re.search(regex, string_for_search, re.IGNORECASE))


def is_strings_equals(
    expected_string: str, actual_string: str, silent: bool = False
) -> bool:
    if not silent:
        logging.info(
            f"Checking if expected string '{expected_string}' "
            f"is equals with actual string '{actual_string}' in lowercase"
        )
    return expected_string.lower() == actual_string.lower()


def filter_for_only_numbers(string: str) -> str:
    logging.info(f"Removing all but numbers from '{string}'")
    return re.sub("\\D", "", string)
