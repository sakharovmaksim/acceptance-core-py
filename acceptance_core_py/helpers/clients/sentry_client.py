from __future__ import annotations

import logging

import sentry_sdk
from sentry_sdk import configure_scope

from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.exception.ac_exception import ACException
from acceptance_core_py.helpers import env


class SentryClient:
    """Attention: Singleton object, use by SentryClient.get_instance().capture_exception()"""

    __instance = None
    __initialized = None
    __screenshot_url = None

    def __init__(self):
        pass

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            logging.debug("Creating SentryClient instance")
            cls.__instance = SentryClient()
        return cls.__instance

    def set_screenshot_url(self, screenshot_url: str) -> SentryClient:
        self.__screenshot_url = screenshot_url
        return self.get_instance()

    def init_client(self):
        if not self.__initialized:
            sentry_project_dsn_url = env.get_sentry_project_dsn_url()
            project_name = env.get_project_name()
            if not project_name:
                raise ACException("Could not get value of project_name from ENV")
            if not sentry_project_dsn_url:
                raise ACException(
                    "Could not get value of sentry_project_dsn_url from ENV"
                )

            logging.debug(f"Init sentry sdk with {sentry_project_dsn_url=}")
            sentry_sdk.init(sentry_project_dsn_url)
            self.__initialized = True

    def capture_exception(self, exception=None) -> str:
        self.init_client()
        with configure_scope() as scope:
            scope.set_level("info")
            scope.set_tag(
                "host_url", env.get_testing_project_url_data().scheme_and_netloc
            )
            scope.set_tag("test", env.get_test_name_with_path())
            scope.set_extra("failing_url", driver_actions.get_current_url().origin_url)
            scope.set_tag("test_type", env.get_test_type())
            if env.is_reference_mode():
                scope.set_tag("reference_mode", True)
            if env.is_testing_mode():
                scope.set_tag("testing_mode", True)
            if self.__screenshot_url:
                scope.set_extra("failing_screenshot", self.__screenshot_url)

        event_id = sentry_sdk.capture_exception(exception, scope)
        event_sentry_url: str = (
            f"https://sentry.asna.pro/sentry/{env.get_project_name()}/?query={event_id}"
        )
        logging.warning(
            f"--- Sentry captured exception URL is: '{event_sentry_url}' ---"
        )
        sentry_link_step(event_sentry_url)
        return event_sentry_url
