from __future__ import annotations


class Selector:
    selector = None

    def __init__(self, selector: str):
        self.selector = selector

    def __str__(self):
        return self.selector

    def child_by_class(self, class_name: str, direct_child: bool = False) -> Selector:
        return self.get_instance(self.selector + (" > " if direct_child else ' ') + "." + class_name)

    def get_instance(self, selector: str) -> Selector:
        return Selector(selector)
