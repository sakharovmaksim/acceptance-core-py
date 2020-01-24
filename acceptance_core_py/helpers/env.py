import logging
import os


def get_base_url() -> str:
    base_url = os.environ["HOST_URL"]
    if not base_url:
        raise Exception("Could not get value for variable HOST_URL from ENV")

    logging.info(f"Got base URL from ENV: '{base_url}'")
    return base_url


def is_enable_mobile_emulation_mode() -> bool:
    return os.environ["MOBILE_EMULATION"] != "False"


def get_waiting_default_timeout() -> int:
    return int(os.environ["WAITING_DEFAULT_TIMEOUT"]) or 35


def get_test_name() -> str:
    """Example: test_correctly_opening_public_page_organization"""
    test_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
    logging.info(f"Getted current test name: '{test_name}'")
    return test_name


def get_test_file_name() -> str:
    """Example: tests/test_correctly_opening_pages.py"""
    test_file_name = os.environ.get('PYTEST_CURRENT_TEST').split(':')[0]
    logging.info(f"Getted current test file name: '{test_file_name}'")
    return test_file_name
