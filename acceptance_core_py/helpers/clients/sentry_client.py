from __future__ import annotations
import logging
import sentry_sdk
from sentry_sdk import configure_scope

from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.helpers import env


class SentryClient:
    """Attention: Singleton object, use by SentryClient.get_instance().capture_exception()"""
    __instance = None
    __initialized = None
    # Look in Sentry project config
    __dsn_url = "YOUR_SENTRY_DSN"
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
            logging.debug(f'Init sentry sdk with {self.__dsn_url=}')
            #environment = 'production' if project_domains.is_production() else 'development'
            #release_name = env.get_git_branch_name() + '_' + env.get_commit_sha()
            sentry_sdk.init(self.__dsn_url)
            self.__initialized = True

    def capture_exception(self, exception=None):
        self.init_client()
        with configure_scope() as scope:
            scope.set_level('info')
            #scope.set_user({'email': env.get_gitlab_user_email()})
            scope.set_tag('host_url', env.get_base_url())
            #scope.set_tag('git_branch_in_ci', env.get_git_branch_name())
            # Replace '/' to '.' needs for compatibility with Prometheus format
            scope.set_tag('test', env.get_test_file_name().replace('/', '.') + '.' + env.get_test_name())
            #scope.set_tag('ci_job_id', env.get_ci_job_id())
            scope.set_extra('test_failed_url', driver_actions.get_url())
            if self.__screenshot_url:
                scope.set_extra('screenshot_from_fail', self.__screenshot_url)

        event_id = sentry_sdk.capture_exception(exception, scope)
        logging.warning(f"--- Captured exception with '{event_id=}' in Sentry ---")
