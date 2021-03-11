import logging
import os

import pytest

from acceptance_core_py.core import driver
from testing_projects_common.conftest.conftest_utils import send_finished_test_metrics


def pytest_configure(config):
    config.addinivalue_line("markers", "mobile: initialize selenium with mobile mode")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Hack https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures
    setattr(item, "rep_" + rep.when, rep)
    # Create attribute request.node.exception for request.node if test failed
    if rep.when == "call" and rep.failed:
        setattr(item, "exception", call.excinfo.value)


@pytest.fixture(autouse=True)
def run_test(request):
    driver.mobile_mode = False

    if request.node.get_closest_marker("mobile"):
        driver.mobile_mode = True

    driver.initialize()

    # Запуск теста
    yield

    send_finished_test_metrics(request)

    driver.close_driver()


@pytest.fixture()
def enable_reference_mode():
    """Using in pytest-X.ini"""
    logging.info("Enabling reference mode for visual tests")
    os.environ["REFERENCE_MODE"] = "1"


@pytest.fixture()
def enable_testing_mode():
    """Using in pytest-X.ini"""
    logging.info("Enabling testing mode for visual tests")
    os.environ["TESTING_MODE"] = "1"


@pytest.fixture()
def enable_developer_mode(enable_reference_mode, enable_testing_mode):
    logging.info("Enabling developer mode for visual tests")
    enable_reference_mode
    enable_testing_mode
