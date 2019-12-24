import logging
import re


def is_string_found_in(needle: str, string_for_search: str) -> bool:
    logging.info(f"Searching needle string '{needle}' in string for search '{string_for_search}' with 'ignorecase'")
    return bool(re.search(needle, string_for_search, re.IGNORECASE))
