from abc import ABC

from acceptance_core_py.core.exception.at_exception import ATException
from acceptance_core_py.core.selector import Selector


class Block(ABC):
    block_class = None
    block_class_contains = None
    block_id = None
    block_tag = None
    block_attribute_name = None
    block_attribute_value = None

    selector = Selector

    def __init__(self, selector=None):
        if selector is None:
            selector = Selector("")
        if isinstance(selector, Selector):
            self.selector = self.get_block_selector_from_context(selector)
        else:
            self.selector = Selector(str(selector))

    def __str__(self):
        return self.me().__str__()

    def get_block_selector_from_context(self, context_selector: Selector) -> Selector:
        if self.block_class:
            return context_selector.child_by_class(self.block_class)
        elif self.block_class_contains:
            return context_selector.child_by_class_contains(self.block_class_contains)
        elif self.block_id:
            return context_selector.child_by_id(self.block_id)
        elif self.block_tag:
            return context_selector.child_by_tag(self.block_tag)
        elif self.block_attribute_name and self.block_attribute_value:
            return context_selector.child_by_attribute(self.block_attribute_name, self.block_attribute_value)
        else:
            raise ATException("Your Block implementation must have either block_id, block_class, " +
                              "block_tag or block_attribute_name and block_attribute_value property specified.")

    def me(self) -> Selector:
        return self.selector
