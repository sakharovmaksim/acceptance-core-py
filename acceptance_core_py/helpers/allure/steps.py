import logging

import allure
import pytest


# Фикстуры для prototype тестов


@allure.step("Выполнить: {with_text}")
def do_step(with_text: str):
    logging.warning(f"Выполнить: {with_text}")


@allure.step("Проверить: {with_text}")
def assert_step(with_text: str):
    logging.warning(f"Проверить: {with_text}")


@allure.step("Подготовка")
def prepare_step():
    logging.warning("Подготовка")


@allure.step("Основная часть")
def main_step():
    logging.warning("Основная часть")


@allure.step("Завершение")
def teardown_step():
    logging.warning("Завершение")


@allure.step("Прото-тест отмечен, как skipped. Его нужно написать в настоящем коде")
def mark_skipped_proto_test_step():
    pytest.skip("Это прото-тест. Его нужно написать в настоящем коде")


# Фикстуры для кода тестов


@allure.step("Код выполнил: {with_text}")
def code_step(with_text: str):
    pass


@allure.step("Код проверит: {with_text}")
def assert_code_step(with_text: str):
    """'Проверит' в будущем, потому что написать что-то этим методом после упавшего ассерта уже не получится"""
    pass


@allure.step("Код будет ожидать: {with_text}")
def waiting_code_step(with_text: str):
    """'дождется' в будущем, потому что написать что-то этим методом после упавшего ожидания уже не получится"""
    pass


@allure.step("Перехваченный exception в Sentry: {event_url}")
def sentry_link_step(event_url: str):
    pass
