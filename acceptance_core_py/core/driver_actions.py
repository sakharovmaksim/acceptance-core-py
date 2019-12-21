import logging

from acceptance_core_py.core import driver
from acceptance_core_py.helpers import env


def open_relative_url(relative_url: str):
    opened_url = env.get_base_url() + relative_url
    logging.info("Opening URL " + opened_url)
    driver.instance.get(opened_url)
