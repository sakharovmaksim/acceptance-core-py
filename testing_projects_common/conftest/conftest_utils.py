import logging

from _pytest.fixtures import FixtureRequest

from acceptance_core_py.core.actions.screenshot_actions import ScreenshotActions
from acceptance_core_py.helpers import env
from acceptance_core_py.helpers.clients.sentry_client import SentryClient


def send_finished_test_metrics(request: FixtureRequest):
    if is_test_failed(request) and env.is_need_send_metrics():
        # send_failed_test_metrics(request)
        pass


def send_failed_test_metrics(request: FixtureRequest):
    sentry_instance: SentryClient = SentryClient.get_instance()
    screenshot_url = capture_screenshot_on_fail()
    if screenshot_url:
        sentry_instance.set_screenshot_url(screenshot_url)
    exception = request.node.exception
    sentry_instance.capture_exception(exception)


def capture_screenshot_on_fail() -> str:
    screenshot_url = ScreenshotActions.get_instance().capture_full_page_screenshot(
        "FAILING"
    )
    logging.warning(f"--- Screenshot on Failing: {screenshot_url} ---")
    return screenshot_url


def is_test_failed(request: FixtureRequest) -> bool:
    # For good test exit by CTRL+C check attr 'rep_call' exists in request.node
    return hasattr(request.node, "rep_call") and request.node.rep_call.failed
