from __future__ import annotations

from selenium.webdriver.remote.webelement import WebElement

from acceptance_core_py.core.actions import driver_actions


class Selector:
    def __init__(self, selector: str):
        self.__selector = selector

    def __str__(self):
        """Return Selector as string"""
        return self.__selector

    @property
    def web_element(self) -> WebElement:
        return driver_actions.locate_element(self)

    # Child by...

    def child_by_class(self, class_name: str, direct_child: bool = False) -> Selector:
        return self.__get_instance(self.__selector + (" > " if direct_child else ' ') + f".{class_name}")

    def child_by_id(self, id_name: str, direct_child: bool = False) -> Selector:
        return self.__get_instance(self.__selector + (" > " if direct_child else ' ') + f"#{id_name}")

    def child_by_attribute(self, name: str, value: str = None, direct_child: bool = False) -> Selector:
        selector = f"[{name}]" if value is None else f"[{name}=\"{value}\"]"
        return self.__get_instance(self.__selector + (" > " if direct_child else ' ') + selector)

    def child_by_tag(self, tag_name: str, direct_child: bool = True) -> Selector:
        return self.__get_instance(self.__selector + (" > " if direct_child else ' ') + tag_name)

    def child_by_begins_with(self, name: str, type: str = "class") -> Selector:
        return self.__get_instance(self.__selector + f" *[{type}^=\"{name}\"]")

    # Child by contains...

    def child_by_class_contains(self, class_name: str, direct_child: bool = False) -> Selector:
        return self.child_by_attribute_contains("class", class_name, direct_child)

    def child_by_attribute_contains(self, name: str, value: str, direct_child: bool = False) -> Selector:
        return self.__get_instance(self.__selector + (" > " if direct_child else ' ') + f"[{name}*=\"{value}\"]")

    # Having...

    def having_attribute(self, name: str, value: str = None) -> Selector:
        selector = f"[{name}]" if value is None else f"[{name}=\"{value}\"]"
        return self.__get_instance(self.__selector + selector)

    def having_class(self, class_name: str) -> Selector:
        return self.__get_instance(self.__selector + f".{class_name}")

    def having_tag(self, tag_name: str) -> Selector:
        return self.__get_instance(self.__selector + tag_name)

    def not_having_class(self, class_name: str) -> Selector:
        return self.__get_instance(self.__selector + f":not(.{class_name})")

    def not_having_attribute(self, name: str) -> Selector:
        return self.__get_instance(self.__selector + f":not([{name}])")

    # Having contains...

    def having_attribute_contains(self, name: str, value: str) -> Selector:
        return self.__get_instance(self.__selector + f"[{name}*=\"{value}\"]")

    def having_attribute_ends_with(self, name: str, value: str) -> Selector:
        return self.__get_instance(self.__selector + f"[{name}$=\"{value}\"]")

    def having_class_contains(self, class_name: str) -> Selector:
        return self.having_attribute_contains("class", class_name)

    def not_having_class_contains(self, class_name: str) -> Selector:
        return self.not_having_attribute_contains("class", class_name)

    def not_having_attribute_contains(self, name: str, value: str) -> Selector:
        return self.__get_instance(self.__selector + f":not([{name}*=\"{value}\"])")

    # Others...

    def nth_of_type(self, index: int) -> Selector:
        return self.__get_instance(self.__selector + f":nth-of-type({str(index)})")

    def first(self) -> Selector:
        return self.__get_instance(self.__selector + ":first")

    def last(self) -> Selector:
        return self.__get_instance(self.__selector + ":last")

    def first_of_type(self) -> Selector:
        return self.__get_instance(self.__selector + ":first-of-type")

    def last_of_type(self) -> Selector:
        return self.__get_instance(self.__selector + ":last-of-type")

    def next_sibling(self) -> Selector:
        return self.__get_instance(self.__selector + "+")

    def __get_instance(self, selector: str) -> Selector:
        return Selector(selector)
