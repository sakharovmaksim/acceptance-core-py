from acceptance_core_py.core.actions import driver_actions
from acceptance_core_py.core.block import Block
from content import content_vars


class HeaderCartBlock(Block):
    block_attribute_name = content_vars.test_attr_name
    block_attribute_value = 'mobile-header-cart'

    def get_text(self) -> str:
        return driver_actions.grab_text_from_element(self.me)
