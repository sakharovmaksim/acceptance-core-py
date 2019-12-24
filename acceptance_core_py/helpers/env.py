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
