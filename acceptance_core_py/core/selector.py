from __future__ import annotations


class Selector:
    selector = None

    def __init__(self, selector: str):
        self.selector = selector

    def __str__(self):
        return self.selector

    # Child by...

    def child_by_class(self, class_name: str, direct_child: bool = False) -> Selector:
        return self.get_instance(self.selector + (" > " if direct_child else ' ') + f".{class_name}")

    def child_by_id(self, id_name: str, direct_child: bool = False) -> Selector:
        return self.get_instance(self.selector + (" > " if direct_child else ' ') + f"#{id_name}")

    def child_by_attribute(self, name: str, value: str = None, direct_child: bool = False) -> Selector:
        selector = f"[{name}]" if value is None else f"[{name}=\"{value}\"]"
        return self.get_instance(self.selector + (" > " if direct_child else ' ') + selector)

    def child_by_tag(self, tag_name: str, direct_child: bool = False) -> Selector:
        return self.get_instance(self.selector + (" > " if direct_child else ' ') + tag_name)

    def child_by_begins_with(self, name: str, type: str = "class") -> Selector:
        return self.get_instance(self.selector + f" *[{type}^=\"{name}\"]")

    # Child by contains...

    def child_by_class_contains(self, class_name: str, direct_child: bool = False) -> Selector:
        return self.child_by_attribute_contains("class", class_name, direct_child)

    def child_by_attribute_contains(self, name: str, value: str, direct_child: bool = False) -> Selector:
        return self.get_instance(self.selector + (" > " if direct_child else ' ') + f"[{name}*=\"{value}\"]")

    # Having...

    def having_attribute(self, name: str, value: str = None) -> Selector:
        selector = f"[{name}]" if value is None else f"[{name}=\"{value}\"]"
        return self.get_instance(self.selector + selector)

    def having_class(self, class_name: str) -> Selector:
        return self.get_instance(self.selector + f".{class_name}")

    def having_tag(self, tag_name: str) -> Selector:
        return self.get_instance(self.selector + tag_name)

    def not_having_class(self, class_name: str) -> Selector:
        return self.get_instance(self.selector + f":not(.{class_name})")

    def not_having_attribute(self, name: str) -> Selector:
        return self.get_instance(self.selector + f":not([{name}])")

    # Having contains...

    def having_attribute_contains(self, name: str, value: str) -> Selector:
        return self.get_instance(self.selector + f"[{name}*=\"{value}\"]")

    def having_attribute_ends_with(self, name: str, value: str) -> Selector:
        return self.get_instance(self.selector + f"[{name}$=\"{value}\"]")

    def having_class_contains(self, class_name: str) -> Selector:
        return self.having_attribute_contains("class", class_name)

    def not_having_class_contains(self, class_name: str) -> Selector:
        return self.not_having_attribute_contains("class", class_name)

    def not_having_attribute_contains(self, name: str, value: str) -> Selector:
        return self.get_instance(self.selector + f":not([{name}*=\"{value}\"])")

    # Others...

    def nth_of_type(self, index: int) -> Selector:
        return self.get_instance(self.selector + f":nth-of-type({index})")

    def first(self) -> Selector:
        return self.get_instance(self.selector + ":first")

    def last(self) -> Selector:
        return self.get_instance(self.selector + ":last")

    def first_of_type(self) -> Selector:
        return self.get_instance(self.selector + ":first-of-type")

    def last_of_type(self) -> Selector:
        return self.get_instance(self.selector + ":last-of-type")

    def next_sibling(self) -> Selector:
        return self.get_instance(self.selector + "+")

    def get_instance(self, selector: str) -> Selector:
        return Selector(selector)
