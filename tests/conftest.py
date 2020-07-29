import os
import pytest
import logging

from _pytest.fixtures import FixtureRequest

from acceptance_core_py.core import driver
from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.helpers import env


def pytest_configure(config):
    config.addinivalue_line('markers', 'mobile: initialize selenium with mobile mode')
    config.addinivalue_line('markers', 'no_ui: not start selenium')


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
    need_selenium_driver_initialize = True

    if request.node.get_closest_marker('mobile'):
        driver.mobile_mode = True
    if request.node.get_closest_marker('no_ui'):
        os.environ['IS_UI_TEST'] = 'False'
        need_selenium_driver_initialize = False

    if need_selenium_driver_initialize:
        driver.initialize()

    # Test running here
    yield

    # For good test exit by CTRL+C check attr 'rep_call' exists in request.node
    if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
        take_test_screenshot_and_send_metrics(request)

    if need_selenium_driver_initialize:
        driver.close_driver()


def take_test_screenshot_and_send_metrics(request: FixtureRequest):
    """Add your mechanism capturing screenshot and test metrics sender"""
    screenshot_url = ''
    if env.is_ui_test():
        logging.warning("--- Capturing failed page screenshot and saving some metrics and artifacts ---")
        # screenshot_url = ScreenshotActions.get_instance().capture_full_page_screenshot("FAILED")

        final_url = driver_actions.get_url()
        logging.warning(f"--- Failed test final URL is: '{final_url}'")

    # if env.is_need_send_metrics():
    #     PrometheusClient.get_instance().push_test_failed_metric_to_gateway()
    #     SentryClient.get_instance().set_screenshot_url(screenshot_url).capture_exception(request.node.exception)

