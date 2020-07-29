import os

import pytest
import logging

from _pytest.fixtures import FixtureRequest

from acceptance_core_py.core import driver


def pytest_configure(config):
    config.addinivalue_line('markers', 'mobile: initialize selenium with mobile mode')


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

    if request.node.get_closest_marker('mobile'):
        driver.mobile_mode = True

    driver.initialize()

    # Test running here
    yield

    # For good test exit by CTRL+C check attr 'rep_call' exists in request.node
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        send_test_metrics(request)

    driver.close_driver()


@pytest.fixture()
def enable_reference_mode():
    """Using in pytest-X.ini"""
    logging.info('Enabling reference mode for visual tests')
    os.environ['REFERENCE_MODE'] = "1"


@pytest.fixture()
def enable_testing_mode():
    """Using in pytest-X.ini"""
    logging.info('Enabling testing mode for visual tests')
    os.environ['TESTING_MODE'] = "1"


def send_test_metrics(request: FixtureRequest):
    pass
    # if env.is_need_send_metrics():
    #     PrometheusClient.get_instance().push_test_failed_metric_to_gateway()
    #     SentryClient.get_instance().capture_exception(request.node.exception)
