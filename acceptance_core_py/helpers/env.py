import logging
import os

from acceptance_core_py.core.testing_project_url_data import TestingProjectUrlData
from acceptance_core_py.helpers.test_runner.ci_testing_host_helper import (
    get_testing_project_url_data_from_ci_env,
)
from acceptance_core_py.helpers.utils.strings_utils import is_strings_equals


def get_testing_project_url_data() -> TestingProjectUrlData:
    """Заполни переменную TESTING_HOST_URL или создай в окружении переменную CI_TESTING_HOST_URL"""
    testing_host_url_from_config = os.environ.get("TESTING_HOST_URL", "")
    if testing_host_url_from_config and testing_host_url_from_config != "FROM_ENV":
        return TestingProjectUrlData(testing_host_url_from_config)

    return get_testing_project_url_data_from_ci_env()


def get_waiting_default_timeout() -> int:
    return int(os.environ.get("WAITING_DEFAULT_TIMEOUT", 35))


def get_test_name() -> str:
    """Пример возвращаемого значения: test_correctly_opening_some_page"""
    test_name = os.environ.get("PYTEST_CURRENT_TEST").split(":")[-1].split(" ")[0]
    logging.debug(f"Got current test name: '{test_name}'")
    return test_name


def get_test_file_name() -> str:
    """Пример возвращаемого значения: tests/test_correctly_opening_pages.py"""
    test_file_name = os.environ.get("PYTEST_CURRENT_TEST").split(":")[0]
    logging.debug(f"Got current test file name: '{test_file_name}'")
    return test_file_name


def get_test_name_with_path() -> str:
    """Пример возвращаемого значения: 'tests.main_page.test_auth_form.py.test_authorization_by_form'"""
    result = get_test_file_name().replace("/", ".") + "." + get_test_name()
    logging.debug(f"Generated test name with path '{result}'")
    return result


def get_project_name() -> str:
    project_name = os.environ.get("PROJECT_NAME", "")
    logging.debug(f"Got '{project_name=}' from ENV")
    return project_name


def get_sentry_project_dsn_url() -> str:
    sentry_project_dsn_url = os.environ.get("SENTRY_PROJECT_DSN_URL", "")
    logging.debug(f"Got '{sentry_project_dsn_url=}' from ENV: ")
    return sentry_project_dsn_url


def is_need_send_metrics() -> bool:
    return os.environ.get("SEND_METRICS") == "True"


def is_ui_test() -> bool:
    var = "IS_UI_TEST"
    if os.environ.get(var):
        return not is_strings_equals(os.environ.get(var), "False")
    return True


def is_headless_mode() -> bool:
    """Возвращает True, если требуется selenium headless mode"""
    var = "HEADLESS_MODE"
    if os.environ.get(var):
        return os.environ.get(var) == "True"
    return False


# Данные из окружения GitLab CI (прочитай https://docs.gitlab.com/ee/ci/variables/predefined_variables.html)


def get_ci_commit_ref_name() -> str:
    """Возвращает branch name как есть из Gitlab-CI Runner Environment"""
    var = "CI_COMMIT_REF_NAME"
    if os.environ.get(var):
        return os.environ.get(var)
    return "no_ci_branch_name"


def get_ci_commit_ref_slug() -> str:
    """Возвращает немного отформатированное branch name из Gitlab-CI Runner Environment"""
    var = "CI_COMMIT_REF_SLUG"
    if os.environ.get(var):
        return os.environ.get(var)
    return "no_ci_branch_name"


def get_ci_project_id() -> str:
    var = "CI_PROJECT_ID"
    if os.environ.get(var):
        return os.environ.get(var)
    return ""


def get_ci_project_name() -> str:
    var = "CI_PROJECT_NAME"
    if os.environ.get(var):
        return os.environ.get(var)
    return ""


# Нужно для движка visual tests


def is_reference_mode() -> bool:
    var = "REFERENCE_MODE"
    if os.environ.get(var):
        return os.environ.get(var) == "1"
    return False


def is_testing_mode() -> bool:
    var = "TESTING_MODE"
    if os.environ.get(var):
        return os.environ.get(var) == "1"
    return False


def get_test_type() -> str:
    """Return type of test: visual or ui"""
    # Change to constants if you want to check types
    if is_reference_mode() or is_testing_mode():
        return "visual"
    return "functional"
